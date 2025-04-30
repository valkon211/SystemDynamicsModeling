from Backend.MainService import MainService
from Frontend.Services.CalculationThread import CalculationThread


class PredictionCalculationThread(CalculationThread):
    def __init__(self, path_x, path_coef, features, model_type):
        super().__init__()
        self.path_x = path_x
        self.path_coef = path_coef
        self.features = features
        self.model_type = model_type

    def run(self):
        result = MainService.get_prediction(
            self.path_x,
            self.path_coef,
            self.features,
            self.model_type,
            progress_callback=self.update_progress,
            log_callback=self.update_log
        )

        self.calculation_done.emit(result)
