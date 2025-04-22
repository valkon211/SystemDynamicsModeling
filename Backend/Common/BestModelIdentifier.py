import numpy as np
import pandas as pd

from Backend.Common.ModelType import ModelType


class BestModelIdentifier:
    def determine_best_model(self, df: pd.DataFrame) -> ModelType:
        return self._topsis(df)

    def _calculate_entropy_weights(self, df: pd.DataFrame) -> np.ndarray:
        data = df.to_numpy()
        column_sums = data.sum(axis=0)
        column_sums[column_sums == 0] = 1e-12

        P = data / column_sums
        P = np.clip(P, 1e-12, None)

        k = 1 / np.log(len(df))
        entropy = -k * (P * np.log(P)).sum(axis=0)
        d = 1 - entropy
        d[d < 0] = 0
        weights = d / d.sum() if d.sum() != 0 else np.ones_like(d) / len(d)

        return weights

    def _topsis(self, df: pd.DataFrame, benefit_criteria: list[str] =["R²"]) -> ModelType:
        data = df.copy()
        norm_data = data / np.sqrt((data ** 2).sum())
        weights = self._calculate_entropy_weights(data)
        weighted_data = norm_data * weights

        ideal = []
        anti_ideal = []
        for col in data.columns:
            if col in benefit_criteria:
                ideal.append(weighted_data[col].max())
                anti_ideal.append(weighted_data[col].min())
            else:
                ideal.append(weighted_data[col].min())
                anti_ideal.append(weighted_data[col].max())

        ideal = np.array(ideal)
        anti_ideal = np.array(anti_ideal)
        d_pos = np.linalg.norm(weighted_data.to_numpy() - ideal, axis=1)
        d_neg = np.linalg.norm(weighted_data.to_numpy() - anti_ideal, axis=1)
        closeness = d_neg / (d_pos + d_neg)
        best_index = np.argmax(closeness)

        return data.index[best_index]