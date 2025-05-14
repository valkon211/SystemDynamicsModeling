import numpy as np
import pandas as pd

from Backend.Common.ModelType import ModelType


class ExtendedSystemDynamicModel:
    def __init__(
            self,
            model_type: ModelType,
            coefficients: pd.DataFrame,  # Индекс — зависимая переменная, колонки — независимые + intercept
            relevant_features: dict[str, list[str]]
            # для каждой зависимой переменной — список фич, от которых она зависит
    ):
        self.model_type = model_type
        self.coefficients = coefficients
        self.relevant_features = relevant_features

    def predict(self, initial_values: pd.Series, steps: int) -> pd.DataFrame:
        history = [initial_values.copy()]
        variables = list(self.coefficients.index)

        for _ in range(steps):
            prev = history[-1].copy()
            new_values = {}

            for var in variables:
                inputs = self.relevant_features[var]
                coeffs = self.coefficients.loc[var]
                intercept = coeffs.get("Intercept", 0)

                x = np.array([prev[f] for f in inputs])
                w = np.array([coeffs[f] for f in inputs])

                if self.model_type == ModelType.Linear:
                    value = intercept + np.dot(w, x)
                elif self.model_type == ModelType.Quadratic:
                    value = intercept + np.dot(w, x ** 2)
                elif self.model_type == ModelType.Quadratic:
                    value = intercept + np.dot(w, np.exp(x))
                else:
                    raise ValueError(f"Неизвестный тип модели: {self.model_type}")

                new_values[var] = value

            history.append(pd.Series(new_values))

        return pd.DataFrame(history).reset_index(drop=True).round(4)

    def get_equation_strings(self) -> dict:
        equations = {}

        for target in self.coefficients.index:
            coef_series = self.coefficients.loc[target]
            terms = []

            for feature, coef in coef_series.items():
                if abs(coef) < 1e-8 or feature == target:
                    continue

                formatted_coef = f"{coef:+.4f}"

                if feature == "Intercept":
                    term = formatted_coef
                elif self.model_type == ModelType.Linear:
                    term = f"{formatted_coef}*{feature}(t-1)"
                elif self.model_type == ModelType.Quadratic:
                    term = f"{formatted_coef}*{feature}(t-1)²"
                elif self.model_type == ModelType.Exponential:
                    term = f"{formatted_coef}*exp({feature}(t-1))"
                else:
                    term = f"{formatted_coef}*{feature}(t-1)"

                terms.append(term)

            equation_body = " ".join(terms)
            equation = f"{target}(t) = {equation_body.strip()}"

            equations[target] = equation

        return equations

    def to_json(self):
        return {
            "model_type": self.model_type.name,
            "features": self.relevant_features,
            "coefficients": self.coefficients.to_dict(orient="index")  # строки — переменные
        }