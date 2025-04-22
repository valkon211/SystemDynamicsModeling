import numpy as np
import pandas as pd

from Backend.Common.ModelType import ModelType
from Backend.Data.AnalyticsDataPreparer import AnalyticsDataPreparer
from Backend.RegressionModels.MultipleRegressionModel import MultipleRegressionModel


class MultipleRegressionModelCreator:
    @staticmethod
    def create_model(X: pd.DataFrame, y: pd.DataFrame, model_type: ModelType) -> MultipleRegressionModel:
        X_transformed = AnalyticsDataPreparer.transform_x(X, model_type)
        coefficients_dict = {}
        feature_names = AnalyticsDataPreparer.get_feature_names(X, model_type)

        for column in y.columns:
            y_transformed = AnalyticsDataPreparer.transform_y(y[[column]], model_type)
            coefficients_array = np.linalg.pinv(X_transformed) @ y_transformed
            coefficients_array = coefficients_array.flatten()
            coefficients_dict[column] = coefficients_array

        coefficients = pd.DataFrame(coefficients_dict, index=feature_names)

        return MultipleRegressionModel(coefficients, model_type)