import enum

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QFileDialog

from Backend.Common.ModelType import ModelType
from Frontend.Services.FileType import FileType
from Frontend.UI.Ui_InputPredictionScreen import Ui_InputPredictionScreen
from Frontend.Widgets.AddModelConfigurationForm import AddModelConfigurationForm
from Frontend.Widgets.ImportModelConfigurationWidget import ImportModelConfigurationWidget


class InputModelType(enum.Enum):
    FromFile = 0
    Add = 1

class InputPredictionScreen(QWidget, Ui_InputPredictionScreen):
    start_calculation_add = pyqtSignal(str, str, list, ModelType, bool)
    start_calculation_import = pyqtSignal(str, str, bool)
    back_to_home = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.file_path_x = ""
        self.file_path_coef = ""

        self.input_type = None

        self.add_model_conf_widget = AddModelConfigurationForm()
        self.import_model_conf_widget = ImportModelConfigurationWidget()

        self.model_conf_add_btn.clicked.connect(lambda: self._show_add_model_conf(InputModelType.Add))
        self.model_conf_import_btn.clicked.connect(lambda: self._show_add_model_conf(InputModelType.FromFile))

        self.add_x_path_btn.clicked.connect(self.select_x_file)
        self.calculate_btn.clicked.connect(self.calculate)
        self.back_btn.clicked.connect(self.back_to_home.emit)

    def select_x_file(self):
        path = self._open_file_dialog(FileType.Table)
        self.file_path_x_le.setText(path)
        self.file_path_x = path

    def calculate(self):
        if self.input_type is InputModelType.FromFile:
            json_path = self.import_model_conf_widget.json_file_path
            if json_path and self.file_path_x:
                if self.sd_simple_rbtn.isChecked():
                    self.start_calculation_import.emit(self.file_path_x, json_path, False)
                if self.sd_extended_rbtn.isChecked():
                    self.start_calculation_import.emit(self.file_path_x, json_path, True)

        if self.input_type is InputModelType.Add:
            data = self.add_model_conf_widget.get_form_result()

            if data and self.file_path_x and data.CoefficientFilePath and data.FeaturesList and data.ModelType:
                if self.sd_simple_rbtn.isChecked():
                    self.start_calculation_add.emit(
                        self.file_path_x,
                        data.CoefficientFilePath,
                        data.FeaturesList,
                        data.ModelType,
                        False
                    )

                if self.sd_extended_rbtn.isChecked():
                    self.start_calculation_add.emit(
                        self.file_path_x,
                        data.CoefficientFilePath,
                        data.FeaturesList,
                        data.ModelType,
                        True
                    )


    def _open_file_dialog(self, file_types: str):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите файл",
            "",
            f"{file_types}"
        )
        if file_name:
            return file_name

    def _show_add_model_conf(self, type: InputModelType):
        if type is InputModelType.Add:
            self.model_config_layout.removeWidget(self.import_model_conf_widget)
            self.import_model_conf_widget.hide()
            self.model_config_layout.addWidget(self.add_model_conf_widget)
            self.add_model_conf_widget.show()

            self.input_type = InputModelType.Add

        if type is InputModelType.FromFile:
            self.model_config_layout.removeWidget(self.add_model_conf_widget)
            self.add_model_conf_widget.hide()
            self.model_config_layout.addWidget(self.import_model_conf_widget)
            self.import_model_conf_widget.show()

            self.input_type = InputModelType.FromFile