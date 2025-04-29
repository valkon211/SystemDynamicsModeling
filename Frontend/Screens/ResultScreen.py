import pandas as pd
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QMessageBox, QFileDialog

from Backend.MainService import MainService
from Frontend.UI.Ui_ResultScreen import Ui_ResultScreen


class ResultScreen(QWidget, Ui_ResultScreen):
    back_to_main = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.result_df = None

        self.export_btn.clicked.connect(self.export_to_excel)
        self.back_btn.clicked.connect(self.back_to_main.emit)

    def set_func_name(self, name):
        self.result_lbl.setText(name)

    def set_dataframe(self, df: pd.DataFrame):
        self.result_df = df
        self.table_result.clear()
        self.table_result.setRowCount(len(df))
        self.table_result.setColumnCount(len(df.columns))
        self.table_result.setHorizontalHeaderLabels(df.columns)

        for i in range(len(df)):
            for j in range(len(df.columns)):
                item = QTableWidgetItem(str(df.iloc[i, j]))
                self.table_result.setItem(i, j, item)

        self.table_result.resizeColumnsToContents()


    def export_to_excel(self):
        if self.result_df is None:
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Сохранить файл",
            "",
            "Excel Files (*.xlsx);"
        )
        if file_path:
            try:
                MainService.export_to_excel(self.result_df, file_path)
                QMessageBox.information(
                    self,
                    "Успех",
                    f"Файл успешно сохранён:\n{file_path}"
                )
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Ошибка",
                    f"Не удалось сохранить файл:\n{str(e)}"
                )