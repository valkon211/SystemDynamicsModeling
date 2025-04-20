from sklearn.metrics import mean_absolute_error, r2_score

class ModelEvaluator:
    @staticmethod
    def mean_absolute_error(y_true, y_pred):
        return mean_absolute_error(y_true, y_pred)

    @staticmethod
    def wape(y_true, y_pred):
        return y_true.sub(y_pred).abs().sum() / y_true.abs().sum()

    @staticmethod
    def r2_score(y_true, y_pred):
        return r2_score(y_true, y_pred)