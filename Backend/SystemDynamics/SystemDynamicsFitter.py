import numpy as np
import pandas as pd

from Backend.Common.ModelType import ModelType
from Backend.SystemDynamics.SystemDynamicsModel import SystemDynamicsModel


class SystemDynamicsFitter:
    def fit(self, X: pd.DataFrame, y: pd.Series, model_type: ModelType, degree: int = 2) -> SystemDynamicsModel:
        if model_type == ModelType.Linear:
            X_ = np.column_stack([np.ones(X.shape[0]), X.values])
        elif model_type == ModelType.Quadratic:
            X_ = np.column_stack([np.ones(X.shape[0]), X.values, X.values ** 2])
        elif model_type == ModelType.Polynomial:
            X_poly = [np.ones(X.shape[0])]
            for i in range(1, degree + 1):
                X_poly.append(np.power(X.values, i))
            X_ = np.column_stack(X_poly)
        elif model_type == ModelType.Exponential:
            X_ = np.column_stack([np.ones(X.shape[0]), X.values])
            y = np.log(y)
        else:
            raise ValueError(f"Неизвестный тип модели: {model_type}")

        coefficients = np.linalg.pinv(X_) @ y.values
        return SystemDynamicsModel(coefficients, model_type)