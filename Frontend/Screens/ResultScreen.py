import pandas as pd
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QMessageBox, QFileDialog

from Backend.Common.CalculationResult import CalculationResult
from Backend.MainService import MainService
from Frontend.UI.Ui_ResultScreen import Ui_ResultScreen


class ResultScreen(QWidget, Ui_ResultScreen):
    back_to_home = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.data: CalculationResult = None

        self.export_excel_btn.clicked.connect(self.export_to_excel)
        self.export_json_btn.clicked.connect(self.export_to_json)
        self.back_btn.clicked.connect(self.back_to_home.emit)

    def set_data(self, data: CalculationResult):
        self.data = data

        self._set_func_name(data.model_type)
        self._set_relevant_features(data.relevant_features)
        self._set_equations(data.equations)
        self._set_dataframe(data.result_df)

        if data.json_data is None:
            self.export_json_btn.setHidden(True)

    def _set_func_name(self, name):
        self.result_lbl.setText(name)

    def _set_relevant_features(self, features: list[str]):
        if features:
            self.relevant_features_le.setText(', '.join(features))

    def _set_equations(self, equations: dict[str, str]):
        for equation in equations.values():
            self.equations_te.append(equation)

    def _set_dataframe(self, df: pd.DataFrame):
        self.result_df = df
        self.table_result.clear()
        self.table_result.setRowCount(len(df))
        self.table_result.setColumnCount(len(df.columns))
        self.table_result.setHorizontalHeaderLabels(df.columns)
        self.table_result.setVerticalHeaderLabels(df.index.tolist())

        for i in range(len(df)):
            for j in range(len(df.columns)):
                item = QTableWidgetItem(str(df.iloc[i, j]))
                self.table_result.setItem(i, j, item)

        self.table_result.resizeColumnsToContents()


    def export_to_excel(self):
        if self.data.result_df is None:
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Сохранить файл",
            "",
            "Excel Files (*.xlsx);"
        )
        if file_path:
            try:
                MainService.export_to_excel(self.data.result_df, file_path)
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

    def export_to_json(self):
        if self.data.json_data is None:
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Сохранить файл",
            "",
            "JSON (*.json)"
        )
        if file_path:
            try:
                MainService.export_to_json(self.data.json_data, file_path)
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