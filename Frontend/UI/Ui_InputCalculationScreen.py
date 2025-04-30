from PyQt5 import QtCore, QtWidgets


class Ui_InputCalculationScreen(object):
    def setupUi(self, main_screen):
        main_screen.setObjectName("main_screen")

        # Создаем внешний вертикальный layout
        self.outer_layout = QtWidgets.QVBoxLayout(main_screen)
        self.outer_layout.setContentsMargins(0, 0, 0, 0)

        # Центрируем layout
        self.centering_layout = QtWidgets.QHBoxLayout()
        self.outer_layout.addLayout(self.centering_layout)

        # Добавляем растяжку слева и справа для центрирования
        self.centering_layout.addStretch(1)

        # Основной виджет, который будет содержать все элементы
        self.main_widget = QtWidgets.QWidget(main_screen)
        self.main_widget.setMinimumSize(500, 0)
        self.main_widget.setMaximumSize(500, 200)
        self.centering_layout.addWidget(self.main_widget)

        # Добавляем растяжку справа для центрирования
        self.centering_layout.addStretch(1)

        # Основной вертикальный layout для элементов внутри main_widget
        self.main_layout = QtWidgets.QVBoxLayout(self.main_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(10)  # Расстояние между элементами

        # Элементы в layout

        # Метка для файла с признаками
        self.add_x_lbl = QtWidgets.QLabel(self.main_widget)
        self.add_x_lbl.setObjectName("add_x_lbl")
        self.main_layout.addWidget(self.add_x_lbl)

        # Layout для файла с признаками
        self.add_file_x_layout = QtWidgets.QHBoxLayout()
        self.add_file_x_layout.setContentsMargins(0, 0, 0, 0)
        self.add_file_x_layout.setSpacing(10)

        self.file_path_x_le = QtWidgets.QLineEdit(self.main_widget)
        self.file_path_x_le.setReadOnly(True)
        self.file_path_x_le.setObjectName("file_path_x_le")
        self.add_file_x_layout.addWidget(self.file_path_x_le)

        self.add_x_path_btn = QtWidgets.QPushButton(self.main_widget)
        self.add_x_path_btn.setObjectName("add_x_path_btn")
        self.add_file_x_layout.addWidget(self.add_x_path_btn)

        self.main_layout.addLayout(self.add_file_x_layout)

        # Метка для файла с целевыми переменными
        self.add_y_lbl = QtWidgets.QLabel(self.main_widget)
        self.add_y_lbl.setObjectName("add_y_lbl")
        self.main_layout.addWidget(self.add_y_lbl)

        # Layout для файла с целевыми переменными
        self.add_file_y_layout = QtWidgets.QHBoxLayout()
        self.add_file_y_layout.setContentsMargins(0, 0, 0, 0)
        self.add_file_y_layout.setSpacing(10)

        self.file_path_y_le = QtWidgets.QLineEdit(self.main_widget)
        self.file_path_y_le.setReadOnly(True)
        self.file_path_y_le.setObjectName("file_path_y_le")
        self.add_file_y_layout.addWidget(self.file_path_y_le)

        self.add_y_path_btn = QtWidgets.QPushButton(self.main_widget)
        self.add_y_path_btn.setObjectName("add_y_path_btn")
        self.add_file_y_layout.addWidget(self.add_y_path_btn)

        self.main_layout.addLayout(self.add_file_y_layout)

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

        # Перевод текста
        self.retranslateUi(main_screen)

        # Подключаем все слоты
        QtCore.QMetaObject.connectSlotsByName(main_screen)

    def retranslateUi(self, main_screen):
        _translate = QtCore.QCoreApplication.translate
        main_screen.setWindowTitle(_translate("main_screen", "Form"))
        self.add_x_lbl.setText(_translate("main_screen", "Файл с признаками"))
        self.add_x_path_btn.setText(_translate("main_screen", "Выбрать..."))
        self.add_y_lbl.setText(_translate("main_screen", "Файл с целевыми переменными"))
        self.add_y_path_btn.setText(_translate("main_screen", "Выбрать..."))
        self.calculate_btn.setText(_translate("main_screen", "Рассчитать"))
        self.back_btn.setText(_translate("main_screen", "Назад"))

