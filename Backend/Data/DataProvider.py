import json

import pandas as pd

class DataProvider:
    @staticmethod
    def load_file(file_path: str, index_in_first: bool = False):
        if file_path.endswith('.csv'):
            if index_in_first:
                return pd.read_csv(file_path, index_col=0)
            return pd.read_csv(file_path)
        elif file_path.endswith('.xlsx') or file_path.endswith('.xls'):
            if index_in_first:
                return pd.read_excel(file_path, index_col=0)
            return pd.read_excel(file_path)
        else:
            raise ValueError("Формат файла не поддерживается. Используйте CSV или Excel.")

    @staticmethod
    def save_to_excel(df: pd.DataFrame, filepath: str = None):
        if filepath is None:
            filepath = "output.xlsx"

        df.to_excel(filepath)

    @staticmethod
    def save_to_json(data, filepath: str = None):
        if filepath is None:
            filepath = "output.json"
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    @staticmethod
    def read_json(filepath: str):
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data