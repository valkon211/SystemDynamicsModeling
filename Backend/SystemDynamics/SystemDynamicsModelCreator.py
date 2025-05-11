import numpy as np
import pandas as pd

from Backend.Common.ModelType import ModelType
from Backend.SystemDynamics.SystemDynamicModel import SystemDynamicModel


class SystemDynamicModelCreator:
    def __init__(self, lag: int = 1):
        self.lag = lag

    def create(
        self,
        features_df: pd.DataFrame,
        targets_df: pd.DataFrame,
        model_type: ModelType,
        relevant_features: list[str]
    ) -> SystemDynamicModel:
        X_lagged, y_lagged = self._prepare_lagged_data(features_df, targets_df, relevant_features)

        all_coefficients = {}

        for target in y_lagged.columns:
            X = X_lagged.copy()
            y = y_lagged[target].values

            # Расширим X в зависимости от типа модели
            if model_type == ModelType.Linear:
                X_design = self._build_linear_matrix(X)
            elif model_type == ModelType.Quadratic:
                X_design = self._build_quadratic_matrix(X)
            elif model_type == ModelType.Exponential:
                X_design = self._build_linear_matrix(X)
                y = np.log(y + 1e-8)  # логарифмирование, избегаем log(0)
            else:
                raise ValueError(f"Неизвестный тип модели: {model_type}")

            # Вычисление коэффициентов по формуле нормального уравнения
            coef = np.linalg.lstsq(X_design, y, rcond=None)[0]
            coef_index = X_design.columns
            all_coefficients[target] = pd.Series(coef, index=coef_index)

        coefficients_df = pd.DataFrame(all_coefficients)

        return SystemDynamicModel(
            model_type=model_type,
            coefficients=coefficients_df,
            relevant_features=relevant_features
        )

    def create_model_from_json(self, data):
        model_type = ModelType[data["model_type"]]
        features = data["features"]
        coefficients = pd.DataFrame.from_dict(data["coefficients"], orient="index")
        coefficients.index.name = None  # очистим имя индекса, если оно установлено

        return SystemDynamicModel(
            coefficients=coefficients,
            model_type=model_type,
            relevant_features=features)

    def _prepare_lagged_data(
        self,
        features_df: pd.DataFrame,
        targets_df: pd.DataFrame,
        relevant_features: list[str]
    ) -> (pd.DataFrame, pd.DataFrame):
        X = features_df[relevant_features].copy()
        X_lagged = X.shift(self.lag)
        y_lagged = targets_df

        # Очищаем от пропусков
        mask = (~X_lagged.isna().any(axis=1)) & (~y_lagged.isna().any(axis=1))
        return X_lagged[mask], y_lagged[mask]

    def _build_linear_matrix(self, X: pd.DataFrame) -> pd.DataFrame:
        X_copy = X.copy()
        X_copy["Intercept"] = 1.0
        return X_copy

    def _build_quadratic_matrix(self, X: pd.DataFrame) -> pd.DataFrame:
        X_quad = X.copy()
        for col in X.columns:
            X_quad[f"{col}²"] = X[col] ** 2
        X_quad["Intercept"] = 1.0
        return X_quad
