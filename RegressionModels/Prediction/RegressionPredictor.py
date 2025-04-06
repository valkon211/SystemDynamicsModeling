import numpy as np
import pandas as pd

from RegressionModels.MultRegressionType import MultRegressionType


class RegressionPredictor:
    def predict(self, X: pd.DataFrame, theta: np.ndarray, model_type: MultRegressionType) -> pd.DataFrame:
        if model_type == MultRegressionType.Linear:
            prediction = self._predict_linear(X, theta)
        elif model_type == MultRegressionType.Polynomial:
            prediction = self._predict_polynomial(X, theta)
        elif model_type == MultRegressionType.Exponential:
            prediction = self._predict_exponential(X, theta)
        elif model_type == MultRegressionType.Quadratic:
            prediction = self._predict_quadratic(X, theta)
        else:
            raise ValueError(f"Неизвестный тип модели: {model_type}")

        return prediction.round(4)

    def _predict_linear(self, X: pd.DataFrame, theta):
        """Предсказание для линейной регрессии: y = b0 + b1*x1 + b2*x2 + ..."""
        X_extended = np.column_stack((np.ones(X.shape[0]), X))
        return X_extended @ theta

    def _predict_polynomial(self, X: pd.DataFrame, theta, degree = 2):
        """Предсказание для полиномиальной регрессии (2-й степени): y = b0 + b1*x + b2*x^2."""
        X_with_intercept = pd.concat([pd.Series(1, index=X.index, name="Intercept"), X], axis=1)
        X_matrix = X_with_intercept.to_numpy()
        theta_matrix = theta.to_numpy()
        predictions = X_matrix @ theta_matrix

        return pd.DataFrame(predictions, columns=theta.columns, index=X.index)

    def _predict_exponential(self, X: pd.DataFrame, theta):
        """Предсказание для экспоненциальной регрессии: y = b0 * exp(b1*x)."""
        X_extended = np.column_stack((np.ones(X.shape[0]), X))
        return np.exp(X_extended @ theta)

    def _predict_quadratic(self, X: pd.DataFrame, theta) -> pd.DataFrame:
        """Предсказание для квадратичной регрессии: y = b0 + b1*x + b2*x^2."""
        X_np = np.array(X)
        X_extended = np.column_stack((X_np, X_np[:, 1:] ** 2))
        return X_extended @ theta
