import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QListWidget


class SearchApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Поиск по списку')

        # Создание виджетов
        self.layout = QVBoxLayout()
        self.search_bar = QLineEdit(self)
        self.list_widget = QListWidget(self)

        # Список элементов
        self.items = ["Apple", "Banana", "Orange", "Pineapple", "Grapes", "Watermelon", "Cherry", "Strawberry"]

        # Добавление элементов в QListWidget
        self.list_widget.addItems(self.items)

        # Добавление виджетов в макет
        self.layout.addWidget(self.search_bar)
        self.layout.addWidget(self.list_widget)
        self.setLayout(self.layout)

        # Подключение сигнала изменения текста
        self.search_bar.textChanged.connect(self.filter_list)

    def filter_list(self):
        search_text = self.search_bar.text().lower()

        # Очистка списка
        self.list_widget.clear()

        # Поиск и добавление совпадающих элементов
        for item in self.items:
            if search_text in item.lower():
                self.list_widget.addItem(item)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SearchApp()
    ex.show()
    sys.exit(app.exec_())
