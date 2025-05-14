from Backend.Common.InputPredictionData import InputPredictionData
from Backend.MainService import MainService
from Frontend.Services.CalculationThread import CalculationThread


class PredictionCalculationThread(CalculationThread):
    def __init__(self, data: InputPredictionData):
        super().__init__()
        self.data = data

    def run(self):
        result = MainService.get_prediction(
            self.data,
            progress_callback=self.update_progress,
            log_callback=self.update_log
        )

        self.calculation_done.emit(result)
