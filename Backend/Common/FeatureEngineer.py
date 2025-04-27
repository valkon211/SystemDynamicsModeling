import numpy as np
import pandas as pd


class FeatureEngineer:
    def __init__(self, relevant_features: list[str] = None):
        self.relevant_features = relevant_features

    def generate_and_select_features(self, X: pd.DataFrame) -> pd.DataFrame:
        #X_with_features = self.prepare_features(X)
        self.select_relevant_features(X)
        X_selected = X[self.relevant_features]

        return X_selected

    def prepare_features(self, X: pd.DataFrame) -> pd.DataFrame:
        X_interacted = X.copy()
        columns = X.columns

        for i in range(len(columns)):
            for j in range(i + 1, len(columns)):
                interaction_term = X[columns[i]] * X[columns[j]]
                X_interacted[f"{columns[i]}*{columns[j]}"] = interaction_term

        if self.relevant_features:
            X_prepared = X_interacted[self.relevant_features]
        else:
            X_prepared = X_interacted

        return X_prepared

    def select_relevant_features(self, X: pd.DataFrame, threshold: float = 0.01) -> None:
        correlations = X.corr().abs()
        upper_triangle = correlations.where(
            np.triu(np.ones(correlations.shape), k=1).astype(bool)
        )
        to_drop = [
            column for column in upper_triangle.columns
            if any(upper_triangle[column] > (1 - threshold))
        ]
        self.relevant_features = [col for col in X.columns if col not in to_drop]

    def prepare_features_for_predict(self, X: pd.DataFrame) -> pd.DataFrame:
        X_interacted = X.copy()
        columns = X.columns

        for i in range(len(columns)):
            for j in range(i + 1, len(columns)):
                interaction_term = X[columns[i]] * X[columns[j]]
                X_interacted[f"{columns[i]}*{columns[j]}"] = interaction_term

        if self.relevant_features is not None:
            missing_features = set(self.relevant_features) - set(X_interacted.columns)
            for feature in missing_features:
                X_interacted[feature] = 0  # если какого-то взаимодействия нет, заполняем нулями

            X_prepared = X_interacted[self.relevant_features]
        else:
            X_prepared = X_interacted

        return X_prepared
