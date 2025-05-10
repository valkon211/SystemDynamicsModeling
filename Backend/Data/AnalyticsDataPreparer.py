import itertools

import numpy as np
import pandas as pd

from Backend.Common.ModelType import ModelType


class AnalyticsDataPreparer:
    min_variance_threshold = 1e-5
    degree = 3

    @staticmethod
    def transform_x(X: pd.DataFrame, model_type: ModelType) -> np.ndarray:
        if model_type == ModelType.Linear or model_type == ModelType.Exponential:
            return np.column_stack([np.ones(X.shape[0]), X.values])
        elif model_type == ModelType.Quadratic:
            return np.column_stack([np.ones(X.shape[0]), X.values, X.values ** 2])
        else:
            raise ValueError(f"Неизвестный тип модели: {model_type}")

    @staticmethod
    def transform_y(y: pd.DataFrame, model_type: ModelType) -> np.ndarray:
        if model_type == ModelType.Exponential:
            return np.log(y.values)
        return y.values

    @staticmethod
    def inverse_transform_y(y: pd.DataFrame, model_type: ModelType) -> pd.DataFrame:
        if model_type == ModelType.Exponential:
            result = pd.DataFrame(index=y.index, columns=y.columns)
            for column in y.columns:
                if model_type == ModelType.Exponential:
                    result[column] = np.exp(y[column])
            return result

        return y

    @staticmethod
    def get_feature_names(X: pd.DataFrame, model_type: ModelType) -> list[str]:
        if model_type == ModelType.Linear or model_type == ModelType.Exponential:
            feature_names = ['Intercept'] + list(X.columns)
        elif model_type == ModelType.Quadratic:
            feature_names = ['Intercept'] + list(X.columns) + [f"{col}²" for col in X.columns]
        else:
            raise ValueError(f"Unsupported model type: {model_type}")

        return feature_names