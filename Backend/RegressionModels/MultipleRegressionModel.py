import pandas as pd

from Backend.Common.ModelType import ModelType
from Backend.Data.AnalyticsDataPreparer import AnalyticsDataPreparer


class MultipleRegressionModel:
    def __init__(self, coefficients: pd.DataFrame, model_type: ModelType):
        self.type = model_type
        self.coefficients = coefficients

    def predict(self, X: pd.DataFrame) -> pd.DataFrame:
        X_transformed = AnalyticsDataPreparer.transform_x(X, self.type)
        feature_names = AnalyticsDataPreparer.get_feature_names(X, self.type)
        X_transformed_df = pd.DataFrame(X_transformed, columns=feature_names, index=X.index)

        if not all(X_transformed_df.columns == self.coefficients.index):
            raise ValueError("Порядок признаков в X не соответствует порядку коэффициентов.")

        prediction = X_transformed_df.dot(self.coefficients)
        prediction = AnalyticsDataPreparer.inverse_transform_y(prediction, self.type)

        return prediction.round(4)

    def get_coefficients(self):
        return self.coefficients


