from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_InputPredictionScreen(object):
    def setupUi(self, main_screen):
        main_screen.setObjectName("main_screen")

        # Внешний вертикальный layout
        self.outer_layout = QtWidgets.QVBoxLayout(main_screen)
        self.outer_layout.setContentsMargins(0, 0, 0, 0)

        # Центрирующий по горизонтали layout
        self.centering_layout = QtWidgets.QHBoxLayout()
        self.outer_layout.addLayout(self.centering_layout)

        # Добавляем растяжку слева
        self.centering_layout.addStretch(1)

        # Основной виджет
        self.main_widget = QtWidgets.QWidget(main_screen)
        self.main_widget.setMinimumSize(500, 0)
        self.main_widget.setMaximumSize(500, 300)
        self.centering_layout.addWidget(self.main_widget)

        # Добавляем растяжку справа
        self.centering_layout.addStretch(1)

        # Внутренний layout
        self.main_layout = QtWidgets.QVBoxLayout(self.main_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(10)

        # Метка для файла
        self.add_x_lbl = QtWidgets.QLabel(self.main_widget)
        self.add_x_lbl.setObjectName("add_x_lbl")
        self.main_layout.addWidget(self.add_x_lbl)

        # Layout для выбора файла
        self.add_file_x_layout = QtWidgets.QHBoxLayout()
        self.add_file_x_layout.setSpacing(10)

        self.file_path_x_le = QtWidgets.QLineEdit(self.main_widget)
        self.file_path_x_le.setText("")
        self.file_path_x_le.setReadOnly(True)
        self.file_path_x_le.setObjectName("file_path_x_le")
        self.add_file_x_layout.addWidget(self.file_path_x_le)

        self.add_x_path_btn = QtWidgets.QPushButton(self.main_widget)
        self.add_x_path_btn.setObjectName("add_x_path_btn")
        self.add_file_x_layout.addWidget(self.add_x_path_btn)

        self.main_layout.addLayout(self.add_file_x_layout)

        # Ввод признаков
        self.features_layout = QtWidgets.QHBoxLayout()
        self.features_layout.setSpacing(10)

        self.features_lbl = QtWidgets.QLabel(self.main_widget)
        self.features_lbl.setObjectName("features_lbl")
        self.features_layout.addWidget(self.features_lbl)

        self.features_le = QtWidgets.QLineEdit(self.main_widget)
        self.features_le.setObjectName("features_le")
        self.features_layout.addWidget(self.features_le)

        self.main_layout.addLayout(self.features_layout)

        # Ввод коэффициентов
        self.coefficients_lbl = QtWidgets.QLabel(self.main_widget)
        self.coefficients_lbl.setObjectName("coefficients_lbl")
        self.main_layout.addWidget(self.coefficients_lbl)

        self.coefficients_layout = QtWidgets.QHBoxLayout()
        self.coefficients_layout.setSpacing(10)

        self.coefficients_le = QtWidgets.QLineEdit(self.main_widget)
        self.coefficients_le.setObjectName("features_le")
        self.coefficients_le.setReadOnly(True)
        self.coefficients_layout.addWidget(self.coefficients_le)

        self.add_coef_path_btn = QtWidgets.QPushButton(self.main_widget)
        self.add_coef_path_btn.setObjectName("add_coef_path_btn")
        self.coefficients_layout.addWidget(self.add_coef_path_btn)

        self.main_layout.addLayout(self.coefficients_layout)

        # Выбор функции
        self.function_lbl = QtWidgets.QLabel(self.main_widget)
        self.function_lbl.setObjectName("function_lbl")
        self.main_layout.addWidget(self.function_lbl)

        self.func_lin_rbtn = QtWidgets.QRadioButton(self.main_widget)
        self.func_lin_rbtn.setObjectName("func_lin_rbtn")
        self.main_layout.addWidget(self.func_lin_rbtn)

        self.func_exp_rbtn = QtWidgets.QRadioButton(self.main_widget)
        self.func_exp_rbtn.setObjectName("func_exp_rbtn")
        self.main_layout.addWidget(self.func_exp_rbtn)

        self.func_quadro_rbtn = QtWidgets.QRadioButton(self.main_widget)
        self.func_quadro_rbtn.setObjectName("func_quadro_rbtn")
        self.main_layout.addWidget(self.func_quadro_rbtn)

        # Layout для кнопок
        self.buttons_layout = QtWidgets.QHBoxLayout()
        self.buttons_layout.setContentsMargins(0, 0, 0, 0)
        self.buttons_layout.setSpacing(10)

        self.back_btn = QtWidgets.QPushButton(self.main_widget)
        self.back_btn.setObjectName("back_btn")
        self.buttons_layout.addWidget(self.back_btn)

        self.calculate_btn = QtWidgets.QPushButton(self.main_widget)
        self.calculate_btn.setObjectName("calculate_btn")
        self.buttons_layout.addWidget(self.calculate_btn)

        self.main_layout.addLayout(self.buttons_layout)

        self.retranslateUi(main_screen)
        QtCore.QMetaObject.connectSlotsByName(main_screen)

    def retranslateUi(self, main_screen):
        _translate = QtCore.QCoreApplication.translate
        main_screen.setWindowTitle(_translate("main_screen", "Form"))
        self.add_x_lbl.setText(_translate("main_screen", "Файл с признаками"))
        self.add_x_path_btn.setText(_translate("main_screen", "Выбрать..."))
        self.add_coef_path_btn.setText(_translate("main_screen", "Выбрать..."))
        self.features_lbl.setText(_translate("main_screen", "Введите релевантные признаки:"))
        self.coefficients_lbl.setText(_translate("main_screen", "Файл с коэффициентами:"))
        self.function_lbl.setText(_translate("main_screen", "Выберите функцию:"))
        self.func_lin_rbtn.setText(_translate("main_screen", "Линейная"))
        self.func_exp_rbtn.setText(_translate("main_screen", "Экспоненциальная"))
        self.func_quadro_rbtn.setText(_translate("main_screen", "Квадратичная"))
        self.calculate_btn.setText(_translate("main_screen", "Рассчитать"))
        self.back_btn.setText(_translate("main_screen", "Назад"))
