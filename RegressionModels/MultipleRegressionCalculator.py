import numpy as np

class MultipleRegressionCalculator:
    def __init__(self, X, y):
        """
        Инициализация класса для вычисления коэффициентов множественной регрессии.

        :param X: Матрица признаков (numpy array).
        :param y: Целевая переменная (numpy array).
        """
        self.X = X
        self.y = y

    def linear_regression(self):
        """Вычисляет коэффициенты линейной регрессии."""
        X_b = np.c_[np.ones((self.X.shape[0], 1)), self.X]  # Добавляем столбец единиц для свободного коэффициента
        theta = np.linalg.pinv(X_b.T @ X_b) @ X_b.T @ self.y
        return theta

    def polynomial_regression(self, degree):
        """Вычисляет коэффициенты полиномиальной регрессии указанной степени."""
        X_poly = self._polynomial_features(self.X, degree)
        return self._compute_coefficients(X_poly, self.y)

    def exponential_regression(self):
        """Вычисляет коэффициенты экспоненциальной регрессии."""
        y_log = np.log(self.y)
        theta = self.linear_regression()
        return theta, np.exp(theta[0])  # Возвращаем коэффициенты и пересчитанное значение свободного члена

    def quadratic_regression(self):
        """Вычисляет коэффициенты квадратичной регрессии."""
        return self.polynomial_regression(2)

    def check_linearity(self):
        """
        Проверяет, является ли зависимость между X и y линейной.
        Метод: Сравнение ошибки аппроксимации линейной и нелинейных моделей.
        """
        theta_linear = self.linear_regression()
        y_pred = np.c_[np.ones((self.X.shape[0], 1)), self.X] @ theta_linear
        error_linear = np.sum((self.y - y_pred) ** 2)

        theta_quad = self.quadratic_regression()
        y_pred_quad = self._polynomial_features(self.X, 2) @ theta_quad
        error_quad = np.sum((self.y - y_pred_quad) ** 2)

        return error_linear <= error_quad  # Если ошибка линейной модели меньше или равна квадратичной, считаем зависимость линейной

    def _polynomial_features(self, X, degree):
        """Генерирует полиномиальные признаки до указанной степени."""
        X_poly = X
        for d in range(2, degree + 1):
            X_poly = np.c_[X_poly, X ** d]
        return np.c_[np.ones((X_poly.shape[0], 1)), X_poly]

    def _compute_coefficients(self, X_transformed, y):
        """Общий метод для вычисления коэффициентов."""
        return np.linalg.pinv(X_transformed.T @ X_transformed) @ X_transformed.T @ y
