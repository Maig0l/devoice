import sys
from time import sleep
from functools import partial
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtCore import QFile, QThread, QObject, pyqtSignal, pyqtSlot
from devoice import Ui_MainWindow
from DemucsWorker import DemucsWorker


# TODO: Show progress (and dispatch worker thread)
#  from a modal_progress.py dialog

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.btn_stop.setVisible(False)
        
        self.ui.btn_inputOpen.clicked.connect(self.select_file)
        self.ui.btn_outOpen  .clicked.connect(self.select_out_dir)
        self.ui.btn_go       .clicked.connect(self.call_demucs)

        # DEBUG
        self.ui.line_input.setText("/home/miguel/dox/projects/python/demucs-gui/snd/duvet.mp3")
        self.ui.line_outDir.setText("/home/miguel/dox/projects/python/demucs-gui/out")

    def select_file(self):
        # TODO: Add a check for file format
        prev_selected = self.ui.line_input.text()
        filename = QFileDialog.getOpenFileName(self, "",
                    prev_selected,
                    "Audio files (*.wav *.flac *.mp3 *.ogg *.opus);;All files (*.*)")[0]
        if filename:
            self.ui.line_input.setText(filename)

    def select_out_dir(self):
        prev_selected = self.ui.line_outDir.text()
        dir = QFileDialog.getExistingDirectory(self, directory=prev_selected)
        if dir:
            self.ui.line_outDir.setText(dir)

    def call_demucs(self):
        input = Path(self.ui.line_input.text())
        outdir = Path(self.ui.line_outDir.text())
        method = "demucs"   # eg. demucs, spleeter
        #model = "demucs"   # eg. demucs, demucs_quantized
        stems2 = self.ui.rad_stems2.isChecked()

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
                lambda: self.workerFinishedHook(self.worker, self.thread)
            )
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

        # UI responses
        self.ui.btn_go.setVisible(False)
        self.ui.btn_stop.setVisible(True)
        self.ui.btn_stop.clicked.connect(
                lambda: self.worker.stop()
            )
        self.thread.finished.connect(
                lambda: self.ui.btn_go.setVisible(True)
            )
        self.thread.finished.connect(
                lambda: self.ui.btn_stop.setVisible(False)
            )
        self.thread.finished.connect(
                lambda: self.showStatMsg("%p%")
            )

    def workerFinishedHook(self, worker, thread):
        worker.statMsg.emit("%p%")
        worker.step.emit(0)
        thread.quit()
        worker.deleteLater()

    @pyqtSlot(int)
    def update_progress(self, progress):
        self.ui.progressBar.setValue(progress)

    @pyqtSlot(str)
    def showStatMsg(self, msg):
        print(msg)
        self.ui.progressBar.setFormat(msg)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())

