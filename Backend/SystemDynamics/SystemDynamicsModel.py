import numpy as np
import pandas as pd

from Backend.Common.ModelType import ModelType


class SystemDynamicsModel:
    def __init__(self, coefficients: np.ndarray, equation_type: ModelType):
        self.coefficients = coefficients
        self.equation_type = equation_type

    def predict(self, X: pd.DataFrame) -> pd.DataFrame:
        if self.equation_type == ModelType.Linear:
            return self._predict_linear(X)
        elif self.equation_type == ModelType.Quadratic:
            return self._predict_quadratic(X)
        elif self.equation_type == ModelType.Polynomial:
            return self._predict_polynomial(X)
        elif self.equation_type == ModelType.Exponential:
            return self._predict_exponential(X)
        else:
            raise ValueError(f"Неизвестный тип модели: {self.equation_type}")

    def _predict_linear(self, X: pd.DataFrame) -> pd.DataFrame:
        X_ = np.column_stack([np.ones(X.shape[0]), X.values])
        prediction = X_ @ self.coefficients
        return pd.DataFrame(prediction, columns=[f"y_{i+1}" for i in range(prediction.shape[1])] if prediction.ndim > 1 else ["y"], index=X.index)

    def _predict_quadratic(self, X: pd.DataFrame) -> pd.DataFrame:
        X_quad = np.column_stack([np.ones(X.shape[0]), X.values, X.values ** 2])
        prediction = X_quad @ self.coefficients
        return pd.DataFrame(prediction, columns=[f"y_{i}" for i in range(prediction.shape[1])] if prediction.ndim > 1 else ["y"], index=X.index)

    def _predict_polynomial(self, X: pd.DataFrame) -> pd.DataFrame:
        X_poly = [np.ones(X.shape[0])]
        for i in range(1, len(self.coefficients)):
            X_poly.append(np.power(X.values, i))
        X_ = np.column_stack(X_poly)
        prediction = X_ @ self.coefficients
        return pd.DataFrame(prediction, columns=[f"y_{i}" for i in range(prediction.shape[1])] if prediction.ndim > 1 else ["y"], index=X.index)

    def _predict_exponential(self, X: pd.DataFrame) -> pd.DataFrame:
        X_exp = np.column_stack([np.ones(X.shape[0]), X.values])
        return np.exp(X_exp @ self.coefficients)

