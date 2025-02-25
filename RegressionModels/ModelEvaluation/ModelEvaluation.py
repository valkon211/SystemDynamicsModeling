import numpy as np
from scipy import stats

class ModelEvaluation:
    def __init__(self, X, y, theta):
        """
        Инициализация класса для оценки значимости модели.

        :param X: Матрица признаков (numpy array).
        :param y: Целевая переменная (numpy array).
        :param theta: Вектор коэффициентов регрессии (numpy array).
        """
        self.X = np.c_[np.ones((X.shape[0], 1)), X]  # Добавляем столбец единиц для свободного члена
        self.y = y
        self.theta = theta
        self.n = len(y)                             # Количество наблюдений
        self.k = self.X.shape[1]                    # Количество параметров (включая свободный член)
        self.y_pred = self.X @ theta                # Предсказанные значения
        self.residuals = y - self.y_pred            # Остатки

    def r_squared(self):
        """Вычисляет коэффициент детерминации R²."""
        ss_total = np.sum((self.y - np.mean(self.y)) ** 2)
        ss_residual = np.sum(self.residuals ** 2)
        return 1 - (ss_residual / ss_total)

    def standard_error(self):
        """Вычисляет стандартную ошибку коэффициентов."""
        mse = np.sum(self.residuals ** 2) / (self.n - self.k)  # Среднеквадратичная ошибка
        var_matrix = mse * np.linalg.pinv(self.X.T @ self.X)  # Ковариационная матрица
        return np.sqrt(np.diag(var_matrix))  # Корень из диагональных элементов

    def f_statistic(self):
        """Вычисляет F-статистику для значимости модели."""
        ss_total = np.sum((self.y - np.mean(self.y)) ** 2)
        ss_residual = np.sum(self.residuals ** 2)
        ss_explained = ss_total - ss_residual

        ms_explained = ss_explained / (self.k - 1)  # Средний квадрат объяснённой дисперсии
        ms_residual = ss_residual / (self.n - self.k)  # Средний квадрат ошибки

        f_value = ms_explained / ms_residual
        p_value = 1 - stats.f.cdf(f_value, self.k - 1, self.n - self.k)  # p-значение F-теста

        return f_value, p_value
