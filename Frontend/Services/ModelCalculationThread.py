from Backend.MainService import MainService
from Frontend.Services.CalculationThread import CalculationThread


class ModelCalculationThread(CalculationThread):
    def __init__(self, path_x, path_y, is_extended):
        super().__init__()
        self.path_x = path_x
        self.path_y = path_y
        self.is_extended = is_extended

    def run(self):
        result = MainService.calculate_model(
            self.path_x,
            self.path_y,
            self.is_extended,
            progress_callback=self.update_progress,
            log_callback=self.update_log
        )

        self.calculation_done.emit(result)
