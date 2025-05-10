from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt


class Ui_InputPredictionScreen(object):
    def setupUi(self, main_screen):
        main_screen.setObjectName("main_screen")

        font = QtGui.QFont()
        font.setBold(True)

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
        self.main_widget.setMaximumSize(500, 500)
        self.centering_layout.addWidget(self.main_widget)

        # Добавляем растяжку справа
        self.centering_layout.addStretch(1)

        # Внутренний layout с выравниванием по центру
        self.main_layout = QtWidgets.QVBoxLayout(self.main_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(10)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)  # <--- Центрирование

        # Layout для импорта признаков
        self.import_features_layout = QtWidgets.QVBoxLayout()
        self.import_features_layout.setSpacing(10)

        # Метка для файла
        self.add_x_lbl = QtWidgets.QLabel(self.main_widget)
        self.add_x_lbl.setObjectName("add_x_lbl")
        self.import_features_layout.addWidget(self.add_x_lbl)

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

        self.import_features_layout.addLayout(self.add_file_x_layout)

        self.main_layout.addLayout(self.import_features_layout)

        # Ввод конфигурации модели
        self.model_config_layout = QtWidgets.QVBoxLayout()
        self.model_config_layout.setSpacing(10)

        self.model_config_lbl = QtWidgets.QLabel(self.main_widget)
        self.model_config_lbl.setObjectName("model_config_lbl")
        self.model_config_lbl.setFont(font)
        self.model_config_layout.addWidget(self.model_config_lbl)

        self.model_config_btn_layout = QtWidgets.QHBoxLayout()
        self.model_config_btn_layout.setSpacing(10)

        self.model_conf_import_btn = QtWidgets.QPushButton(self.main_widget)
        self.model_conf_import_btn.setObjectName("model_conf_import_btn")
        self.model_config_btn_layout.addWidget(self.model_conf_import_btn)

        self.model_conf_add_btn = QtWidgets.QPushButton(self.main_widget)
        self.model_conf_add_btn.setObjectName("model_conf_add_btn")
        self.model_config_btn_layout.addWidget(self.model_conf_add_btn)

        self.model_config_layout.addLayout(self.model_config_btn_layout)

        self.main_layout.addLayout(self.model_config_layout)

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
        self.model_config_lbl.setText(_translate("main_screen", "Конфигурация модели"))
        self.model_conf_import_btn.setText(_translate("main_screen", "Импорт из файла"))
        self.model_conf_add_btn.setText(_translate("main_screen", "Ввести вручную"))
        self.calculate_btn.setText(_translate("main_screen", "Рассчитать"))
        self.back_btn.setText(_translate("main_screen", "Назад"))
