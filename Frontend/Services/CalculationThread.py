from PyQt5.QtCore import QThread, pyqtSignal

from Backend.Common.CalculationResult import CalculationResult


class CalculationThread(QThread):
    progress_update = pyqtSignal(int)
    calculation_done = pyqtSignal(CalculationResult)
    log_update = pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def update_progress(self, value):
        self.progress_update.emit(value)

    def update_log(self, message):
        self.log_update.emit(message)