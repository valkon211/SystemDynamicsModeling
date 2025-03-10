import numpy as np
import pandas as pd
from pandas.core.interchange.dataframe_protocol import DataFrame

from RegressionModels.MultRegressionType import MultRegressionType


class RegressionPredictor:
    def predict(self, X: pd.DataFrame, model_type: MultRegressionType, coefficients: np.ndarray):
        X = X.to_numpy()  # Преобразуем DataFrame в numpy array

        if X.shape[1] + 1 == coefficients.shape[0]:
            X = np.hstack([np.ones((X.shape[0], 1)), X])

        if model_type == MultRegressionType.Linear:
            y_pred = self._predict_linear(X, coefficients)
        elif model_type == MultRegressionType.Polynomial:
            y_pred = self._predict_polynomial(X, coefficients)
        elif model_type == MultRegressionType.Exponential:
            y_pred = self._predict_exponential(X, coefficients)
        elif model_type == MultRegressionType.Quadratic:
            y_pred = self._predict_quadratic(X, coefficients)
        else:
            raise ValueError(f"Неизвестный тип модели: {model_type}")

        if y_pred.ndim == 1:
            y_pred = y_pred.reshape(-1, 1)

        # Создаём DataFrame с нужными названиями колонок
        column_names = [f"y{i + 1}" for i in range(y_pred.shape[1])]
        return pd.DataFrame(y_pred, columns=column_names)

    def _predict_linear(self, X, coefficients):
        """Предсказание для линейной регрессии: y = b0 + b1*x1 + b2*x2 + ..."""
        y_pred = X @ coefficients  # X * theta

        # Создаём DataFrame с корректными заголовками колонок
        column_names = [f"y{i + 1}" for i in range(y_pred.shape[1] if y_pred.ndim > 1 else 1)]
        return pd.DataFrame(y_pred, columns=column_names)

    def _predict_polynomial(self, X, coefficients):
        """Предсказание для полиномиальной регрессии (2-й степени): y = b0 + b1*x + b2*x^2."""
        X_poly = np.c_[np.ones((X.shape[0], 1)), X, X**2]
        return X_poly @ coefficients

    def _predict_exponential(self, X, coefficients):
        """Предсказание для экспоненциальной регрессии: y = b0 * exp(b1*x)."""
        linear_combination = X @ coefficients
        y_pred = np.exp(linear_combination)

        # Создаём DataFrame с корректными заголовками колонок
        column_names = [f"y{i + 1}" for i in range(y_pred.shape[1] if y_pred.ndim > 1 else 1)]
        return pd.DataFrame(y_pred, columns=column_names)

    def _predict_quadratic(self, X, coefficients):
        """Предсказание для квадратичной регрессии: y = b0 + b1*x + b2*x^2."""
        X_quad = np.c_[np.ones((X.shape[0], 1)), X, X**2]
        return X_quad @ coefficients
