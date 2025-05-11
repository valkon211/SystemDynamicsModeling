import numpy as np
import pandas as pd

from Backend.Common.ModelType import ModelType
from Backend.SystemDynamics.ExtendedSystemDynamicModel import ExtendedSystemDynamicModel


class ExtendedSystemDynamicModelCreator:
    def _fit_equation(self, y: pd.Series, X: pd.DataFrame, model_type: ModelType) -> pd.Series:
        if model_type == ModelType.Linear:
            X_design = X.copy()
        elif model_type == ModelType.Quadratic:
            X_design = X ** 2
        elif model_type == ModelType.Exponential:
            X_design = X.copy()
            y = np.log(y.replace(0, 1e-6))  # избегаем log(0)
        else:
            raise ValueError(f"Неизвестный тип модели: {model_type}")

        X_design = X_design.copy()
        X_design['Intercept'] = 1.0

        coeffs = np.linalg.lstsq(X_design.values, y.values, rcond=None)[0]
        return pd.Series(coeffs, index=X_design.columns)

    def create(self, features_df: pd.DataFrame, targets_df: pd.DataFrame, model_type: ModelType) -> ExtendedSystemDynamicModel:
        all_vars = features_df.columns.tolist() + targets_df.columns.tolist()
        combined_df = pd.concat([features_df, targets_df], axis=1)

        relevant_features: dict[str, list[str]] = {}
        coefficient_rows: list[pd.Series] = []

        # Анализ зависимостей: каждая переменная зависит от других
        for target in all_vars:
            independent_vars = [var for var in all_vars if var != target]
            X = combined_df[independent_vars]
            y = combined_df[target]

            coeffs = self._fit_equation(y, X, model_type)
            coeffs.name = target
            coeffs = coeffs.round(3)
            coeffs[coeffs.abs() < 0.0005] = 0.0
            coefficient_rows.append(coeffs)

            relevant = [var for var in coeffs.index if var != 'Intercept' and not np.isclose(coeffs[var], 0.0)]
            relevant_features[target] = relevant

        coefficients_df = pd.DataFrame(coefficient_rows)

        return ExtendedSystemDynamicModel(
            model_type=model_type,
            coefficients=coefficients_df,
            relevant_features=relevant_features
        )

    @staticmethod
    def create_from_json(data) -> ExtendedSystemDynamicModel:
        coefficients = pd.DataFrame.from_dict(data["coefficients"], orient="index")
        coefficients.index.name = None
        return ExtendedSystemDynamicModel(
            model_type=data["model_type"],
            coefficients=coefficients,
            relevant_features=data["relevant_features"]
        )