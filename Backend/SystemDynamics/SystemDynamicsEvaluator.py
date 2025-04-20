import numpy as np
import pandas as pd

from Backend.Common.ModelEvaluator import ModelEvaluator


class SystemDynamicsEvaluator(ModelEvaluator):
    def evaluate(self, y_true: pd.DataFrame, y_pred: pd.DataFrame) -> dict:
        mae = self.mean_absolute_error(y_true, y_pred)
        wape = self.wape(y_true, y_pred)
        r2 = self.r2_score(y_true, y_pred)

        return {
            "MAE": np.round(mae, 4),
            "WAPE": np.round(wape, 4),
            "R²": np.round(r2, 4)
        }