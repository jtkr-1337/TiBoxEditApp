from PyQt5 import uic


class ErrorDialog:
    standard_text = "Error! No subject has been selected!"

    def __init__(self):
        self.win = uic.loadUi("ui/dialog_gui.ui")

    def show(self, text=standard_text):
        self.win.label.setText(text)
        self.win.show()
