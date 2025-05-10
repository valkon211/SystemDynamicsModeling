from PyQt5 import QtWidgets, QtCore


class Ui_ImportModelConfigurationWidget(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")

        # Создаём внешний контейнер для центрирования
        self.outer_layout = QtWidgets.QVBoxLayout(Form)
        self.outer_layout.setContentsMargins(0, 0, 0, 0)

        # Центрирующий контейнер по горизонтали
        self.centering_layout = QtWidgets.QHBoxLayout()
        self.outer_layout.addLayout(self.centering_layout)

        # Основной виджет с содержимым
        self.main_widget = QtWidgets.QWidget(Form)
        self.centering_layout.addWidget(self.main_widget)

        self.model_import_layout = QtWidgets.QVBoxLayout(self.main_widget)
        self.model_import_layout.setSpacing(10)

        self.model_import_lbl = QtWidgets.QLabel(self.main_widget)
        self.model_import_lbl.setObjectName("model_import_lbl")
        self.model_import_layout.addWidget(self.model_import_lbl)

        # Layout для выбора файла
        self.add_file_model_layout = QtWidgets.QHBoxLayout()
        self.add_file_model_layout.setSpacing(10)

        self.file_path_model_le = QtWidgets.QLineEdit(self.main_widget)
        self.file_path_model_le.setText("")
        self.file_path_model_le.setReadOnly(True)
        self.file_path_model_le.setObjectName("file_path_model_le")
        self.add_file_model_layout.addWidget(self.file_path_model_le)

        self.add_model_path_btn = QtWidgets.QPushButton(self.main_widget)
        self.add_model_path_btn.setObjectName("add_model_path_btn")
        self.add_file_model_layout.addWidget(self.add_model_path_btn)

        self.model_import_layout.addLayout(self.add_file_model_layout)

        self.centering_layout.addLayout(self.model_import_layout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, form):
        _translate = QtCore.QCoreApplication.translate
        form.setWindowTitle(_translate("form", "Form"))
        self.model_import_lbl.setText(_translate("form", "Файл с конфигурацией модели"))
        self.add_model_path_btn.setText(_translate("form", "Выбрать..."))