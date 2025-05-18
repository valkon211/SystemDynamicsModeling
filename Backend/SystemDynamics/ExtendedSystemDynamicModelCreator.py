import numpy as np
import pandas as pd

from Backend.Common.ModelType import ModelType
from Backend.SystemDynamics.ExtendedSystemDynamicModel import ExtendedSystemDynamicModel


class ExtendedSystemDynamicModelCreator:
    def _fit_equation(self, y: pd.Series, X: pd.DataFrame, model_type: ModelType) -> pd.Series:
        if model_type == ModelType.Linear:
            X_design = X.copy()

        elif model_type == ModelType.Quadratic:
            X_squared = X ** 2
            X_squared.columns = [f"{col}²" for col in X.columns]
            X_design = pd.concat([X, X_squared], axis=1)

        elif model_type == ModelType.Exponential:
            X_design = X.copy()
            y = np.log(y.replace(0, 1e-6))  # избегаем log(0)

        else:
            raise ValueError(f"Неизвестный тип модели: {model_type}")

        X_design = X_design.copy()
        X_design['Intercept'] = 1.0

        coeffs = np.linalg.lstsq(X_design.values, y.values, rcond=None)[0]
        return pd.Series(coeffs, index=X_design.columns)

    def create(
        self,
        features_df: pd.DataFrame,
        targets_df: pd.DataFrame,
        model_type: ModelType,
        relevant_features: list[str]
    ) -> ExtendedSystemDynamicModel:
        all_features = features_df.columns.tolist()

        # Подготовка полного набора фич
        if model_type == ModelType.Quadratic:
            squared_features = [f"{col}²" for col in all_features]
            full_feature_names = all_features + squared_features
        else:
            full_feature_names = all_features

        combined_df = pd.concat([features_df, targets_df], axis=1)
        all_targets = combined_df.columns.tolist()

        coefficient_rows: list[pd.Series] = []

        for target in all_targets:
            # Используем только релевантные признаки при обучении
            X = features_df[relevant_features]
            y = combined_df[target]

            # Получаем коэффициенты только для релевантных признаков
            coeffs_partial = self._fit_equation(y, X, model_type)
            coeffs_partial = coeffs_partial.round(4)
            coeffs_partial[coeffs_partial.abs() < 0.0005] = 0.0

            # Создаём полный вектор коэффициентов
            full_coeffs = pd.Series(0.0, index=full_feature_names + ['Intercept'])
            for name in coeffs_partial.index:
                full_coeffs[name] = coeffs_partial[name]

            full_coeffs.name = target
            coefficient_rows.append(full_coeffs)

        coefficients_df = pd.DataFrame(coefficient_rows)

        return ExtendedSystemDynamicModel(
            model_type=model_type,
            coefficients=coefficients_df
        )

    @staticmethod
    def create_from_json(data) -> ExtendedSystemDynamicModel:
        coefficients = pd.DataFrame.from_dict(data["coefficients"], orient="index")
        coefficients.index.name = None

        return ExtendedSystemDynamicModel(
            model_type=data["model_type"],
            coefficients=coefficients
        )