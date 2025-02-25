import numpy as np
import pandas as pd

class RegressionPredictor:
    def __init__(self, model_type, coefficients):
        """
        Инициализация предсказателя.

        :param model_type: Тип уравнения ('linear', 'polynomial', 'exponential', 'quadratic').
        :param coefficients: Список коэффициентов уравнения.
        """
        self.model_type = model_type
        self.coefficients = np.array(coefficients)

    def predict(self, X: pd.DataFrame):
        """
        Метод предсказания значений на основе входных данных и типа модели.

        :param X: DataFrame с фактами.
        :return: Предсказанные значения в виде массива numpy.
        """
        X = X.to_numpy()  # Преобразуем DataFrame в numpy array
        if self.model_type == "linear":
            return self._predict_linear(X)
        elif self.model_type == "polynomial":
            return self._predict_polynomial(X)
        elif self.model_type == "exponential":
            return self._predict_exponential(X)
        elif self.model_type == "quadratic":
            return self._predict_quadratic(X)
        else:
            raise ValueError(f"Неизвестный тип модели: {self.model_type}")

    def _predict_linear(self, X):
        """Предсказание для линейной регрессии: y = b0 + b1*x1 + b2*x2 + ..."""
        X = np.c_[np.ones((X.shape[0], 1)), X]  # Добавляем единичный столбец для свободного члена
        return X @ self.coefficients

    def _predict_polynomial(self, X):
        """Предсказание для полиномиальной регрессии (2-й степени): y = b0 + b1*x + b2*x^2."""
        X_poly = np.c_[np.ones((X.shape[0], 1)), X, X**2]
        return X_poly @ self.coefficients

    def _predict_exponential(self, X):
        """Предсказание для экспоненциальной регрессии: y = b0 * exp(b1*x)."""
        return self.coefficients[0] * np.exp(self.coefficients[1] * X)

    def _predict_quadratic(self, X):
        """Предсказание для квадратичной регрессии: y = b0 + b1*x + b2*x^2."""
        X_quad = np.c_[np.ones((X.shape[0], 1)), X, X**2]
        return X_quad @ self.coefficients
