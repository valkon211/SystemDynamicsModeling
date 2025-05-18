import numpy as np
import pandas as pd

from Backend.Common.ModelType import ModelType


class ExtendedSystemDynamicModel:
    def __init__(
            self,
            model_type: ModelType,
            coefficients: pd.DataFrame  # Индекс — зависимая переменная, колонки — независимые + intercept
    ):
        self.model_type = model_type
        self.coefficients = coefficients

    def predict(self, initial_values: pd.Series, steps: int) -> pd.DataFrame:
        current_state = initial_values.copy()
        history = [current_state.copy()]
        targets = list(self.coefficients.index)

        for _ in range(steps):
            new_values = {}

            for target in targets:
                coeffs = self.coefficients.loc[target]
                intercept = coeffs.get("Intercept", 0.0)

                value = intercept

                for feature, weight in coeffs.items():
                    if feature == "Intercept" or np.isclose(weight, 0.0):
                        continue

                    if feature.endswith("²"):
                        base_name = feature.replace("²", "")
                        val = current_state.get(base_name, 0.0) ** 2
                    elif self.model_type == ModelType.Exponential:
                        val = np.exp(current_state.get(feature, 0.0))
                    else:
                        val = current_state.get(feature, 0.0)

                    value += weight * val

                new_values[target] = value

            current_state = current_state.copy()
            current_state.update(pd.Series(new_values))
            history.append(current_state.copy())

        return pd.DataFrame(history)[self.coefficients.index].reset_index(drop=True).round(4)

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
                elif self.model_type == ModelType.Linear or self.model_type == ModelType.Quadratic:
                    term = f"{formatted_coef}*{feature}(t-1)"
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
            "coefficients": self.coefficients.to_dict(orient="index")  # строки — переменные
        }