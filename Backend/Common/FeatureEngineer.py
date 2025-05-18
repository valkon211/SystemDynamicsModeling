import pandas as pd
import statsmodels.api as sm

class FeatureEngineer:
    @staticmethod
    def select_relevant_features(
            features_df: pd.DataFrame,
            targets_df: pd.DataFrame | pd.Series,
            corr_threshold: float = 0.2,
            variance_threshold: float = 1e-5
        ) -> list[str]:
        if isinstance(targets_df, pd.Series):
            targets_df = targets_df.to_frame()  # Преобразуем в DataFrame с одним столбцом

        relevant_features_set = set()

        for target_col in targets_df.columns:
            target = targets_df[target_col]
            # Корреляция признаков с текущей целевой переменной
            correlations = features_df.apply(lambda col: col.corr(target))

            # Фильтрация по абсолютной корреляции
            corr_filtered = correlations[correlations.abs() >= corr_threshold]

            # Фильтрация по дисперсии
            variances = features_df[corr_filtered.index].var()
            relevant_for_target = variances[variances >= variance_threshold].index.tolist()

            relevant_features_set.update(relevant_for_target)

        return sorted(relevant_features_set)

    @staticmethod
    def select_relevant_features_after_regression(
            features_df: pd.DataFrame,
            targets_df: pd.DataFrame,
            coefficients_df: pd.DataFrame,
            min_variance: float = 1e-4,
            min_normalized_coef: float = 0.05
    ) -> list[str]:
        # Отсечём признаки с низкой дисперсией
        feature_variances = features_df.var()
        high_variance_features = feature_variances[feature_variances > min_variance].index.tolist()

        # Отфильтруем коэффициенты только для этих признаков
        filtered_coefs = coefficients_df.loc[coefficients_df.index.intersection(high_variance_features)]

        # Нормализуем коэффициенты (по колонкам — т.е. по каждому target)
        normalized_abs_coefs = filtered_coefs.abs().div(filtered_coefs.abs().max())

        # Отбор признаков, у которых хотя бы по одному target нормализованный коэффициент >= порога
        is_relevant = (normalized_abs_coefs >= min_normalized_coef).any(axis=1)

        return is_relevant[is_relevant].index.tolist()