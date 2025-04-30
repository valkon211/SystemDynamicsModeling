import pandas as pd

from Backend.Common.FeatureEngineer import FeatureEngineer
from Backend.Common.ModelType import ModelType
from Backend.Data.AnalyticsDataPreparer import AnalyticsDataPreparer


class MultipleRegressionModel:
    def __init__(self, coefficients: pd.DataFrame, relevant_features: list[str], model_type: ModelType):
        self.type = model_type
        self.coefficients = coefficients
        self.relevant_features = relevant_features

    def predict(self, X: pd.DataFrame) -> pd.DataFrame:
        if self.relevant_features == [] or self.relevant_features == None:
            self.relevant_features = self.coefficients.index.difference(['Intercept']).tolist()

        # 1. Подготовка признаков
        X_prepared = FeatureEngineer.prepare_for_prediction(X, self.relevant_features)

        # 2. Трансформация (полиномы, квадрат, лог и т.д.)
        X_transformed = AnalyticsDataPreparer.transform_x(X_prepared, self.type)

        # 3. Предсказание
        y_pred = X_transformed @ self.coefficients

        # 4. Обратное преобразование, если нужно (например, экспонента)
        y_pred = AnalyticsDataPreparer.inverse_transform_y(y_pred, self.type)

        return y_pred.round(4)

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
                elif self.type == ModelType.Quadratic and feature.endswith("²"):
                    original_feature = feature[:-1]  # убираем последний символ "²"
                    term = f"{coef:+.4f} * {original_feature}²"
                else:
                    term = f"{coef:+.4f} * {feature}"

                terms.append(term)

            equation_body = " ".join(terms)
            if self.type == ModelType.Exponential:
                equation = f"{target}(t) = exp({equation_body.strip()})"
            else:
                equation = f"{target}(t) = {equation_body.strip()}"

            equations[target] = equation

        return equations

