import pandas as pd


class CalculationResult:
    def __init__(self,
                 result_df: pd.DataFrame,
                 result_func: str,
                 relevant_features:list[str] = None,
                 equations: dict[str, str] = None):
        self.result_df = result_df
        self.result_func = result_func
        self.relevant_features = relevant_features
        self.equations = equations