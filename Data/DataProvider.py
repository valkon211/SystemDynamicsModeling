import pandas as pd
from Data.DataValidator import DataValidator


class DataProvider:
    def __init__(self, facts_path, targets_path):
        self.facts_path = facts_path
        self.targets_path = targets_path
        self.facts = None
        self.targets = None
        self.dataValidator = DataValidator

    def get_facts(self):
        return self.facts

    def get_targets(self):
        return self.targets

    def load_data(self):
        try:
            facts = self._load_file(self.facts_path)
            targets = self._load_file(self.targets_path)

            is_valid, message = self.dataValidator.validate(facts, targets)

            if not is_valid:
                raise Exception(message)

            facts.columns = [f"x{i + 1}" for i in range(facts.shape[1])]
            targets.columns = [f"y{i + 1}" for i in range(targets.shape[1])]

            self.facts = facts
            self.targets = targets

        except Exception as e:
            raise ImportError(f"Ошибка при загрузке данных: {e}")

    def _load_file(self, file_path):
        if file_path.endswith('.csv'):
            return pd.read_csv(file_path)
        elif file_path.endswith('.xlsx') or file_path.endswith('.xls'):
            return pd.read_excel(file_path)
        else:
            raise ValueError("Формат файла не поддерживается. Используйте CSV или Excel.")