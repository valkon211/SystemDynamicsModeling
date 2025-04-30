from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget

from Frontend.UI.Ui_HomeScreen import Ui_HomeScreen


class HomeScreen(QWidget, Ui_HomeScreen):
    calculate_need = pyqtSignal()
    prediction_need = pyqtSignal()
    rules_need = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.calculate_model_btn.clicked.connect(self.calculate_need.emit)
        self.get_prediction_btn.clicked.connect(self.prediction_need.emit)
        self.rules_btn.clicked.connect(self.rules_need.emit)