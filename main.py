from Data.DataProvider import DataProvider
from RegressionModels.ModelEvaluation.ModelEvaluation import ModelEvaluation
from RegressionModels.MultRegressionType import MultRegressionType
from RegressionModels.MultipleRegressionCalculator import MultipleRegressionCalculator
from RegressionModels.Prediction.RegressionPredictor import RegressionPredictor


def main():
    # Считываем пути до файлов с таблицами фактов и целевых показателей
    facts_path = "facts.xls"#input("Введите путь к файлу с таблицей фактов: ")
    targets_path = "targets.xls"#input("Введите путь к файлу с таблицей целевых показателей: ")

    # Загружаем данные
    data_provider = DataProvider(facts_path, targets_path)
    data_provider.load_data()

    facts = data_provider.get_facts()
    targets = data_provider.get_targets()

    regression_calculator = MultipleRegressionCalculator(facts, targets)
    predictor = RegressionPredictor()

    for model_type in MultRegressionType:
        print(f"{model_type}\n")

        theta = regression_calculator.get_theta(model_type)
        targets_pred = predictor.predict(facts, theta, model_type)

        print(f"Предсказание:\n{targets_pred}")
        print(f"Коэффициенты:\n{theta}")

        print(f"\nОценка модели {model_type}:")
        evaluator = ModelEvaluation(facts, targets, targets_pred)
        eval_results = evaluator.evaluate()
        print(eval_results)


if __name__ == "__main__":
    main()
