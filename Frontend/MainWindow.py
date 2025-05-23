from PyQt5.QtWidgets import QStackedWidget, QMainWindow

from Backend.Common.CalculationResult import CalculationResult
from Frontend.Screens.HomeScreen import HomeScreen
from Frontend.Screens.InputCalculationScreen import InputCalculationScreen
from Frontend.Screens.InputPredictionScreen import InputPredictionScreen
from Frontend.Screens.ProgressScreen import ProgressScreen
from Frontend.Screens.ResultScreen import ResultScreen
from Frontend.Services.ModelCalculationThread import ModelCalculationThread
from Frontend.Services.PredictionCalculationThread import PredictionCalculationThread
from Frontend.Widgets.RulesWidget import RulesWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("System Dynamic Model Finder")

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # Экраны
        self.home_screen = HomeScreen()
        self.input_calculation_screen = InputCalculationScreen()
        self.input_prediction_screen = InputPredictionScreen()
        self.progress_screen = ProgressScreen()
        self.result_screen = ResultScreen()
        self.rules_widget = RulesWidget()
        self.window = None

        self.home_screen.calculate_need.connect(self.show_input_calculation_screen)
        self.home_screen.prediction_need.connect(self.show_input_prediction_screen)
        self.home_screen.rules_need.connect(self.open_rules_window)

        self.input_calculation_screen.back_to_home.connect(self.show_home_screen)
        self.input_calculation_screen.start_calculation.connect(self.start_calculation)

        self.input_prediction_screen.back_to_home.connect(self.show_home_screen)
        self.input_prediction_screen.start_calculation.connect(self.start_prediction)

        self.result_screen.back_to_home.connect(self.show_home_screen)

        self.stack.addWidget(self.home_screen)
        self.stack.addWidget(self.input_calculation_screen)
        self.stack.addWidget(self.input_prediction_screen)
        self.stack.addWidget(self.progress_screen)
        self.stack.addWidget(self.result_screen)

    def reset_input_calculation_screen(self):
        self.input_calculation_screen.file_path_x_le.clear()
        self.input_calculation_screen.file_path_y_le.clear()
        self.input_calculation_screen.file_path_x = ""
        self.input_calculation_screen.file_path_y = ""
        self.input_calculation_screen.sd_simple_rbtn.setChecked(False)
        self.input_calculation_screen.sd_extended_rbtn.setChecked(False)

    def reset_input_prediction_screen(self):
        self.input_prediction_screen.file_path_x_le.clear()
        self.input_prediction_screen.file_path_x = ""
        self.input_prediction_screen.add_model_conf_widget.coefficients_le.clear()
        self.input_prediction_screen.add_model_conf_widget.func_lin_rbtn.setChecked(False)
        self.input_prediction_screen.add_model_conf_widget.func_exp_rbtn.setChecked(False)
        self.input_prediction_screen.add_model_conf_widget.func_quadro_rbtn.setChecked(False)
        self.input_prediction_screen.import_model_conf_widget.file_path_model_le.clear()
        self.input_prediction_screen.sd_simple_rbtn.setChecked(False)
        self.input_prediction_screen.sd_extended_rbtn.setChecked(False)

    def reset_progress_screen(self):
        self.progress_screen.log_te.clear()
        self.progress_screen.progressBar.setValue(0)

    def reset_result_screen(self):
        self.result_screen.table_result.clear()
        self.result_screen.equations_te.clear()

    def show_home_screen(self):
        self.stack.setCurrentWidget(self.home_screen)

    def show_input_calculation_screen(self):
        self.reset_input_calculation_screen()
        self.stack.setCurrentWidget(self.input_calculation_screen)

    def show_input_prediction_screen(self):
        self.reset_input_prediction_screen()
        self.stack.setCurrentWidget(self.input_prediction_screen)

    def show_progress_screen(self):
        self.reset_progress_screen()
        self.stack.setCurrentWidget(self.progress_screen)

    def open_rules_window(self):
        if self.window is None:
            self.window = QMainWindow()
            self.window.setCentralWidget(self.rules_widget)
            self.window.setWindowTitle("Правила использования")
            self.window.resize(500, 720)

        self.window.show()
        self.window.raise_()  # Поднимает окно наверх
        self.window.activateWindow()  # Фокус

    def show_result(self, result: CalculationResult):
        self.reset_result_screen()
        self.result_screen.set_data(result)
        self.stack.setCurrentWidget(self.result_screen)

    def start_calculation(self, path_x, path_y, is_extended):
        self.show_progress_screen()

        self.thread = ModelCalculationThread(path_x, path_y, is_extended)
        self.thread.progress_update.connect(self.progress_screen.update_progress)
        self.thread.log_update.connect(self.progress_screen.append_log)
        self.thread.calculation_done.connect(self.show_result)
        self.thread.start()

    def start_prediction(self, data):
        self.show_progress_screen()

        self.thread = PredictionCalculationThread(data)
        self.thread.progress_update.connect(self.progress_screen.update_progress)
        self.thread.log_update.connect(self.progress_screen.append_log)
        self.thread.calculation_done.connect(self.show_result)
        self.thread.start()
