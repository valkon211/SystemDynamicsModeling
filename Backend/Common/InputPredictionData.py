from dataclasses import dataclass

from Backend.Common.ModelType import ModelType


@dataclass
class InputPredictionData:
    path_x: str = None
    path_coefficients: str = None
    model_type: ModelType = None
    relevant_features: list[str] = None
    json_data_path: str = None
    is_extended: bool = False
