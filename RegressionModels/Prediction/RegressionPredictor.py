import numpy as np
import pandas as pd
from pandas.core.interchange.dataframe_protocol import DataFrame

from RegressionModels.MultRegressionType import MultRegressionType


class RegressionPredictor:
    def predict(self, X: pd.DataFrame, model_type: MultRegressionType, coefficients):
        """
        Метод предсказания значений на основе входных данных и типа модели.

        :param coefficients:
        :param model_type:
        :param X: DataFrame с фактами.
        :return: Предсказанные значения в виде массива numpy.
        """
        X = X.to_numpy()  # Преобразуем DataFrame в numpy array
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
        column_names = [f"y {i + 1}" for i in range(y_pred.shape[1])]
        return pd.DataFrame(y_pred, columns=column_names)

    def _predict_linear(self, X, coefficients):
        """Предсказание для линейной регрессии: y = b0 + b1*x1 + b2*x2 + ..."""
        X = np.c_[np.ones((X.shape[0], 1)), X]  # Добавляем единичный столбец для свободного члена
        return X @ coefficients

    def _predict_polynomial(self, X, coefficients):
        """Предсказание для полиномиальной регрессии (2-й степени): y = b0 + b1*x + b2*x^2."""
        X_poly = np.c_[np.ones((X.shape[0], 1)), X, X**2]
        return X_poly @ coefficients

    def _predict_exponential(self, X, coefficients):
        """Предсказание для экспоненциальной регрессии: y = b0 * exp(b1*x)."""
        return coefficients[0] * np.exp(coefficients[1] * X)

    def _predict_quadratic(self, X, coefficients):
        """Предсказание для квадратичной регрессии: y = b0 + b1*x + b2*x^2."""
        X_quad = np.c_[np.ones((X.shape[0], 1)), X, X**2]
        return X_quad @ coefficients
