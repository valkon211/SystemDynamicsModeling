import pandas as pd

class DataValidator:
    @staticmethod
    def validate(facts_df, targets_df):
        # Проверка, что таблицы не пустые
        if facts_df.empty:
            return False, "Таблица с фактами пуста."
        if targets_df.empty:
            return False, "Таблица с целевыми показателями пуста."

        # Проверка, что количество строк совпадает
        if len(facts_df) != len(targets_df):
            return False, f"Количество строк в таблицах не совпадает ({len(facts_df)} ≠ {len(targets_df)})."

        # Проверка, что все значения можно конвертировать в числа
        try:
            facts_df.apply(pd.to_numeric)
            targets_df.apply(pd.to_numeric)
        except ValueError:
            return False, "В таблицах есть неконвертируемые в число значения."

        # Проверка, что нет пустых значений
        if facts_df.isnull().values.any():
            return False, "В таблице с фактами есть пустые ячейки."
        if targets_df.isnull().values.any():
            return False, "В таблице с целевыми показателями есть пустые ячейки."

        return True, "Данные успешно прошли валидацию."
