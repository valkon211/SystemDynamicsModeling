from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QFileDialog

from Frontend.UI.Ui_InputCalculationScreen import Ui_InputCalculationScreen


class InputCalculationScreen(QWidget, Ui_InputCalculationScreen):
    start_calculation = pyqtSignal(str, str)
    back_to_home = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.file_path_x = ""
        self.file_path_y = ""

        self.add_x_path_btn.clicked.connect(self.select_x_file)
        self.add_y_path_btn.clicked.connect(self.select_y_file)
        self.calculate_btn.clicked.connect(self.calculate)
        self.back_btn.clicked.connect(self.back_to_home.emit)

    def select_x_file(self):
        path = self._open_file_dialog()
        self.file_path_x_le.setText(path)
        self.file_path_x = path

    def select_y_file(self):
        path = self._open_file_dialog()
        self.file_path_y_le.setText(path)
        self.file_path_y = path

    def calculate(self):
        if self.file_path_x and self.file_path_y:
            self.start_calculation.emit(self.file_path_x, self.file_path_y)

    def _open_file_dialog(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите файл",
            "",
            "Таблицы (*.xls *.xlsx *.csv)"
        )
        if file_name:
            return file_name