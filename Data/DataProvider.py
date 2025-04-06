import os
import datetime
import pandas as pd


class DataProvider:
    @staticmethod
    def load_file(file_path: str):
        if file_path.endswith('.csv'):
            return pd.read_csv(file_path)
        elif file_path.endswith('.xlsx') or file_path.endswith('.xls'):
            return pd.read_excel(file_path)
        else:
            raise ValueError("Формат файла не поддерживается. Используйте CSV или Excel.")

    @staticmethod
    def save_to_excel(df: pd.DataFrame, filename: str = "output", folder: str = "reports"):
        os.makedirs(folder, exist_ok=True)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        result_filename = f"{filename}_{timestamp}.xlsx"
        filepath = os.path.join(folder, result_filename)
        df.to_excel(filepath, index=False)