from itertools import combinations_with_replacement

import numpy as np
import pandas as pd

from RegressionModels.MultRegressionType import MultRegressionType


class MultipleRegressionCalculator:
    def __init__(self, X: pd.DataFrame, y: pd.DataFrame):
        self.X = X
        self.y = y

    def get_theta(self, model_type: MultRegressionType):
        if model_type == MultRegressionType.Linear:
            theta = self._fit_linear()
        elif model_type == MultRegressionType.Polynomial:
            theta = self._fit_polynomial()
        elif model_type == MultRegressionType.Exponential:
            theta = self._fit_exponential()
        elif model_type == MultRegressionType.Quadratic:
            theta = self._fit_quadratic()
        else:
            raise ValueError(f"Неизвестный тип модели: {model_type}")

        return theta

    def _prepare_polynomial_features(self, degree):
        poly_features = [self.X]
        for d in range(2, degree + 1):
            for cols in combinations_with_replacement(self.X.columns, d):
                poly_features.append(self.X[list(cols)].prod(axis=1))
        X_poly = pd.concat(poly_features, axis=1)
        return np.column_stack((np.ones(X_poly.shape[0]), X_poly))

    def _fit_linear(self):
        X_extended = np.column_stack((np.ones(self.X.shape[0]), self.X))
        theta = np.linalg.inv(X_extended.T @ X_extended) @ X_extended.T @ self.y
        return theta

    def _fit_exponential(self):
        y_log = np.log(self.y)
        X_extended = np.column_stack((np.ones(self.X.shape[0]), self.X))
        theta = np.linalg.inv(X_extended.T @ X_extended) @ X_extended.T @ y_log
        return np.exp(theta)

    def _fit_polynomial(self, degree=2):
        X_poly = self._prepare_polynomial_features(degree)
        theta = np.linalg.inv(X_poly.T @ X_poly) @ X_poly.T @ self.y
        return theta

    def _fit_quadratic(self):
        X_extended = np.column_stack((np.ones(self.X.shape[0]), self.X, self.X ** 2))
        theta = np.linalg.inv(X_extended.T @ X_extended) @ X_extended.T @ self.y

        return theta
