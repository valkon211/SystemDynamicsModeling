from PyQt5.QtWidgets import QStackedWidget, QMainWindow

from Backend.Common.CalculationResult import CalculationResult
from Frontend.Screens.HomeScreen import HomeScreen
from Frontend.Screens.InputCalculationScreen import InputCalculationScreen
from Frontend.Screens.ProgressScreen import ProgressScreen
from Frontend.Screens.ResultScreen import ResultScreen
from Frontend.Services.ModelCalculationThread import ModelCalculationThread
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
        self.progress_screen = ProgressScreen()
        self.result_screen = ResultScreen()
        self.rules_widget = RulesWidget()
        self.window = None

        self.home_screen.calculate_model_btn.clicked.connect(self.show_input_calculation_screen)
        self.home_screen.rules_btn.clicked.connect(self.open_rules_window)
        self.input_calculation_screen.back_btn.clicked.connect(self.show_home_screen)
        self.input_calculation_screen.start_calculation.connect(self.start_calculation)
        self.result_screen.back_to_main.connect(self.show_home_screen)

        self.stack.addWidget(self.home_screen)
        self.stack.addWidget(self.input_calculation_screen)
        self.stack.addWidget(self.progress_screen)
        self.stack.addWidget(self.result_screen)

    def reset_input_calculation_screen(self):
        self.input_calculation_screen.file_path_x_le.clear()
        self.input_calculation_screen.file_path_y_le.clear()
        self.input_calculation_screen.file_path_x = ""
        self.input_calculation_screen.file_path_y = ""

    def reset_progress_screen(self):
        self.progress_screen.log_te.clear()
        self.progress_screen.progressBar.setValue(0)

    def show_home_screen(self):
        self.stack.setCurrentWidget(self.home_screen)

    def show_input_calculation_screen(self):
        self.reset_input_calculation_screen()
        self.stack.setCurrentWidget(self.input_calculation_screen)

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
        self.result_screen.set_dataframe(result.result_df)
        self.result_screen.set_func_name(result.result_func)
        self.stack.setCurrentWidget(self.result_screen)

    def start_calculation(self, path_x, path_y):
        self.show_progress_screen()

        self.thread = ModelCalculationThread(path_x, path_y)
        self.thread.progress_update.connect(self.progress_screen.update_progress)
        self.thread.log_update.connect(self.progress_screen.append_log)
        self.thread.calculation_done.connect(self.show_result)
        self.thread.start()