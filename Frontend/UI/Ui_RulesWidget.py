from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_RulesWidget(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")

        # Создаём внешний контейнер для центрирования
        self.outer_layout = QtWidgets.QVBoxLayout(Form)
        self.outer_layout.setContentsMargins(0, 0, 0, 0)

        # Центрирующий контейнер по горизонтали
        self.centering_layout = QtWidgets.QHBoxLayout()
        self.outer_layout.addLayout(self.centering_layout)

        self.centering_layout.addStretch(1)

        # Основной виджет с содержимым
        self.main_widget = QtWidgets.QWidget(Form)
        self.centering_layout.addWidget(self.main_widget)
        self.centering_layout.addStretch(1)

        # Основной вертикальный layout
        self.verticalLayout = QtWidgets.QVBoxLayout(self.main_widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        # Метки и текстовые поля
        self.how_coef_lbl = QtWidgets.QLabel(self.main_widget)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.how_coef_lbl.setFont(font)
        self.how_coef_lbl.setObjectName("how_coef_lbl")
        self.verticalLayout.addWidget(self.how_coef_lbl)

        self.how_coef_te = QtWidgets.QPlainTextEdit(self.main_widget)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.how_coef_te.setFont(font)
        self.how_coef_te.setReadOnly(True)
        self.how_coef_te.setObjectName("how_coef_te")
        self.verticalLayout.addWidget(self.how_coef_te)

        self.how_targets_lbl = QtWidgets.QLabel(self.main_widget)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.how_targets_lbl.setFont(font)
        self.how_targets_lbl.setObjectName("how_targets_lbl")
        self.verticalLayout.addWidget(self.how_targets_lbl)

        self.how_targets_te = QtWidgets.QPlainTextEdit(self.main_widget)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.how_targets_te.setFont(font)
        self.how_targets_te.setReadOnly(True)
        self.how_targets_te.setObjectName("how_targets_te")
        self.verticalLayout.addWidget(self.how_targets_te)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.how_coef_lbl.setText(_translate("Form", "Как получить коэффициенты?"))
        self.how_coef_te.setPlainText(_translate("Form", "1. Нажмите кнопку \"Рассчитать модель\".\n"
"2. Загрузите файл с данными о признаках (features)*.\n"
"3. Загрузите файл с данными о целевых переменных (targets)*.\n"
"4. Нажмите кнопку \"Рассчитать\".\n"
"5. После проведения рассчетов на экране появятся данные с коэффициентами модели системной динамики.\n"
"6. При желании можете экспортировать коэффициенты в excel-таблицу, нажав кнопку \"Экспорт в excel\"\n"
"\n"
"*Поддерживаются файлы следующих форматов: .xls, .xlsx, .csv"))
        self.how_targets_lbl.setText(_translate("Form", "Как предсказать целевые переменные?"))
        self.how_targets_te.setPlainText(_translate("Form", "1. Нажмите кнопку \"Предсказать целевые переменные\".\n"
"2. Загрузите файл с данными о признаках (features)*.\n"
"3. Загрузите файл с коэффициентами для модели системной динамики*.\n"
"4. Нажмите на кнопку \"Рассчитать\".\n"
"5. После проведения рассчетов на экране появится предсказанные значения целевых переменных.\n"
"6. При желании можете экспортировать результат в excel-таблицу, нажав кнопку \"Экспорт в excel\"\n"
"\n"
"*Поддерживаются файлы следующих форматов: .xls, .xlsx, .csv"))
