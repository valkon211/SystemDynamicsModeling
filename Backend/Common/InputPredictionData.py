from dataclasses import dataclass

from Backend.Common.InputModelType import InputModelType
from Backend.Common.ModelType import ModelType


@dataclass
class InputPredictionData:
    input_model_type: InputModelType
    path_x: str = None
    path_coefficients: str = None
    model_type: ModelType = None
    json_data_path: str = None
    is_extended: bool = False
