from PyQt5 import QtWidgets, QtCore


class Ui_AddModelConfigurationForm(object):
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

        self.model_conf_form_layout = QtWidgets.QVBoxLayout(self.main_widget)
        self.model_conf_form_layout.setSpacing(10)

        self.features_layout = QtWidgets.QHBoxLayout()
        self.features_layout.setSpacing(10)

        self.features_lbl = QtWidgets.QLabel(self.main_widget)
        self.features_lbl.setObjectName("features_lbl")
        self.features_layout.addWidget(self.features_lbl)

        self.features_le = QtWidgets.QLineEdit(self.main_widget)
        self.features_le.setObjectName("features_le")
        self.features_layout.addWidget(self.features_le)

        self.model_conf_form_layout.addLayout(self.features_layout)

        # Ввод коэффициентов
        self.coefficients_lbl = QtWidgets.QLabel(self.main_widget)
        self.coefficients_lbl.setObjectName("coefficients_lbl")
        self.model_conf_form_layout.addWidget(self.coefficients_lbl)

        self.coefficients_layout = QtWidgets.QHBoxLayout()
        self.coefficients_layout.setSpacing(10)

        self.coefficients_le = QtWidgets.QLineEdit(self.main_widget)
        self.coefficients_le.setObjectName("features_le")
        self.coefficients_le.setReadOnly(True)
        self.coefficients_layout.addWidget(self.coefficients_le)

        self.add_coef_path_btn = QtWidgets.QPushButton(self.main_widget)
        self.add_coef_path_btn.setObjectName("add_coef_path_btn")
        self.coefficients_layout.addWidget(self.add_coef_path_btn)

        self.model_conf_form_layout.addLayout(self.coefficients_layout)

        # Выбор функции
        self.func_chose_layout = QtWidgets.QVBoxLayout(self.main_widget)
        self.func_chose_layout.setSpacing(10)

        self.function_lbl = QtWidgets.QLabel(self.main_widget)
        self.function_lbl.setObjectName("function_lbl")
        self.func_chose_layout.addWidget(self.function_lbl)

        self.func_lin_rbtn = QtWidgets.QRadioButton(self.main_widget)
        self.func_lin_rbtn.setObjectName("func_lin_rbtn")
        self.func_chose_layout.addWidget(self.func_lin_rbtn)

        self.func_exp_rbtn = QtWidgets.QRadioButton(self.main_widget)
        self.func_exp_rbtn.setObjectName("func_exp_rbtn")
        self.func_chose_layout.addWidget(self.func_exp_rbtn)

        self.func_quadro_rbtn = QtWidgets.QRadioButton(self.main_widget)
        self.func_quadro_rbtn.setObjectName("func_quadro_rbtn")
        self.func_chose_layout.addWidget(self.func_quadro_rbtn)

        self.model_conf_form_layout.addLayout(self.func_chose_layout)

        self.centering_layout.addLayout(self.model_conf_form_layout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, form):
        _translate = QtCore.QCoreApplication.translate
        form.setWindowTitle(_translate("form", "Form"))
        self.add_coef_path_btn.setText(_translate("form", "Выбрать..."))
        self.features_lbl.setText(_translate("form", "Релевантные признаки:"))
        self.coefficients_lbl.setText(_translate("form", "Файл с коэффициентами:"))
        self.function_lbl.setText(_translate("form", "Функция:"))
        self.func_lin_rbtn.setText(_translate("form", "Линейная"))
        self.func_exp_rbtn.setText(_translate("form", "Экспоненциальная"))
        self.func_quadro_rbtn.setText(_translate("form", "Квадратичная"))