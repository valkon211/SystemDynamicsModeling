import json

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

        return pd.DataFrame(history).reset_index(drop=True)

    def to_json(self, filepath: str) -> None:
        model_dict = {
            "model_type": self.model_type,
            "coefficients": self.coefficients.to_dict(orient="index"),  # сохраняем построчно
            "relevant_features": self.relevant_features
        }
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(model_dict, f, ensure_ascii=False, indent=4)

    def get_equation_strings(self) -> dict:
        equation_dict = {}

        for output_var in self.coefficients.index:
            coeffs = self.coefficients.loc[output_var]
            terms = []

            for input_var, coef in coeffs.items():
                if coef == 0 or pd.isna(coef):
                    continue

                formatted_coef = f"{abs(coef):.3f}"

                if self.model_type == ModelType.Linear:
                    expr = f"{formatted_coef}*{input_var}(t-1)"
                elif self.model_type == ModelType.Quadratic:
                    expr = f"{formatted_coef}*{input_var}(t-1)²"
                elif self.model_type == ModelType.Exponential:
                    expr = f"{formatted_coef}*exp({input_var}(t-1))"
                else:
                    expr = f"{formatted_coef}*{input_var}(t-1)"  # fallback

                sign = "-" if coef < 0 else "+"
                terms.append((sign, expr))

            if terms:
                first_sign, first_expr = terms[0]
                equation = f"{output_var}(t) = "
                equation += f"- {first_expr}" if first_sign == "-" else first_expr
                for sign, expr in terms[1:]:
                    equation += f" {sign} {expr}"
            else:
                equation = f"{output_var}(t) = 0"

            equation_dict[output_var] = equation

        return equation_dict

    def to_json(self):
        return {
            "model_type": self.model_type.name,
            "features": self.relevant_features,
            "coefficients": self.coefficients.to_dict(orient="index")  # строки — переменные
        }