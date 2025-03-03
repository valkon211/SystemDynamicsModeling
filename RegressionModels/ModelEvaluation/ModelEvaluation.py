import numpy as np
import pandas as pd


class ModelEvaluation:
    def __init__(self, X: pd.DataFrame, y: pd.DataFrame, y_pred: pd.DataFrame):
        self.X = X
        self.y = y
        self.y_pred = y_pred

    def wape(self):
        """Вычисление WAPE (Weighted Absolute Percentage Error)."""
        return (abs(self.y - self.y_pred).sum() / self.y.sum()).mean()

    def ar(self):
        """Вычисление AR (Accuracy Ratio)."""
        return (1 - abs(self.y - self.y_pred) / self.y).mean().mean()

    def r_squared(self):
        """Коэффициент детерминации R²."""
        ss_total = ((self.y - self.y.mean()) ** 2).sum()
        ss_residual = ((self.y - self.y_pred) ** 2).sum()
        return 1 - (ss_residual / ss_total)

    def standard_error(self):
        """Вычисление стандартной ошибки коэффициентов регрессии."""
        residuals = self.y - self.y_pred
        mse = (residuals ** 2).sum() / (len(self.y) - len(self.X.columns) - 1)
        X_with_intercept = pd.concat([pd.Series(1, index=self.X.index, name="Intercept"), self.X], axis=1)
        cov_matrix = np.linalg.inv(X_with_intercept.T @ X_with_intercept) * mse.mean()
        return np.sqrt(np.diag(cov_matrix))

    def f_statistic(self):
        """Вычисление F-статистики для модели."""
        ss_total = ((self.y - self.y.mean()) ** 2).sum()
        ss_regression = ((self.y_pred - self.y.mean()) ** 2).sum()
        k = len(self.X.columns)  # Число предикторов
        n = len(self.y)  # Число наблюдений
        f_stat = (ss_regression / k) / ((ss_total - ss_regression) / (n - k - 1))
        return f_stat.mean()