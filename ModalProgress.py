import subprocess, os, platform
from functools import partial
from pathlib import Path
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import QThread, pyqtSlot
from modal_progress import Ui_Dialog as Ui_ModalProgress
from DemucsWorker import DemucsWorker

# TODO: Either forcefully terminate thread on dialog close
#  or disable OS close action

class ModalProgress(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_ModalProgress()
        self.ui.setupUi(self)

        self.ui.btn_open.setVisible(False)

        self.parentUi = self.parent().ui
        self.start_worker()

    def start_worker(self):
        # Gather options from main window
        input    = Path(self.parentUi.line_input.text())
        outdir   = Path(self.parentUi.line_outDir.text())
        method   = "demucs"   # eg. demucs, spleeter
        model    = "demucs"   # eg. demucs, demucs_quantized [UNUSED]
        stems2   = self.parentUi.rad_stems2.isChecked()

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
        self.worker.finished.connect(self.worker_finished_hook)
        self.thread.finished.connect(self.thread.deleteLater)

        # Start & stop
        self.thread.start()
        self.ui.btn_stop.clicked.connect(
                lambda: self.worker.stop()
            )

    @pyqtSlot(int)
    def worker_finished_hook(self, exitCode):
        if exitCode == 0:
            self.showStatMsg("Finished.")
            self.ui.btn_open.setVisible(True)
            self.ui.btn_open.clicked.connect(
                    lambda: self.open_default_app(self.worker.track_folder)
                )
        else:
            self.showStatMsg("Canceled.")
        self.thread.quit()
        self.worker.deleteLater()

        # Change button actions
        self.btn_stop_to_close()

    def btn_stop_to_close(self):
        self.ui.btn_stop.setText("Close")
        self.ui.btn_stop.clicked.disconnect()
        self.ui.btn_stop.clicked.connect(self.close)

    def open_default_app(self, path):
        if platform.system() == 'Darwin':       # MacOS
            subprocess.Popen(('nohup', 'open', path))
        elif platform.system() == 'Windows':    # Windows
            os.startfile(path)
        else:                                   # Linux variants
            subprocess.Popen(('nohup', 'xdg-open', path))

    @pyqtSlot(int)
    def update_progress(self, progress):
        self.ui.progressBar.setValue(progress)

    @pyqtSlot(str)
    def showStatMsg(self, msg):
        if msg == "%p%":
            msg = "Separating..."

        print(msg)
        self.ui.lbl_status.setText(msg)

