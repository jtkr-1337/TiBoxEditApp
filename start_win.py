from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import Qt, QTimer
from PyQt5 import QtWidgets, uic
from start_gui import Ui_MainWindow
from main_app import MainApp
from api_connector import API_Connector


class StartGUI(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint)

        self._old_pos = None
        api = API_Connector()
        groups = api.get_groups()
        self.dialog = StartWidget(groups)

        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.close_and_open_next)
        self.timer.start(1500)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._old_pos = event.pos()
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._old_pos = None
    def mouseMoveEvent(self, event):
        if not self._old_pos:
            return
        delta = event.pos() - self._old_pos
        self.move(self.pos() + delta)

    def start(self):
        self.show()

    def close_and_open_next(self):
        self.close()
        self.dialog.exec_()


class StartWidget(QtWidgets.QDialog):
    def __init__(self, groups):
        super().__init__()
        uic.loadUi("ui/load_gui.ui", self)

        for i in range(len(groups)):
            self.comboBox.addItem(groups[i]['text'], groups[i])


        self.buttonBox.accepted.connect(self.my_accept)
        self.buttonBox.rejected.connect(self.my_reject)

        self.main = MainApp()

    def my_accept(self):
        self.main.show(self.comboBox.itemData(self.comboBox.currentIndex()))
        self.accept()

    def my_reject(self):
        self.reject()
