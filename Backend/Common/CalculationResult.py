import pandas as pd


class CalculationResult:
    def __init__(self,
                 result_df: pd.DataFrame,
                 model_type: str,
                 relevant_features:list[str] = None,
                 equations: dict[str, str] = None,
                 json_data = None):
        self.result_df = result_df
        self.model_type = model_type
        self.relevant_features = relevant_features
        self.equations = equations
        self.json_data = json_data