import numpy as np
import pandas as pd

from Backend.Common.ModelEvaluator import ModelEvaluator


class SystemDynamicsModelEvaluator(ModelEvaluator):
    def evaluate(self, true_series: pd.Series, pred_series: pd.Series) -> pd.DataFrame:
        mae_total = 0
        wape_total = 0
        r2_total = 0
        n_targets = true_series.shape[0]

        data = pd.concat([true_series, pred_series], axis=1)
        data.columns = ['true', 'pred']

        for _, row in data.iterrows():
            y_true = row['true']
            y_pred = row['pred']

            mae = self.mean_absolute_error(pd.Series([y_true]), pd.Series([y_pred]))
            wape = self.wape(pd.Series([y_true]), pd.Series([y_pred]))
            r2 = self.r2_score(pd.Series([y_true]), pd.Series([y_pred]))

            mae_total += mae
            wape_total += wape
            r2_total += r2

        mae_total /= n_targets
        wape_total /= n_targets
        r2_total /= n_targets

        return pd.DataFrame([[mae_total, wape_total, r2_total]], columns=["MAE", "WAPE", "R²"]).round(4)