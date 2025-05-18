from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ResultScreen(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")

        self.outer_layout = QtWidgets.QVBoxLayout(Form)
        self.outer_layout.setContentsMargins(0, 0, 0, 0)

        self.centering_layout = QtWidgets.QHBoxLayout()
        self.outer_layout.addLayout(self.centering_layout)

        self.centering_layout.addStretch(1)

        self.main_widget = QtWidgets.QWidget(Form)
        self.centering_layout.addWidget(self.main_widget)
        self.centering_layout.addStretch(1)

        self.main_widget.setMinimumSize(600, 0)
        self.main_widget.setMaximumSize(600, 500)

        self.main_layout = QtWidgets.QVBoxLayout(self.main_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        # Кнопки
        self.btn_layout = QtWidgets.QHBoxLayout()
        self.btn_layout.setObjectName("btn_layout")
        self.back_btn = QtWidgets.QPushButton(self.main_widget)
        self.back_btn.setObjectName("back_btn")
        self.btn_layout.addWidget(self.back_btn)
        self.export_excel_btn = QtWidgets.QPushButton(self.main_widget)
        self.export_excel_btn.setObjectName("export_excel_btn")
        self.btn_layout.addWidget(self.export_excel_btn)
        self.export_json_btn = QtWidgets.QPushButton(self.main_widget)
        self.export_json_btn.setObjectName("export_json_btn")
        self.btn_layout.addWidget(self.export_json_btn)
        self.main_layout.addLayout(self.btn_layout)

        font = QtGui.QFont()
        font.setBold(True)

        # Метки
        self.lbl_layout = QtWidgets.QHBoxLayout()
        self.lbl_layout.setObjectName("lbl_layout")

        self.text_lbl = QtWidgets.QLabel(self.main_widget)
        self.text_lbl.setObjectName("text_lbl")
        self.text_lbl.setFont(font)
        self.lbl_layout.addWidget(self.text_lbl)

        self.result_lbl = QtWidgets.QLabel(self.main_widget)
        self.result_lbl.setObjectName("result_lbl")
        self.result_lbl.setFont(font)
        self.lbl_layout.addWidget(self.result_lbl)
        self.main_layout.addLayout(self.lbl_layout)

        self.equations_text_lbl = QtWidgets.QLabel(self.main_widget)
        self.equations_text_lbl.setObjectName("equations_text_lbl")
        self.equations_text_lbl.setFont(font)
        self.main_layout.addWidget(self.equations_text_lbl)

        self.equations_te = QtWidgets.QTextEdit(self.main_widget)
        self.equations_te.setReadOnly(True)
        self.equations_te.setObjectName("equations_te")
        self.main_layout.addWidget(self.equations_te)

        # Таблица
        self.table_result = QtWidgets.QTableWidget(self.main_widget)
        self.table_result.setObjectName("tableWidget")
        self.table_result.setColumnCount(0)
        self.table_result.setRowCount(0)
        self.main_layout.addWidget(self.table_result)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.back_btn.setText(_translate("Form", "На главную"))
        self.export_excel_btn.setText(_translate("Form", "Экспорт в excel"))
        self.export_json_btn.setText(_translate("Form", "Экспорт в json"))
        self.text_lbl.setText(_translate("Form", "Функция:"))
        self.result_lbl.setText(_translate("Form", ""))
        self.equations_text_lbl.setText(_translate("Form", "Уравнения:"))
