from Data.DataProvider import DataProvider
from Data.AnalyticsDataProvider import AnalyticsDataProvider
from ModelType import ModelType
from RegressionModels.BestModelIdentifier import BestModelIdentifier
from RegressionModels.MultipleRegressionFitter import MultipleRegressionFitter
from RegressionModels.MultipleRegressionModelEvaluator import MultipleRegressionModelEvaluator
from RegressionModels.MultipleRegressionPredictor import MultipleRegressionPredictor
from SystemDynamics.SystemDynamicsEvaluator import SystemDynamicsEvaluator
from SystemDynamics.SystemDynamicsFitter import SystemDynamicsFitter


def main():
    facts_path = "facts_v3.xlsx"#input("Введите путь к файлу с таблицей фактов: ")
    targets_path = "targets_v3.xlsx"#input("Введите путь к файлу с таблицей целевых показателей: ")

    data_provider = DataProvider
    analytics_data = AnalyticsDataProvider(facts_path, targets_path)

    facts = analytics_data.get_facts()
    targets = analytics_data.get_targets()

    regression_calculator = MultipleRegressionFitter(facts, targets)
    predictor = MultipleRegressionPredictor()

    correlation_matrix = analytics_data.get_correlation_matrix()
    data_provider.save_to_excel(correlation_matrix, "correlation_matrix")

    for model_type in ModelType:
        theta = regression_calculator.get_theta(model_type)
        data_provider.save_to_excel(theta, f"{model_type.name}_coefficients")

        targets_prediction = predictor.predict(facts, theta, model_type)
        data_provider.save_to_excel(targets_prediction, f"{model_type.name}_prediction")
        analytics_data.add_prediction(targets_prediction, model_type)

    predictions = analytics_data.get_merged_predictions()
    data_provider.save_to_excel(predictions, "models_prediction")

    mult_reg_evaluator = MultipleRegressionModelEvaluator()
    model_evaluation = mult_reg_evaluator.evaluate_models(targets, analytics_data.get_predictions())

    best_model_identifier = BestModelIdentifier()
    best_model = best_model_identifier.determine_best_model(model_evaluation)

    print(f"Лучшая модель: {best_model}")

    sys_dynamics_fitter = SystemDynamicsFitter()
    sys_dynamics_model = sys_dynamics_fitter.fit(facts, targets, best_model)

    sys_dynamics_evaluator = SystemDynamicsEvaluator()
    sys_dynamics_prediction = sys_dynamics_model.predict(facts)
    data_provider.save_to_excel(sys_dynamics_prediction, "sys_dynamics_model_prediction")
    sys_dynamics_evaluation = sys_dynamics_evaluator.evaluate(targets, sys_dynamics_prediction)

    print(sys_dynamics_evaluation)

if __name__ == "__main__":
    main()
