import os, sys
import magic
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from devoice import Ui_MainWindow
from ModalProgress import ModalProgress


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.btn_stop.setVisible(False)
        
        self.ui.btn_inputOpen.clicked.connect(self.select_file)
        self.ui.btn_outOpen  .clicked.connect(self.select_out_dir)
        self.ui.btn_go       .clicked.connect(self.start_progress_modal)

        # DEBUG
        self.ui.line_input.setText("./test/snd/duvet.mp3")
        self.ui.line_outDir.setText("./test/out")

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

    def start_progress_modal(self):
        # Validate input
        inFile = self.ui.line_input.text()
        outDir = self.ui.line_outDir.text()

        if not (inFile and outDir):
            errMsg = ("Empty fields", "Please select an input file and an output directory.")
        elif not os.path.isfile(inFile):
            errMsg = ("File not found", "The file doesn't exist.")
        elif "audio/" not in magic.from_file(inFile, mime=True):
            errMsg = ("Incorrect file format", "Please select an audio file.")
        else:
            dial = ModalProgress(self)
            dial.exec()
            return True

        QMessageBox.warning(self, errMsg[0], errMsg[1])
        return False

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())

