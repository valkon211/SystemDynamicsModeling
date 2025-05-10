import pandas as pd

from Backend.Common.FeatureEngineer import FeatureEngineer
from Backend.Common.ModelType import ModelType
from Backend.Data.AnalyticsDataPreparer import AnalyticsDataPreparer


class MultipleRegressionModel:
    def __init__(self, coefficients: pd.DataFrame, features: list[str], model_type: ModelType):
        self.model_type = model_type
        self.coefficients = coefficients
        self.features = features

    def predict(self, X: pd.DataFrame) -> pd.DataFrame:
        if self.features == [] or self.features is None:
            self.features = self.coefficients.index.difference(['Intercept']).tolist()

        X_prepared = FeatureEngineer.prepare_for_prediction(X, self.features)

        X_features = FeatureEngineer.generate_features(X)
        X_selected = X_features[self.features]

        X_transformed = AnalyticsDataPreparer.transform_x(X, self.model_type)
        y_pred = X_transformed @ self.coefficients
        y_pred = AnalyticsDataPreparer.inverse_transform_y(y_pred, self.model_type)

        return y_pred.round(4)