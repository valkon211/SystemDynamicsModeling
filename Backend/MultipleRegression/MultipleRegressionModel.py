import pandas as pd

from Backend.Common.FeatureEngineer import FeatureEngineer
from Backend.Common.ModelType import ModelType
from Backend.Data.AnalyticsDataPreparer import AnalyticsDataPreparer


class MultipleRegressionModel:
    def __init__(self, coefficients: pd.DataFrame, model_type: ModelType, feature_engineer: FeatureEngineer):
        self.type = model_type
        self.coefficients = coefficients
        self.feature_engineer = feature_engineer

    def predict(self, X: pd.DataFrame) -> pd.DataFrame:
        # 1. Генерация полных признаков (включая взаимодействия)
        X_with_features = self.feature_engineer.prepare_features(X)

        # 2. Оставляем только релевантные признаки, которые выбрали при обучении
        X_prepared = X_with_features[self.feature_engineer.relevant_features]

        # 3. Применяем все нужные трансформации
        X_transformed = AnalyticsDataPreparer.transform_x(X_prepared, self.type)

        prediction = X_transformed @ self.coefficients
        prediction = AnalyticsDataPreparer.inverse_transform_y(prediction, self.type)

        return prediction.round(4)

