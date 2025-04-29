from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt


class Ui_HomeScreen(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")

        # Основной layout — центрирует всё содержимое
        self.outer_layout = QtWidgets.QVBoxLayout(Form)
        self.outer_layout.setContentsMargins(0, 0, 0, 0)
        self.outer_layout.setSpacing(0)

        # Вставка растяжек для вертикального центрирования
        self.outer_layout.addStretch(1)

        # Центральный контейнер
        self.central_widget = QtWidgets.QWidget(Form)
        self.central_layout = QtWidgets.QVBoxLayout(self.central_widget)
        self.central_layout.setContentsMargins(40, 40, 40, 40)
        self.central_layout.setSpacing(20)
        self.central_layout.setAlignment(Qt.AlignCenter)

        self.logo_lbl = QtWidgets.QLabel(self.central_widget)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        font.setBold(True)
        self.logo_lbl.setFont(font)
        self.logo_lbl.setAlignment(Qt.AlignCenter)
        self.central_layout.addWidget(self.logo_lbl)

        self.calculate_model_btn = QtWidgets.QPushButton(self.central_widget)
        self.central_layout.addWidget(self.calculate_model_btn)

        self.get_prediction_btn = QtWidgets.QPushButton(self.central_widget)
        self.central_layout.addWidget(self.get_prediction_btn)

        self.rules_btn = QtWidgets.QPushButton(self.central_widget)
        self.central_layout.addWidget(self.rules_btn)

        # Горизонтальное центрирование
        hbox = QtWidgets.QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.central_widget)
        hbox.addStretch(1)

        self.outer_layout.addLayout(hbox)
        self.outer_layout.addStretch(1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "System Dynamic Model Finder"))
        self.logo_lbl.setText(_translate("Form", "System Dynamic Model Finder"))
        self.calculate_model_btn.setText(_translate("Form", "Рассчитать модель"))
        self.get_prediction_btn.setText(_translate("Form", "Предсказать целевые переменные"))
        self.rules_btn.setText(_translate("Form", "Как пользоваться утилитой?"))
