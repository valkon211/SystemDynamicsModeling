import time

from PyQt5.QtWidgets import QWidget

from Frontend.UI.Ui_ProgressScreen import Ui_ProgressScreen


class ProgressScreen(QWidget, Ui_ProgressScreen):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def update_progress(self, value):
        time.sleep(1)
        self.progressBar.setValue(value)

    def append_log(self, message):
        self.log_te.append(message)