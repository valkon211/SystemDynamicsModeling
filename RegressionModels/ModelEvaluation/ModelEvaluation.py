import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score, r2_score


class ModelEvaluation:
    def __init__(self, X: pd.DataFrame, y: pd.DataFrame, y_pred: pd.DataFrame):
        self.X = X
        self.y = y
        self.y_pred = y_pred

    def wape(self) -> pd.DataFrame:
        """Вычисление WAPE (Weighted Absolute Percentage Error)."""
        absolute_errors = abs(self.y - self.y_pred)
        sum_absolute_errors = absolute_errors.sum()
        sum_actual_values = abs(self.y).sum()
        wape_values = sum_absolute_errors / sum_actual_values

        return pd.DataFrame(wape_values, columns=["WAPE"])

    def ar(self) -> pd.DataFrame:
        """Вычисление AR (Accuracy Ratio)."""
        if self.y.shape != self.y_pred.shape:
            raise ValueError("Размерности y и y_pred должны совпадать!")

        ar_values = {}

        for col in self.y.columns:
            # Вычисляем AUC
            auc = roc_auc_score(self.y[col], self.y_pred[col])

            # Gini Coefficient
            gini_model = 2 * auc - 1

            # Accuracy Ratio
            ar_values[col] = round(gini_model / 1, 4)  # Деление на G_perfect = 1

        # Создаём DataFrame
        ar_df = pd.DataFrame(ar_values, columns=["AR"])

        return ar_df

    def r_squared(self):
        """Коэффициент детерминации R²."""
        # Проверка размерностей
        if self.y.shape != self.y_pred.shape:
            raise ValueError("Размерности y и y_pred должны совпадать!")

        r2_values = {col: round(r2_score(self.y[col], self.y_pred[col]), 4) for col in self.y.columns}

        return pd.DataFrame(r2_values)

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