from Backend.Common.InputPredictionData import InputPredictionData
from Backend.MainService import MainService
from Frontend.Services.CalculationThread import CalculationThread


class PredictionCalculationThread(CalculationThread):
    def __init__(self, path_x=None, path_json=None, path_coef=None, features=None, model_type=None, is_extended=False):
        super().__init__()
        self.path_x = path_x
        self.path_json = path_json
        self.path_coef = path_coef
        self.features = features
        self.model_type = model_type
        self.is_extended = is_extended

    def run(self):
        data = None

        if self.path_x and self.path_json:
            data = InputPredictionData(
                path_x=self.path_x,
                json_data_path=self.path_json,
                is_extended=self.is_extended
            )

        if self.path_x and self.path_coef and self.features and self.model_type:
            data = InputPredictionData(
                path_x=self.path_x,
                path_coefficients=self.path_coef,
                model_type=self.model_type,
                relevant_features=self.features,
                is_extended=self.is_extended
            )

        result = MainService.get_prediction(
            data,
            progress_callback=self.update_progress,
            log_callback=self.update_log
        )

        self.calculation_done.emit(result)
