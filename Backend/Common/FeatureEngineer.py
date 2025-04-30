import pandas as pd
import itertools

class FeatureEngineer:
    @staticmethod
    def generate_features(X: pd.DataFrame) -> pd.DataFrame:
        """Добавляет признаки взаимодействия между колонками"""
        X_new = X.copy()
        for (col1, col2) in itertools.combinations(X.columns, 2):
            X_new[f"{col1}*{col2}"] = X[col1] * X[col2]
        return X_new

    @staticmethod
    def select_relevant_features(X: pd.DataFrame, threshold: float = 1e-5) -> list:
        """Удаляет признаки с низкой дисперсией"""
        variances = X.var()
        relevant_features = variances[variances > threshold].index.tolist()
        return relevant_features

    @staticmethod
    def prepare_for_prediction(X: pd.DataFrame, relevant_features: list) -> pd.DataFrame:
        """Добавляет признаки взаимодействия и фильтрует по нужным признакам"""
        X_with_features = FeatureEngineer.generate_features(X)

        # Добавим отсутствующие признаки как нули (если обучали на большем числе фич)
        for feature in relevant_features:
            if feature not in X_with_features.columns:
                X_with_features[feature] = 0.0

        return X_with_features[relevant_features]