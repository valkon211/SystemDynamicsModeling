from PyQt5.QtWidgets import QWidget

from Frontend.UI.Ui_HomeScreen import Ui_HomeScreen


class HomeScreen(QWidget, Ui_HomeScreen):
    def __init__(self):
        super().__init__()
        self.setupUi(self)