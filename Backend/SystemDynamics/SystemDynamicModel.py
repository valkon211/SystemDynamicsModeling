import numpy as np
import pandas as pd

from Backend.Common.ModelType import ModelType


class SystemDynamicModel:
    def __init__(
        self,
        model_type: ModelType,
        coefficients: pd.DataFrame,
        relevant_features: list[str]
    ):
        self.model_type = model_type
        self.coefficients = coefficients  # DataFrame: index=features, columns=targets
        self.relevant_features = relevant_features

    def predict(self, df: pd.DataFrame) -> pd.DataFrame:
        X = df[self.relevant_features].copy()

        if self.model_type == ModelType.Linear:
            X_design = self._build_linear_matrix(X)
        elif self.model_type == ModelType.Quadratic:
            X_design = self._build_quadratic_matrix(X)
        elif self.model_type == ModelType.Exponential:
            X_design = self._build_linear_matrix(X)
        else:
            raise ValueError(f"Неизвестный тип модели: {self.model_type}")

        predictions = pd.DataFrame(index=X.index)

        for target in self.coefficients.columns:
            coeffs = self.coefficients[target]

            # Подгоняем под порядок коэффициентов
            X_aligned = X_design.reindex(columns=coeffs.index, fill_value=0)

            y_pred = X_aligned.values @ coeffs.values

            if self.model_type == "exponential":
                y_pred = np.exp(y_pred)

            predictions[target] = y_pred

        return predictions

    def get_equations(self) -> dict[str, str]:
        equations = {}

        for target in self.coefficients.columns:
            coef_series = self.coefficients[target]
            terms = []

            for feature, coef in coef_series.items():
                if abs(coef) < 1e-8:
                    continue

                if feature == "Intercept":
                    term = f"{coef:.4f}"
                elif self.model_type == ModelType.Quadratic and feature.endswith("²"):
                    original_feature = feature[:-1]  # убираем последний символ "²"
                    term = f"{coef:+.4f} * {original_feature}²"
                else:
                    term = f"{coef:+.4f} * {feature}"

                terms.append(term)

            equation_body = " ".join(terms)
            if self.model_type == ModelType.Exponential:
                equation = f"{target}(t) = exp({equation_body.strip()})"
            else:
                equation = f"{target}(t) = {equation_body.strip()}"

            equations[target] = equation

        return equations

    def _build_linear_matrix(self, X: pd.DataFrame) -> pd.DataFrame:
        X_copy = X.copy()
        X_copy["intercept"] = 1.0
        return X_copy

    def _build_quadratic_matrix(self, X: pd.DataFrame) -> pd.DataFrame:
        X_quad = X.copy()
        for col in X.columns:
            X_quad[f"{col}^2"] = X[col] ** 2
        X_quad["intercept"] = 1.0
        return X_quad

    def get_as_json(self):
        data = {
            "model_type": self.model_type.name,
            "features": list(self.coefficients.index),
            "coefficients": self.coefficients.to_dict(orient="index")
        }

        return data

