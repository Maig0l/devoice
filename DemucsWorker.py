import tempfile
import os
from pathlib import Path
from shutil import rmtree
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QApplication

from demucs.pretrained import load_pretrained
from demucs.audio import AudioFile
from demucs.separate import load_track
from demucs.utils import *

import torch as th
import torchaudio as ta
from scipy.io import wavfile
from pydub import AudioSegment

class DemucsWorker(QObject):
    _running = False
    finished = pyqtSignal(int)
    step     = pyqtSignal(int)
    # Message shown in progress bar.
    # %p% for progress int
    statMsg  = pyqtSignal(str)

    def __init__(self):
        QObject.__init__(self)

    def apply_model(self, model, mix, shifts=None, split=False,
                    overlap=0.25, transition_power=1.):
        """
        Apply model to a given mixture.

        Args:
            shifts (int): if > 0, will shift in time `mix` by a random amount between 0 and 0.5 sec
                and apply the oppositve shift to the output. This is repeated `shifts` time and
                all predictions are averaged. This effectively makes the model time equivariant
                and improves SDR by up to 0.2 points.
            split (bool): if True, the input will be broken down in 8 seconds extracts
                and predictions will be performed individually on each and concatenated.
                Useful for model with large memory footprint like Tasnet.
            progress (bool): if True, show a progress bar (requires split=True)
        """
        assert transition_power >= 1, "transition_power < 1 leads to weird behavior."
        device = mix.device
        channels, length = mix.shape
        if split:
            out = th.zeros(4, channels, length, device=device)
            sum_weight = th.zeros(length, device=device)
            segment = model.segment_length
            stride = int((1 - overlap) * segment)
            offsets = range(0, length, stride)
            scale = stride / model.samplerate

            # We start from a triangle shaped weight, with maximal weight in the middle
            # of the segment. Then we normalize and take to the power `transition_power`.
            # Large values of transition power will lead to sharper transitions.
            weight = th.cat([th.arange(1, segment // 2 + 1),
                             th.arange(segment - segment // 2, 0, -1)]).to(device)
            assert len(weight) == segment
            # If the overlap < 50%, this will translate to linear transition when
            # transition_power is 1.
            weight = (weight / weight.max())**transition_power

            ###SET TRACE
            #import web_pdb; web_pdb.set_trace()

            offsets_count = sum(1 for i in offsets)

            for idx, offset in enumerate(offsets):
                if self._running:
                    chunk = TensorChunk(mix, offset, segment)
                    chunk_out = self.apply_model(model, chunk, shifts=shifts)
                    chunk_length = chunk_out.shape[-1]
                    out[..., offset:offset + segment] += weight[:chunk_length] * chunk_out
                    sum_weight[offset:offset + segment] += weight[:chunk_length]

                    offset += segment
                    self.step.emit(((idx+1) * 100) // offsets_count)
                else:
                    return False
            assert sum_weight.min() > 0
            out /= sum_weight
            return out
        elif shifts:
            max_shift = int(0.5 * model.samplerate)
            mix = tensor_chunk(mix)
            padded_mix = mix.padded(length + 2 * max_shift)
            out = 0
            for _ in range(shifts):
                offset = random.randint(0, max_shift)
                shifted = TensorChunk(padded_mix, offset, length + max_shift - offset)
                shifted_out = self.apply_model(model, shifted)
                out += shifted_out[..., max_shift - offset:]
            out /= shifts
            return out
        else:
            valid_length = model.valid_length(length)
            mix = tensor_chunk(mix)
            padded_mix = mix.padded(valid_length)
            with th.no_grad():
                out = model(padded_mix.unsqueeze(0))[0]
            return center_trim(out, length)

    def mix_stems(self, sources, output):
        """
        Mix multiple stems into a single waveform with the same normalized volume as the source.
        """
        waves = [AudioSegment.from_file(source) for source in sources]

        merged = AudioSegment.silent(
                    duration   = waves[0].duration_seconds*1000,
                    frame_rate = waves[0].frame_rate)

        for wave in waves:
            merged = merged.overlay(wave)

        # It gets exported in wav as to not waste time encoding
        #  to FLAC twice, as separate() always encodes to FLAC at the end
        merged.export(output, format="wav")

    def separate(self, filename, outDir, model="demucs", stems2=False):
        # `model` (str) can be any of the supported models by demucs
        #  eg. demucs, demucs_quantized, etc
        # Load model BY NAME
        self.statMsg.emit("Loading model...")
        self.modelName = model
        model = load_pretrained(self.modelName)
        model.to("cpu")

        sourceNames = ["drums", "bass", "other", "vocals"]

        # Load sound file and center the waveform or smth
        self.statMsg.emit("Loading song...")
        wav = load_track(filename, "cpu", model.audio_channels, model.samplerate)
        ref = wav.mean(0)
        wav = (wav - ref.mean()) / ref.std()

        # Apply model to get stems
        self.statMsg.emit("%p%")
        sources = self.apply_model(model, wav, shifts=0, split=True)
        if not self._running:
            return False
        sources = sources * ref.std() + ref.mean()

        # Save the stems to a temporary directory
        tmpDir = Path(tempfile.mkdtemp(prefix='devoice.'))

        for stemSrc, stemName in zip(sources, model.sources):
            # Magic math shit
            stemSrc = stemSrc / max(1.01 * stemSrc.abs().max(), 1)
            stemSrc = stemSrc.cpu()

            # Save as wavefile
            stem = str(tmpDir / stemName)
            wavname = str(tmpDir / f"{stemName}.wav")
            ta.save(wavname, stemSrc, sample_rate=model.samplerate)

        # Set up actual output directory
        self.statMsg.emit("Saving...")
        track_folder = outDir / filename.name.rsplit(".", 1)[0]
        track_folder.mkdir(exist_ok=True)

        if stems2:
            sources = []
            for f in os.listdir(tmpDir):
                if f != "vocals.wav":
                    sources.append(tmpDir / f)
            self.mix_stems(sources, tmpDir / 'off-vocal.wav')

            # Delete all other stem files
            for f in os.listdir(tmpDir):
                if f not in ['off-vocal.wav', 'vocals.wav']:
                    (tmpDir / f).unlink()

        # Reencode to FLAC into `track_folder` and clean tmpDir
        for stemName in os.listdir(tmpDir):
            stem = AudioSegment.from_file(tmpDir / stemName)

            codec = "flac"
            newName = stemName.rsplit(".", 1)[0] + f".{codec}"
            stem.export(track_folder / newName, format=codec)

        rmtree(tmpDir)
        print("Finished")
        return True

    def run(self, filename, outDir, model="demucs", stems2=False):
        self._running = True
        # TODO: use *args, **kwargs ? 
        result = self.separate(filename, outDir, model, stems2)
        self.finished.emit(
                0 if result else 1
            )

    def stop(self):
        self.statMsg.emit("Stopping...")
        self._running = False

if __name__ == '__main__':
    w = DemucsWorker()

