from Backend.Data.AnalyticsDataProvider import AnalyticsDataProvider
from Backend.Common.ModelType import ModelType
from Backend.Common.BestModelIdentifier import BestModelIdentifier
from Backend.RegressionModels.MultipleRegressionModelCreator import MultipleRegressionModelCreator
from Backend.RegressionModels.MultipleRegressionModelEvaluator import MultipleRegressionModelEvaluator
from Backend.SystemDynamics.SystemDynamicsEvaluator import SystemDynamicsEvaluator
from Backend.SystemDynamics.SystemDynamicsModelCreator import SystemDynamicsModelCreator


def main():
    facts_path = "././facts.xls"  #input("Введите путь к файлу с таблицей фактов: ")
    targets_path = "././targets.xls"  #input("Введите путь к файлу с таблицей целевых показателей: ")

    analytics_data = AnalyticsDataProvider(facts_path, targets_path)
    best_model_ident = BestModelIdentifier()
    mr_evaluator = MultipleRegressionModelEvaluator()
    sd_evaluator = SystemDynamicsEvaluator()

    facts = analytics_data.get_facts()
    targets = analytics_data.get_targets()

    mr_predictions = {}

    for model_type in ModelType:
        mr_model = MultipleRegressionModelCreator.create_model(facts, targets, model_type)
        prediction = mr_model.predict(facts)
        mr_predictions[model_type] = prediction

    best_type = best_model_ident.determine_best_model(mr_evaluator.evaluate_models(targets, mr_predictions))

    sd_model = SystemDynamicsModelCreator.create_model(facts, targets, best_type)
    sd_prediction = sd_model.predict(facts)

    print(sd_evaluator.evaluate(targets, sd_prediction))

if __name__ == "__main__":
    main()
