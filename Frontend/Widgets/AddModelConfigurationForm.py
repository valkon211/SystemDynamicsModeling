from dataclasses import dataclass

from PyQt5.QtWidgets import QWidget, QFileDialog

from Backend.Common.ModelType import ModelType
from Frontend.Services.FileType import FileType
from Frontend.UI.Ui_AddModelConfigurationForm import Ui_AddModelConfigurationForm

@dataclass
class AddModelFormResult:
    CoefficientFilePath: None
    ModelType: None

class AddModelConfigurationForm(QWidget, Ui_AddModelConfigurationForm):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.add_coef_path_btn.clicked.connect(self.select_coef_file)

    def get_form_result(self):
        return AddModelFormResult(
            CoefficientFilePath=self.coefficients_le.text(),
            ModelType=self._get_model_type()
        )

    def _get_model_type(self):
        if self.func_lin_rbtn.isChecked():
            return ModelType.Linear
        if self.func_exp_rbtn.isChecked():
            return ModelType.Exponential
        if self.func_quadro_rbtn.isChecked():
            return ModelType.Quadratic

        return None

    def select_coef_file(self):
        path = self._open_file_dialog(FileType.Table)
        self.coefficients_le.setText(path)

    def _open_file_dialog(self, file_types: str):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите файл",
            "",
            f"{file_types}"
        )
        if file_name:
            return file_name