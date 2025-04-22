import numpy as np
import pandas as pd

from Backend.Common.ModelType import ModelType


class AnalyticsDataPreparer:
    @staticmethod
    def transform_x(X: pd.DataFrame, model_type: ModelType) -> np.ndarray:
        degree = 2

        if model_type == ModelType.Linear:
            return np.column_stack([np.ones(X.shape[0]), X.values])
        elif model_type == ModelType.Quadratic:
            return np.column_stack([np.ones(X.shape[0]), X.values, X.values ** 2])
        elif model_type == ModelType.Polynomial:
            X_poly = [np.ones(X.shape[0])]
            for i in range(1, degree + 1):
                X_poly.append(np.power(X.values, i))
            return np.column_stack(X_poly)
        elif model_type == ModelType.Exponential:
            return np.column_stack([np.ones(X.shape[0]), X.values])
        else:
            raise ValueError(f"Неизвестный тип модели: {model_type}")

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
    def transform_y(y: pd.DataFrame, model_type: ModelType) -> np.ndarray:
        if model_type == ModelType.Exponential:
            return np.log(y.values)
        return y.values

    @staticmethod
    def get_feature_names(X: pd.DataFrame, model_type: ModelType) -> list:
        degree = 2
        if model_type == ModelType.Linear:
            return ['Intercept'] + list(X.columns)
        elif model_type == ModelType.Quadratic:
            return ['Intercept'] + list(X.columns) + [f"{col}²" for col in X.columns]
        elif model_type == ModelType.Polynomial:
            names = ['Intercept']
            for i in range(1, degree + 1):
                names += [f"{col}^{i}" for col in X.columns]
            return names
        elif model_type == ModelType.Exponential:
            return ['Intercept'] + list(X.columns)
        else:
            raise ValueError(f"Неизвестный тип модели: {model_type}")