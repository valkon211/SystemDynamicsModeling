from Data.DataProvider import DataProvider
from Data.AnalyticsDataProvider import AnalyticsDataProvider
from RegressionModels.ModelEvaluation.ModelEvaluation import ModelEvaluation
from RegressionModels.MultRegressionType import MultRegressionType
from RegressionModels.MultipleRegressionCalculator import MultipleRegressionCalculator
from RegressionModels.Prediction.RegressionPredictor import RegressionPredictor

def main():
    # Считываем пути до файлов с таблицами фактов и целевых показателей
    facts_path = "facts.xls"#input("Введите путь к файлу с таблицей фактов: ")
    targets_path = "targets.xls"#input("Введите путь к файлу с таблицей целевых показателей: ")

    data_provider = DataProvider
    analytics_data = AnalyticsDataProvider(facts_path, targets_path)

    facts = analytics_data.get_facts()
    targets = analytics_data.get_targets()

    regression_calculator = MultipleRegressionCalculator(facts, targets)
    predictor = RegressionPredictor()

    correlation_matrix = analytics_data.get_correlation_matrix()
    data_provider.save_to_excel(correlation_matrix, "correlation_matrix")

    for model_type in MultRegressionType:
        print(f"{model_type}")

        theta = regression_calculator.get_theta(model_type)
        data_provider.save_to_excel(theta, f"{model_type.name}_coefficients")

        targets_prediction = predictor.predict(facts, theta, model_type)
        data_provider.save_to_excel(targets_prediction, f"{model_type.name}_prediction")
        analytics_data.add_prediction(targets_prediction, model_type.name)

        print(f"Оценка модели:")
        evaluator = ModelEvaluation(facts, targets, targets_prediction)
        eval_results = evaluator.evaluate()
        print(eval_results)

    predictions = analytics_data.get_merged_predictions()
    data_provider.save_to_excel(predictions, "models_prediction")


if __name__ == "__main__":
    main()
