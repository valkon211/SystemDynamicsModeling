import numpy as np

class MultipleRegressionCalculator:
    def linear_regression(self, X, y):
        """Вычисляет коэффициенты линейной регрессии."""
        X_b = np.c_[np.ones((X.shape[0], 1)), X]  # Добавляем столбец единиц для свободного коэффициента
        theta = np.linalg.pinv(X_b.T @ X_b) @ X_b.T @ y
        return theta

    def polynomial_regression(self, X, y, degree = 2):
        """Вычисляет коэффициенты полиномиальной регрессии указанной степени."""
        X_poly = self._polynomial_features(X, degree)
        return self._compute_coefficients(X_poly, y)

    def exponential_regression(self, X, y):
        """Вычисляет коэффициенты экспоненциальной регрессии."""
        y_log = np.log(y)
        theta = self.linear_regression(X, y_log)
        return theta, np.exp(theta[0])  # Возвращаем коэффициенты и пересчитанное значение свободного члена

    def quadratic_regression(self, X, y):
        """Вычисляет коэффициенты квадратичной регрессии."""
        return self.polynomial_regression(X, y, 2)

    def check_linearity(self, X, y):
        """
        Проверяет, является ли зависимость между X и y линейной.
        Метод: Сравнение ошибки аппроксимации линейной и нелинейных моделей.
        """
        theta_linear = self.linear_regression(X, y)
        y_pred = np.c_[np.ones((X.shape[0], 1)), X] @ theta_linear
        error_linear = np.sum((y - y_pred) ** 2)

        theta_quad = self.quadratic_regression(X, y)
        y_pred_quad = self._polynomial_features(X, 2) @ theta_quad
        error_quad = np.sum((y - y_pred_quad) ** 2)

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
