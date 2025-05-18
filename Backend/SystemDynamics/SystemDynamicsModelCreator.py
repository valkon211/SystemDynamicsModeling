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
        X_lagged, y_lagged = self._prepare_lagged_data(features_df, targets_df)

        all_feature_names = list(features_df.columns)
        all_coefficients = {}

        for target in y_lagged.columns:
            X = X_lagged[relevant_features].copy()
            y = y_lagged[target].values

            # Построение дизайн-матрицы с только релевантными переменными
            if model_type == ModelType.Linear:
                X_design = self._build_linear_matrix(X)
                full_X_design = self._build_linear_matrix(features_df[all_feature_names].copy())
            elif model_type == ModelType.Quadratic:
                X_design = self._build_quadratic_matrix(X)
                full_X_design = self._build_quadratic_matrix(features_df[all_feature_names].copy())
            elif model_type == ModelType.Exponential:
                X_design = self._build_linear_matrix(X)
                full_X_design = self._build_linear_matrix(features_df[all_feature_names].copy())
                y = np.log(y + 1e-8)
            else:
                raise ValueError(f"Неизвестный тип модели: {model_type}")

            # Вычисляем коэффициенты только по релевантным признакам
            coef = np.linalg.lstsq(X_design, y, rcond=None)[0]
            partial_coef_series = pd.Series(coef, index=X_design.columns)

            # Обнуляем коэффициенты нерелевантных признаков, создавая полную серию
            full_coef_series = pd.Series(0.0, index=full_X_design.columns)
            full_coef_series.update(partial_coef_series)

            all_coefficients[target] = full_coef_series

        coefficients_df = pd.DataFrame(all_coefficients).round(4)

        return SystemDynamicModel(
            model_type=model_type,
            coefficients=coefficients_df
        )

    def create_from_json(self, data):
        coefficients = pd.DataFrame.from_dict(data["coefficients"], orient="index")
        coefficients.index.name = None

        return SystemDynamicModel(
            coefficients=coefficients,
            model_type=ModelType[data["model_type"]])

    def _prepare_lagged_data(
        self,
        features_df: pd.DataFrame,
        targets_df: pd.DataFrame,
    ) -> (pd.DataFrame, pd.DataFrame):
        X_lagged = features_df.shift(self.lag)
        y_lagged = targets_df
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
