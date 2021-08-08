from demucs.utils import *
import torch as th

def apply_model(model, mix, shifts=None, split=False,
                overlap=0.25, transition_power=1., progress=None):
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

        # TODO: Remove when external progress gets implemented
        if progress:
            #progress should be a QProgressBar widget
            #offsets = tqdm.tqdm(offsets, unit_scale=scale, ncols=120, unit='seconds')
            pass

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

        for offset in offsets:
            chunk = TensorChunk(mix, offset, segment)
            chunk_out = apply_model(model, chunk, shifts=shifts)
            chunk_length = chunk_out.shape[-1]
            out[..., offset:offset + segment] += weight[:chunk_length] * chunk_out
            sum_weight[offset:offset + segment] += weight[:chunk_length]

            offset += segment
            # TODO: Send progress signal to Qt or smth (look out for offsets)
            if progress:
                progressVal = (offset * 100) // offsets.stop
                progress.setValue(progressVal)
        assert sum_weight.min() > 0
        out /= sum_weight
        if progress:
            progress.setValue(100)
        return out
    elif shifts:
        max_shift = int(0.5 * model.samplerate)
        mix = tensor_chunk(mix)
        padded_mix = mix.padded(length + 2 * max_shift)
        out = 0
        for _ in range(shifts):
            offset = random.randint(0, max_shift)
            shifted = TensorChunk(padded_mix, offset, length + max_shift - offset)
            shifted_out = apply_model(model, shifted)
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

def mix_stems(sources):
    """
    Mix multiple stems into a single waveform with the same normalized volume as the source.
    """
    pass
