import sys

from PyQt5.QtWidgets import QApplication

from Frontend.MainWindow import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setFixedSize(800, 600)
    window.show()
    sys.exit(app.exec_())