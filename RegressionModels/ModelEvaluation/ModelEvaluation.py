import numpy as np
import pandas as pd


class ModelEvaluation:
    def __init__(self, X: pd.DataFrame, y: pd.DataFrame, y_pred: pd.DataFrame):
        self.X = X
        self.y = y
        self.y_pred = y_pred

    def evaluate(self):
        return {
            "WAPE": self.weighted_absolute_percentage_error(),
            "AR": self.accuracy_ratio(),
            "R²": self.r_squared(),
            "Std": self.standard_error(),
            "F-metrics": self.f_statistic()
        }

    def weighted_absolute_percentage_error(self) -> pd.DataFrame:
        """Вычисление WAPE (Weighted Absolute Percentage Error)."""
        wape = (np.abs(self.y - self.y_pred).sum() / np.abs(self.y).sum()).round(4)
        return pd.DataFrame(wape).transpose().rename(columns=lambda x: f"WAPE {x}")

    def accuracy_ratio(self) -> pd.DataFrame:
        """Вычисление AR (Accuracy Ratio)."""
        ar = (1 - (np.abs(self.y - self.y_pred).sum() / np.abs(self.y).sum())).round(4)
        return pd.DataFrame(ar).transpose().rename(columns=lambda x: f"AR {x}")

    def r_squared(self):
        """Коэффициент детерминации R²."""
        ss_total = ((self.y - self.y.mean()) ** 2).sum()
        ss_residual = ((self.y - self.y_pred) ** 2).sum()
        r2 = (1 - (ss_residual / ss_total)).round(4)
        return pd.DataFrame(r2).transpose().rename(columns=lambda x: f"R² {x}")

    def standard_error(self):
        """Вычисление стандартной ошибки коэффициентов регрессии."""
        residuals = self.y - self.y_pred
        mse = (residuals ** 2).sum() / (len(self.y) - len(self.X.columns) - 1)
        X_with_intercept = pd.concat([pd.Series(1, index=self.X.index, name="Intercept"), self.X], axis=1)
        cov_matrix = np.linalg.inv(X_with_intercept.T @ X_with_intercept) * mse.mean()
        return np.sqrt(np.diag(cov_matrix))

    def f_statistic(self):
        """Вычисление F-статистики для модели."""
        f_stats = []  # Список для хранения F-статистик для каждого столбца y

        # Число предикторов и наблюдений
        k = len(self.X.columns)  # Число предикторов
        n = len(self.y)  # Число наблюдений

        # Вычисляем F-статистику для каждого столбца y
        for col in self.y.columns:  # Итерируемся по именам столбцов y
            y_col = self.y[col]  # Текущий столбец y
            y_pred_col = self.y_pred[col]  # Предсказанные значения для текущего столбца y

            # Общая сумма квадратов (SS_total)
            ss_total = ((y_col - y_col.mean()) ** 2).sum()

            # Сумма квадратов регрессии (SS_regression)
            ss_regression = ((y_pred_col - y_col.mean()) ** 2).sum()

            # F-статистика для текущего столбца
            f_stat = (ss_regression / k) / ((ss_total - ss_regression) / (n - k - 1))
            f_stats.append(f_stat)

        return np.array(f_stats)