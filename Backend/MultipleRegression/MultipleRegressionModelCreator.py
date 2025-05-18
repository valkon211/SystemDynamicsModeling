import numpy as np
import pandas as pd

from Backend.Common.FeatureEngineer import FeatureEngineer
from Backend.Common.ModelType import ModelType
from Backend.Data.AnalyticsDataPreparer import AnalyticsDataPreparer
from Backend.MultipleRegression.MultipleRegressionModel import MultipleRegressionModel


class MultipleRegressionModelCreator:
    @staticmethod
    def create_model(X: pd.DataFrame, y: pd.DataFrame, model_type: ModelType) -> MultipleRegressionModel:
        relevant_features = FeatureEngineer.select_relevant_features(X, y)
        X_selected = X[relevant_features]
        X_transformed = AnalyticsDataPreparer.transform_x(X_selected, model_type)

        coefficients_dict = {}
        for column in y.columns:
            y_transformed = AnalyticsDataPreparer.transform_y(y[[column]], model_type)
            coef = np.linalg.pinv(X_transformed) @ y_transformed
            coefficients_dict[column] = coef.flatten()

        feature_names = AnalyticsDataPreparer.get_feature_names(X_selected, model_type)
        coefficients_df = pd.DataFrame(coefficients_dict, index=feature_names)

        return MultipleRegressionModel(
            coefficients=coefficients_df,
            features=relevant_features,
            model_type=model_type)