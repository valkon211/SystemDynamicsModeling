from Backend.MainService import MainService
from Frontend.Services.CalculationThread import CalculationThread


class ModelCalculationThread(CalculationThread):
    def __init__(self, path_x, path_y):
        super().__init__()
        self.path_x = path_x
        self.path_y = path_y

    def run(self):
        result = MainService.calculate(
            self.path_x,
            self.path_y,
            progress_callback=self.update_progress,
            log_callback=self.update_log
        )

        self.calculation_done.emit(result)
