from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ProgressScreen(object):
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

        self.main_widget.setMinimumSize(500, 0)
        self.main_widget.setMaximumSize(500, 400)

        self.main_layout = QtWidgets.QVBoxLayout(self.main_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.progress_lbl = QtWidgets.QLabel(self.main_widget)
        self.progress_lbl.setObjectName("progress_lbl")
        self.main_layout.addWidget(self.progress_lbl)

        self.progressBar = QtWidgets.QProgressBar(self.main_widget)
        self.progressBar.setObjectName("progressBar")
        self.main_layout.addWidget(self.progressBar)

        self.log_te = QtWidgets.QTextEdit(self.main_widget)
        self.log_te.setReadOnly(True)
        self.log_te.setObjectName("log_te")
        self.main_layout.addWidget(self.log_te)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.progress_lbl.setText(_translate("Form", "Идут вычисления..."))
