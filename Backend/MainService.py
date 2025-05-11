import pandas as pd
from sklearn.model_selection import train_test_split

from Backend.Common.CalculationResult import CalculationResult
from Backend.Common.InputPredictionData import InputPredictionData
from Backend.Data.AnalyticsDataProvider import AnalyticsDataProvider
from Backend.Common.ModelType import ModelType
from Backend.Common.BestModelIdentifier import BestModelIdentifier
from Backend.Data.DataProvider import DataProvider
from Backend.MultipleRegression.MultipleRegressionModel import MultipleRegressionModel
from Backend.MultipleRegression.MultipleRegressionModelCreator import MultipleRegressionModelCreator
from Backend.MultipleRegression.MultipleRegressionModelEvaluator import MultipleRegressionModelEvaluator
from Backend.SystemDynamics.ExtendedSystemDynamicModelCreator import ExtendedSystemDynamicModelCreator
from Backend.SystemDynamics.SystemDynamicsModelCreator import SystemDynamicModelCreator
from Backend.SystemDynamics.SystemDynamicsModelEvaluator import SystemDynamicsModelEvaluator


class MainService:
    @staticmethod
    def calculate_model(path_x, path_y, is_extended=False, progress_callback=None, log_callback=None):
        def update(progress, message):
            if progress_callback:
                progress_callback(progress)
            if log_callback:
                log_callback(message)

        best_model_ident = BestModelIdentifier()
        mr_evaluator = MultipleRegressionModelEvaluator()
        sd_evaluator = SystemDynamicsModelEvaluator()

        completed = 0
        update(completed, "Начинаем загрузку файлов...")

        analytics_data = AnalyticsDataProvider(path_x, path_y)

        completed = 5
        update(completed, "Файлы загружены. Начинаем обработку данных...")

        features = analytics_data.get_facts()
        targets = analytics_data.get_targets()

        X_train, X_test, y_train, y_test = train_test_split(features, targets, test_size=0.2, random_state=42)

        completed = 10
        update(completed, "Разделение выборки на тренировочную и тестовую завершено. Начинаем основную обработку...")

        mr_predictions = {}
        mr_models = {}
        for model_type in ModelType:
            mr_model = MultipleRegressionModelCreator.create_model(X_train, y_train, model_type)
            prediction = mr_model.predict(X_test)

            mr_models[model_type] = mr_model
            mr_predictions[model_type] = prediction

            completed += 10
            update(completed, f"Расчёт модели множественной регрессии типа {model_type.name} завершён.")

        completed = 50
        update(completed, f"Расчёт моделей множественной регрессии типа завершён.")
        update(completed, f"Начинаем анализ моделей множественной регрессии.")

        best_type = best_model_ident.determine_best_model(mr_evaluator.evaluate_models(y_test, mr_predictions))
        best_mr_model = mr_models[best_type]

        completed = 60
        update(completed, f"Анализ моделей множественной регрессии завершён.")
        update(completed, f"Начинаем построение модели системной динамики.")

        if is_extended:
            sd_creator = ExtendedSystemDynamicModelCreator()
            sd_model = sd_creator.create(features, targets, best_type)

            data = pd.concat([X_test, y_test], axis=1)
            sd_prediction = sd_model.predict(data.iloc[0], 1)
            sd_eval_result = sd_evaluator.evaluate(data.iloc[1], sd_prediction.iloc[1])

            print(sd_eval_result)

            update(100, "Расчёт завершён")

            return CalculationResult(
                result_df= sd_model.coefficients,
                model_type= sd_model.model_type.name,
                relevant_features= None,
                equations = sd_model.get_equation_strings(),
                json_data= sd_model.to_json())

        else:
            sd_creator = SystemDynamicModelCreator()
            sd_model = sd_creator.create(features, targets, best_type, best_mr_model.features)

            update(100, "Расчёт завершён")

            return CalculationResult(
                result_df=sd_model.coefficients,
                model_type=sd_model.model_type.name,
                relevant_features=sd_model.relevant_features,
                equations=sd_model.get_equation_strings(),
                json_data=sd_model.to_json())

    @staticmethod
    def get_prediction(data: InputPredictionData, progress_callback=None, log_callback=None):
        def update(progress, message):
            if progress_callback:
                progress_callback(progress)
            if log_callback:
                log_callback(message)

        if data.path_x and data.json_data_path:
            completed = 0
            update(completed, "Начинаем загрузку файлов...")

            X = DataProvider.read_table_file(data.path_x)
            X.columns = [f"x{i + 1}" for i in range(X.shape[1])]

            completed = 10
            update(completed, "Файл с признаками загружен")

            model_data = DataProvider.read_json_file(data.json_data_path)

            completed = 20
            update(completed, "Файл с данными о модели загружен")
            update(completed, "Начинаем обработку данных...")

            completed = 30
            update(completed, "Создание модели...")

            model = MultipleRegressionModelCreator.create_model_from_json(model_data)

            completed = 40
            update(completed, "Модель создана")

            completed = 50
            update(completed, "Начинаем вычислять целевые переменные...")

            prediction = model.predict(X)

            update(100, "Расчёт завершён")

            return CalculationResult(
                result_df=prediction,
                model_type=model.model_type.name,
                equations=model.get_equations())

        if data.path_x and data.path_coefficients and data.model_type and data.relevant_features:
            completed = 0
            update(completed, "Начинаем загрузку файлов...")

            X = DataProvider.read_table_file(data.path_x)
            X.columns = [f"x{i + 1}" for i in range(X.shape[1])]

            completed = 10
            update(completed, "Файл с признаками загружен")

            coefficients = DataProvider.read_table_file(data.path_coefficients, True)

            completed = 20
            update(completed, "Файл с коэффициентами загружен")
            update(completed, "Начинаем обработку данных...")

            completed = 30
            update(completed, "Создание модели...")

            model = MultipleRegressionModel(coefficients, data.relevant_features, data.model_type)

            completed = 40
            update(completed, "Модель создана")
            update(completed, "Начинаем вычислять целевые переменные...")

            prediction = model.predict(X)

            update(100, "Расчёт завершён")

            return CalculationResult(
                result_df=prediction,
                model_type=model.model_type.name,
                equations=model.get_equations())

    @staticmethod
    def export_to_excel(df: pd.DataFrame, filepath: str = None):
        DataProvider.save_to_excel(df, filepath)

    @staticmethod
    def export_to_json(data, filepath: str = None):
        DataProvider.save_to_json(data, filepath)



