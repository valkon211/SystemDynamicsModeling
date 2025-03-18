from itertools import combinations_with_replacement

import numpy as np
import pandas as pd

from RegressionModels.MultRegressionType import MultRegressionType


class RegressionPredictor:
    def predict(self, X: pd.DataFrame, theta: np.ndarray, model_type: MultRegressionType):
        if model_type == MultRegressionType.Linear:
            y_pred = self._predict_linear(X, theta)
        elif model_type == MultRegressionType.Polynomial:
            y_pred = self._predict_polynomial(X, theta)
        elif model_type == MultRegressionType.Exponential:
            y_pred = self._predict_exponential(X, theta)
        elif model_type == MultRegressionType.Quadratic:
            y_pred = self._predict_quadratic(X, theta)
        else:
            raise ValueError(f"Неизвестный тип модели: {model_type}")

        return y_pred

    def _predict_linear(self, X: pd.DataFrame, theta):
        """Предсказание для линейной регрессии: y = b0 + b1*x1 + b2*x2 + ..."""
        X_extended = np.column_stack((np.ones(X.shape[0]), X))
        return X_extended @ theta

    def _predict_polynomial(self, X: pd.DataFrame, theta):
        """Предсказание для полиномиальной регрессии (2-й степени): y = b0 + b1*x + b2*x^2."""
        X_poly = self._prepare_polynomial_features(X, degree=2)
        return X_poly @ theta

    def _predict_exponential(self, X: pd.DataFrame, theta):
        """Предсказание для экспоненциальной регрессии: y = b0 * exp(b1*x)."""
        X_extended = np.column_stack((np.ones(X.shape[0]), X))
        return np.exp(X_extended @ theta)

    def _predict_quadratic(self, X: pd.DataFrame, theta):
        """Предсказание для квадратичной регрессии: y = b0 + b1*x + b2*x^2."""
        X_extended = np.column_stack((np.ones(X.shape[0]), X, X**2))
        return X_extended @ theta

    def _prepare_polynomial_features(self, X: pd.DataFrame, degree):
        poly_features = [X]
        for d in range(2, degree + 1):
            for cols in combinations_with_replacement(X.columns, d):
                poly_features.append(X[list(cols)].prod(axis=1))
        X_poly = pd.concat(poly_features, axis=1)

        return np.column_stack((np.ones(X_poly.shape[0]), X_poly))
