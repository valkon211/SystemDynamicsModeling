from sklearn.model_selection import train_test_split

from Backend.Data.AnalyticsDataProvider import AnalyticsDataProvider
from Backend.Common.ModelType import ModelType
from Backend.Common.BestModelIdentifier import BestModelIdentifier
from Backend.MultipleRegression.MultipleRegressionModelCreator import MultipleRegressionModelCreator
from Backend.MultipleRegression.MultipleRegressionModelEvaluator import MultipleRegressionModelEvaluator
from Backend.SystemDynamics.SystemDynamicsModelEvaluator import SystemDynamicsModelEvaluator
from Backend.SystemDynamics.SystemDynamicsModelCreator import SystemDynamicsModelCreator


def main():
    facts_path = "././facts_v3.xlsx"  #input("Введите путь к файлу с таблицей фактов: ")
    targets_path = "././targets_v3.xlsx"  #input("Введите путь к файлу с таблицей целевых показателей: ")

    analytics_data = AnalyticsDataProvider(facts_path, targets_path)
    best_model_ident = BestModelIdentifier()
    mr_evaluator = MultipleRegressionModelEvaluator()
    sd_evaluator = SystemDynamicsModelEvaluator()

    facts = analytics_data.get_facts()
    targets = analytics_data.get_targets()

    X_train, X_test, y_train, y_test = train_test_split(facts, targets, test_size=0.2, random_state=42)

    mr_predictions = {}

    for model_type in ModelType:

        if model_type == ModelType.Polynomial:
            continue

        mr_model = MultipleRegressionModelCreator.create_model(X_train, y_train, model_type)
        prediction = mr_model.predict(X_test)
        mr_predictions[model_type] = prediction

    best_type = best_model_ident.determine_best_model(mr_evaluator.evaluate_models(y_test, mr_predictions))

    print(f"\nBest model: {best_type}")

    #sd_model = SystemDynamicsModelCreator.create_model(X_train, y_train, best_type)
    #print(sd_evaluator.evaluate(y_test, sd_model.predict(X_test)))

if __name__ == "__main__":
    main()
