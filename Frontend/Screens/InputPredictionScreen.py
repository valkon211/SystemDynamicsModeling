from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QFileDialog

from Backend.Common.ModelType import ModelType
from Frontend.UI.Ui_InputPredictionScreen import Ui_InputPredictionScreen


class InputPredictionScreen(QWidget, Ui_InputPredictionScreen):
    start_calculation = pyqtSignal(str, str, list, ModelType)
    back_to_home = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.file_path_x = ""
        self.file_path_coef = ""

        self.add_x_path_btn.clicked.connect(self.select_x_file)
        self.add_coef_path_btn.clicked.connect(self.select_coef_file)
        self.calculate_btn.clicked.connect(self.calculate)
        self.back_btn.clicked.connect(self.back_to_home.emit)

    def select_x_file(self):
        path = self._open_file_dialog()
        self.file_path_x_le.setText(path)
        self.file_path_x = path

    def select_coef_file(self):
        path = self._open_file_dialog()
        self.coefficients_le.setText(path)
        self.file_path_coef = path

    def calculate(self):
        features = self.get_features()
        model_type = self.get_model_type()
        if self.file_path_x and self.file_path_coef and model_type:
            self.start_calculation.emit(self.file_path_x, self.file_path_coef, features, model_type)

    def get_features(self) -> list[str]:
        features_text = self.features_le.text()

        if features_text == "":
            return []

        return features_text.split(',')

    def get_model_type(self):
        if self.func_lin_rbtn.isChecked():
            return ModelType.Linear
        if self.func_exp_rbtn.isChecked():
            return ModelType.Exponential
        if self.func_quadro_rbtn.isChecked():
            return ModelType.Quadratic

        return None

    def _open_file_dialog(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите файл",
            "",
            "Таблицы (*.xls *.xlsx *.csv)"
        )
        if file_name:
            return file_name