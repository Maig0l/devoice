from time import sleep
from PyQt5.QtCore import QObject, pyqtSignal

class DebugWorker(QObject):
    _running = False
    finished = pyqtSignal(int)
    step     = pyqtSignal(int)
    # Message shown in progress bar.
    # %p% for progress int
    statMsg  = pyqtSignal(str)

    def __init__(self):
        QObject.__init__(self)

    def longTask(self):
        r = 10
        for x in range(r):
            if self._running:
                print(f"x = {x}")
                sleep(1)
                self.step.emit(((x+1) * 100) // r)
            else:
                return False
        return True

    def run(self, filename, outDir, model="demucs", stems2=False):
        self._running = True
        result = self.longTask()
        self.finished.emit(
                0 if result else 1
            )

    def stop(self):
        self.statMsg.emit("Stopping...")
        self._running = False
