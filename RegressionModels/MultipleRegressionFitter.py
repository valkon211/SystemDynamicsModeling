import numpy as np
import pandas as pd

from ModelType import ModelType

class MultipleRegressionFitter:
    def __init__(self, X: pd.DataFrame, y: pd.DataFrame):
        self.X = X
        self.y = y

    def get_theta(self, model_type: ModelType):
        if model_type == ModelType.Linear:
            theta = self._fit_linear()
        elif model_type == ModelType.Polynomial:
            theta = self._fit_polynomial()
        elif model_type == ModelType.Exponential:
            theta = self._fit_exponential()
        elif model_type == ModelType.Quadratic:
            theta = self._fit_quadratic()
        else:
            raise ValueError(f"Неизвестный тип модели: {model_type}")

        return theta

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
        X_with_intercept = pd.concat([pd.Series(1, index=self.X.index, name="Intercept"), self.X], axis=1)
        X_matrix = X_with_intercept.to_numpy()
        Y_matrix = self.y.to_numpy()

        theta = np.linalg.inv(X_matrix.T @ X_matrix) @ X_matrix.T @ Y_matrix
        return pd.DataFrame(theta, columns=self.y.columns, index=X_with_intercept.columns)

    def _fit_quadratic(self):
        X_np = np.array(self.X)
        X_quad = np.column_stack((X_np, X_np[:, 1:] ** 2))  # Добавляем квадратичные признаки
        theta = np.linalg.inv(X_quad.T @ X_quad) @ X_quad.T @ np.array(self.y)

        return pd.DataFrame(theta, columns=[f"y{i + 1}" for i in range(self.y.shape[1])])
