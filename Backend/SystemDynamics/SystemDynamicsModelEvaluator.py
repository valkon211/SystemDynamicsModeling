import numpy as np
import pandas as pd

from Backend.Common.ModelEvaluator import ModelEvaluator


class SystemDynamicsModelEvaluator(ModelEvaluator):
    def evaluate(self, true_df: pd.DataFrame, pred_df: pd.DataFrame) -> pd.DataFrame:
        mae_total = 0
        wape_total = 0
        r2_total = 0
        n_targets = true_df.shape[1]

        for column in true_df.columns:
            y_true = true_df[column]
            y_pred = pred_df[column]

            mae = self.mean_absolute_error(y_true, y_pred)
            wape = self.wape(y_true, y_pred)
            r2 = self.r2_score(y_true, y_pred)

            mae_total += mae
            wape_total += wape
            r2_total += r2

        mae_result = np.round(mae_total, 4) / n_targets
        wape_result = np.round(wape_total, 4) / n_targets
        r2_result = np.round(r2_total, 4) / n_targets

        return pd.DataFrame([[mae_result, wape_result, r2_result]], columns=["MAE", "WAPE", "R²"]).round(4)