import pandas as pd


class CalculationResult:
    def __init__(self, result_df: pd.DataFrame, result_func: str):
        self.result_df = result_df
        self.result_func = result_func