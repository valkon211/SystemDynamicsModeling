import numpy as np
import pandas as pd

from Backend.Common.FeatureEngineer import FeatureEngineer
from Backend.Common.ModelType import ModelType
from Backend.Data.AnalyticsDataPreparer import AnalyticsDataPreparer
from Backend.MultipleRegression.MultipleRegressionModel import MultipleRegressionModel


class MultipleRegressionModelCreator:
    @staticmethod
    def create_model(X: pd.DataFrame, y: pd.DataFrame, model_type: ModelType) -> MultipleRegressionModel:
        feature_engineer = FeatureEngineer()

        X_selected = feature_engineer.generate_and_select_features(X)
        X_transformed = AnalyticsDataPreparer.transform_x(X_selected, model_type)
        feature_names = AnalyticsDataPreparer.get_feature_names(X_selected, model_type)

        coefficients_dict = {}

        for column in y.columns:
            y_transformed = AnalyticsDataPreparer.transform_y(y[[column]], model_type)
            coefficients_array = np.linalg.pinv(X_transformed) @ y_transformed
            coefficients_array = coefficients_array.flatten()
            coefficients_dict[column] = coefficients_array

        coefficients = pd.DataFrame(coefficients_dict, index=feature_names)

        return MultipleRegressionModel(coefficients, model_type, feature_engineer)