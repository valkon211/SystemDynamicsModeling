from PyQt5.QtWidgets import QWidget

from Frontend.UI.Ui_RulesWidget import Ui_RulesWidget


class RulesWidget(QWidget, Ui_RulesWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)