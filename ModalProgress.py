from functools import partial
from pathlib import Path
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot
from modal_progress import Ui_Dialog as Ui_ModalProgress
from DemucsWorker import DemucsWorker

# TODO: Either forcefully terminate thread on dialog close
#  or disable OS close action

class ModalProgress(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_ModalProgress()
        self.ui.setupUi(self)

        self.start_worker()

    def start_worker(self):
        # Gather options from main window
        parentUi = self.parent().ui
        input    = Path(parentUi.line_input.text())
        outdir   = Path(parentUi.line_outDir.text())
        method   = "demucs"   # eg. demucs, spleeter
        model    = "demucs"   # eg. demucs, demucs_quantized [UNUSED]
        stems2   = parentUi.rad_stems2.isChecked()

        # Prepare thread
        self.thread = QThread()
        if method == "demucs":
            self.worker = DemucsWorker()

        self.worker.moveToThread(self.thread)

        # Connect signals
        self.thread.started.connect(
                partial(self.worker.run, input, outdir, 'demucs', stems2)
            )
        self.worker.step.connect(self.update_progress)
        self.worker.statMsg.connect(self.showStatMsg)
        self.worker.finished.connect(
                lambda: self.worker_finished_hook(self.worker, self.thread)
            )
        self.thread.finished.connect(self.thread.deleteLater)

        # Start & stop
        self.thread.start()
        self.ui.btn_stop.clicked.connect(
                lambda: self.worker.stop()
            )

    def worker_finished_hook(self, worker, thread):
        # TODO: Make a "Open outDir" button
        # TODO: Change Stop button to a Close button
        self.showStatMsg("Finished.")
        thread.quit()
        worker.deleteLater()

    @pyqtSlot(int)
    def update_progress(self, progress):
        self.ui.progressBar.setValue(progress)

    @pyqtSlot(str)
    def showStatMsg(self, msg):
        if msg == "%p%":
            msg = "Separating..."

        print(msg)
        self.ui.lbl_status.setText(msg)

