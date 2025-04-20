import pandas as pd

from Backend.Data.DataProvider import DataProvider
from Backend.Data.DataValidator import DataValidator
from Backend.Common.ModelType import ModelType


class AnalyticsDataProvider:
    def __init__(self, facts_path: str, targets_path: str):
        self.facts_path = facts_path
        self.targets_path = targets_path
        self.facts = None
        self.targets = None
        self.predictions = {}

        self.dataValidator = DataValidator
        self.dataProvider = DataProvider

        self._load_data()

    def get_facts(self):
        return self.facts

    def get_targets(self):
        return self.targets

    def get_correlation_matrix(self):
        combined_data = pd.concat([self.facts, self.targets], axis=1)
        return combined_data.corr().round(4)

    def get_predictions(self) -> dict:
        return self.predictions

    def get_merged_predictions(self) -> pd.DataFrame:
        result = pd.DataFrame()

        for col in self.targets.columns:
            # Добавляем истинные значения
            result[f"{col}_true"] = self.targets[col].values

            # Добавляем предсказания каждой модели
            for model_name, pred_df in self.predictions.items():
                result[f"{col}_{model_name.name}"] = pred_df[col].values

        return result

    def add_prediction(self, prediction: pd.DataFrame, model_type: ModelType):
        self.predictions[model_type] = prediction

    def _load_data(self):
        try:
            facts = self.dataProvider.load_file(self.facts_path)
            targets = self.dataProvider.load_file(self.targets_path)

            is_valid, message = self.dataValidator.validate(facts, targets)

            if not is_valid:
                raise Exception(message)

            facts.columns = [f"x{i + 1}" for i in range(facts.shape[1])]
            targets.columns = [f"y{i + 1}" for i in range(targets.shape[1])]

            self.facts = facts
            self.targets = targets

        except Exception as e:
            raise ImportError(f"Ошибка при загрузке данных: {e}")