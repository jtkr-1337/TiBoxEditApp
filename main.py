from PyQt5 import QtWidgets, uic
from start_win import StartGUI
import sys


app = QtWidgets.QApplication([])

start_win = StartGUI()
start_win.start()

sys.exit(app.exec_())
