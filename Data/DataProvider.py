import pandas as pd
from Data.DataValidator import DataValidator


class DataProvider:
    def __init__(self, facts_path, targets_path):
        self.facts_path = facts_path
        self.targets_path = targets_path
        self.facts = None
        self.targets = None
        self.X = None
        self.y = None

        self.dataValidator = DataValidator

    def load_data(self):
        try:
            # Загружаем факты
            facts = self._load_file(self.facts_path)
            # Загружаем целевые показатели
            targets = self._load_file(self.targets_path)

            is_valid, message = self.dataValidator.validate(facts, targets)

            if not is_valid:
                raise Exception(message)

            self.facts = facts
            self.targets = targets

            # Преобразуем в numpy массивы
            self.X = self.facts.values
            self.y = self.targets.values

        except Exception as e:
            print(f"Ошибка при загрузке данных: {e}")
            self.X, self.y = None, None


    def _load_file(self, file_path):
        if file_path.endswith('.csv'):
            return pd.read_csv(file_path)
        elif file_path.endswith('.xlsx') or file_path.endswith('.xls'):
            return pd.read_excel(file_path)
        else:
            raise ValueError("Формат файла не поддерживается. Используйте CSV или Excel.")

    def get_features(self):
        return self.X

    def get_targets(self):
        return self.y

    def get_facts_df(self):
        return self.facts

    def get_targets_df(self):
        return self.targets