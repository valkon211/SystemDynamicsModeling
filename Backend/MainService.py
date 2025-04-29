import pandas as pd
from sklearn.model_selection import train_test_split

from Backend.Common.CalculationResult import CalculationResult
from Backend.Data.AnalyticsDataProvider import AnalyticsDataProvider
from Backend.Common.ModelType import ModelType
from Backend.Common.BestModelIdentifier import BestModelIdentifier
from Backend.Data.DataProvider import DataProvider
from Backend.MultipleRegression.MultipleRegressionModelCreator import MultipleRegressionModelCreator
from Backend.MultipleRegression.MultipleRegressionModelEvaluator import MultipleRegressionModelEvaluator
from Backend.SystemDynamics.SystemDynamicsModelEvaluator import SystemDynamicsModelEvaluator
from Backend.SystemDynamics.SystemDynamicsModelCreator import SystemDynamicsModelCreator

class MainService:
    @staticmethod
    def calculate(path_x, path_y, progress_callback=None, log_callback=None):
        def update(progress, message):
            if progress_callback:
                progress_callback(progress)
            if log_callback:
                log_callback(message)

        best_model_ident = BestModelIdentifier()
        mr_evaluator = MultipleRegressionModelEvaluator()

        completed = 0

        update(completed, "Начинаем загрузку файлов...")

        analytics_data = AnalyticsDataProvider(path_x, path_y)
        completed += 5

        update(completed, "Файлы загружены. Начинаем обработку данных...")

        facts = analytics_data.get_facts()
        targets = analytics_data.get_targets()

        X_train, X_test, y_train, y_test = train_test_split(facts, targets, test_size=0.2, random_state=42)
        completed += 5

        update(completed, "Разделение выборки на тренировочную и тестовую завершено. Начинаем основную обработку...")

        mr_predictions = {}

        for model_type in ModelType:

            if model_type == ModelType.Polynomial:
                continue

            mr_model = MultipleRegressionModelCreator.create_model(X_train, y_train, model_type)
            prediction = mr_model.predict(X_test)
            mr_predictions[model_type] = prediction
            completed += 10

            update(completed, f"Расчёт модели множественной регрессии типа {model_type.name} завершён.")

        best_type = best_model_ident.determine_best_model(mr_evaluator.evaluate_models(y_test, mr_predictions))

        update(100, "Расчёт завершён")

        return CalculationResult(MultipleRegressionModelCreator.create_model(X_train, y_train, best_type).coefficients, best_type.name)

    @staticmethod
    def export_to_excel(df: pd.DataFrame, file_path: str = None):
        DataProvider.save_to_excel(df, file_path)