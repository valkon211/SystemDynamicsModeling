import pandas as pd


class DataAnalyzer:
    @staticmethod
    def get_correlation_matrix(X: pd.DataFrame, y: pd.DataFrame) -> pd.DataFrame:
        combined_data = pd.concat([X, y], axis=1)
        return combined_data.corr().round(4)