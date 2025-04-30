import numpy as np
import pandas as pd

from Backend.Common.FeatureEngineer import FeatureEngineer
from Backend.Common.ModelType import ModelType
from Backend.Data.AnalyticsDataPreparer import AnalyticsDataPreparer
from Backend.MultipleRegression.MultipleRegressionModel import MultipleRegressionModel


class MultipleRegressionModelCreator:
    @staticmethod
    def create_model(X: pd.DataFrame, y: pd.DataFrame, model_type: ModelType) -> MultipleRegressionModel:
        # 1. Генерация признаков и отбор
        X_features = FeatureEngineer.generate_features(X)
        relevant_features = FeatureEngineer.select_relevant_features(X_features)
        X_selected = X_features[relevant_features]

        # 2. Преобразование признаков
        X_transformed = AnalyticsDataPreparer.transform_x(X_selected, model_type)

        # 3. Получаем имена фичей (в том порядке, в котором они идут в transform_x)
        feature_names = AnalyticsDataPreparer.get_feature_names(X_selected, model_type)

        # 4. Расчёт коэффициентов
        coefficients_dict = {}
        for column in y.columns:
            y_transformed = AnalyticsDataPreparer.transform_y(y[[column]], model_type)
            coef = np.linalg.pinv(X_transformed) @ y_transformed
            coefficients_dict[column] = coef.flatten()

        # 5. Создаём DataFrame с индексами — названиями фичей
        coefficients_df = pd.DataFrame(coefficients_dict, index=feature_names)

        return MultipleRegressionModel(coefficients_df, relevant_features, model_type)