import pandas as pd

from Backend.Common.ModelType import ModelType
from Backend.Data.AnalyticsDataPreparer import AnalyticsDataPreparer


class MultipleRegressionModel:
    def __init__(self, coefficients: pd.DataFrame, features: list[str], model_type: ModelType):
        self.model_type = model_type
        self.coefficients = coefficients
        self.features = features

    def predict(self, X: pd.DataFrame) -> pd.DataFrame:
        X_selected = X[self.features]
        X_transformed = AnalyticsDataPreparer.transform_x(X_selected, self.model_type)
        y_pred = X_transformed @ self.coefficients
        y_pred = AnalyticsDataPreparer.inverse_transform_y(y_pred, self.model_type)

        return y_pred.round(4)