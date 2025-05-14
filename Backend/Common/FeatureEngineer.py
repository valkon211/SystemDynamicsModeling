import pandas as pd

class FeatureEngineer:
    @staticmethod
    def select_relevant_features(X: pd.DataFrame, threshold: float = 1e-5) -> list:
        """Удаляет признаки с низкой дисперсией"""
        variances = X.var()
        relevant_features = variances[variances > threshold].index.tolist()
        return relevant_features