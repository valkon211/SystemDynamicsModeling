import numpy as np
import pandas as pd

from Backend.Common.ModelEvaluator import ModelEvaluator

class MultipleRegressionModelEvaluator(ModelEvaluator):
    def evaluate_models(self, true_df: pd.DataFrame, predictions_dict: dict) -> pd.DataFrame:
        results = {
            "MAE": [],
            "WAPE": [],
            "R²": []
        }
        model_names = []

        for model_name, pred_df in predictions_dict.items():
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

            # усреднение по всем столбцам
            results["MAE"].append(np.round(mae_total, 4) / n_targets)
            results["WAPE"].append(np.round(wape_total, 4) / n_targets)
            results["R²"].append(np.round(r2_total, 4) / n_targets)
            model_names.append(model_name)

        metrics_df = pd.DataFrame(results, index=model_names)
        print("\n", metrics_df)
        return metrics_df