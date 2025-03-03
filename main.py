from Data.DataProvider import DataProvider
from Data.DataValidator import DataValidator
from RegressionModels.ModelEvaluation.ModelEvaluation import ModelEvaluation
from RegressionModels.MultRegressionType import MultRegressionType
from RegressionModels.MultipleRegressionCalculator import MultipleRegressionCalculator
from RegressionModels.Prediction.RegressionPredictor import RegressionPredictor


def main():
    # Считываем пути до файлов с таблицами фактов и целевых показателей
    facts_path = input("Введите путь к файлу с таблицей фактов: ")
    targets_path = input("Введите путь к файлу с таблицей целевых показателей: ")

    # Загружаем данные
    data_provider = DataProvider(facts_path, targets_path)
    data_provider.load_data()

    facts = data_provider.get_features_array()
    targets = data_provider.get_targets_array()

    facts_df = data_provider.get_facts_df()
    targets_df = data_provider.get_targets_df()

    # Вычисляем коэффициенты множественной регрессии для всех типов уравнений
    regression_calculator = MultipleRegressionCalculator()

    models = {
        MultRegressionType.Linear: regression_calculator.linear_regression(facts, targets),
        MultRegressionType.Polynomial: regression_calculator.polynomial_regression(facts, targets),
        MultRegressionType.Exponential: regression_calculator.exponential_regression(facts, targets),
        MultRegressionType.Quadratic: regression_calculator.quadratic_regression(facts, targets)
    }

    # Оцениваем каждую модель
    predictor = RegressionPredictor()

    for model_type, coefficients in models.items():
        print(f"\nОценка модели {model_type}:")

        # Предсказанные значения
        predicted_values = predictor.predict(facts_df, model_type, coefficients)
        print(predicted_values)

        # Вычисляем метрики
        evaluator = ModelEvaluation(facts_df, targets_df, predicted_values)

        ar = evaluator.ar()
        wape = evaluator.wape()
        r_squared = evaluator.r_squared()
        std_error = evaluator.standard_error()
        f_stat = evaluator.f_statistic()

        # Вывод результатов

        print(f"AR: {ar}")
        print(f"WAPE: {wape}")
        print(f"Коэффициент детерминации R²: {r_squared}")
        print(f"Стандартная ошибка коэффициентов: {std_error}")
        print(f"F-статистика: {f_stat}")


if __name__ == "__main__":
    main()