if __name__ == '__main__':
    features_path = ""
    targets_path = ""

    best_model_ident = BestModelIdentifier()
    mr_evaluator = MultipleRegressionModelEvaluator()
    sd_creator = SystemDynamicModelCreator()
    sd_evaluator = SystemDynamicsModelEvaluator()

    analytics_data = AnalyticsDataProvider(features_path, targets_path)
    features = analytics_data.get_facts()
    targets = analytics_data.get_targets()

    X_train, X_test, y_train, y_test = train_test_split(features, targets, test_size=0.2, random_state=42)

    mr_predictions = {}
    mr_models = {}
    for model_type in ModelType:
        mr_model = MultipleRegressionModelCreator.create_model(X_train, y_train, model_type)
        prediction = mr_model.predict(X_test)

        mr_models[model_type] = mr_model
        mr_predictions[model_type] = prediction

    best_type = best_model_ident.determine_best_model(mr_evaluator.evaluate_models(y_test, mr_predictions))
    best_mr_model = mr_models[best_type]

    print("best model type:\t", best_type)
    print("features:\t", best_mr_model.features)
    print("coefficients:\n", best_mr_model.coefficients)

    sd_model = sd_creator.create(X_train, y_train, best_type, best_mr_model.features)

    sd_prediction = sd_model.predict(X_test)

    print(sd_evaluator.evaluate(y_test, sd_prediction))
