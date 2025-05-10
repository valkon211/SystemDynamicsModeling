from PyQt5.QtWidgets import QWidget, QFileDialog

from Frontend.Services.FileType import FileType
from Frontend.UI.Ui_ImportModelConfigurationWidget import Ui_ImportModelConfigurationWidget


class ImportModelConfigurationWidget(QWidget, Ui_ImportModelConfigurationWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.json_file_path = ""

        self.add_model_path_btn.clicked.connect(self.select_file)

    def select_file(self):
        path = self._open_file_dialog(FileType.Json)
        self.file_path_model_le.setText(path)

        self.json_file_path = path

    def _open_file_dialog(self, file_types: str):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите файл",
            "",
            f"{file_types}"
        )
        if file_name:
            return file_name
