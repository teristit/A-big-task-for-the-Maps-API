import os
import sys

import requests
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtWidgets import QPushButton, QLineEdit

SCREEN_SIZE = [600, 450]


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.X, self.Y = 37.530887, 55.703118
        self.spn = 0.002
        self.tmap = 'map'
        self.getImage()
        self.initUI()

    def getImage(self):
        map_request = f"http://static-maps.yandex.ru/1.x/?ll={self.X},{self.Y}&spn={self.spn},{self.spn}&l={self.tmap}"
        response = requests.get(map_request)

        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        # Запишем полученное изображение в файл.
        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PgUp:
            self.spn += self.spn // 10
            print(self.spn)
        elif event.key() == Qt.Key_PgDown:
            self.spn -= self.spn // 10
            print(self.spn)

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')

        ## Изображение
        self.pixmap = QPixmap(self.map_file)
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(600, 550)
        self.image.setPixmap(self.pixmap)
        self.line1 = QLineEdit(self)
        self.line1.setGeometry(10, 10, 150, 30)
        self.baton_search = QPushButton(self)
        self.baton_search.setGeometry(170, 10, 80, 30)
        self.baton_search.setText('Потерятся')
        self.baton_map = QPushButton(self)
        self.baton_map.setGeometry(250, 10, 40, 30)
        self.baton_map.setText('Карта')
        self.baton_sat = QPushButton(self)
        self.baton_sat.setGeometry(290, 10, 60, 30)
        self.baton_sat.setText('Спутник')
        self.baton_mixed = QPushButton(self)
        self.baton_mixed.setGeometry(350, 10, 70, 30)
        self.baton_mixed.setText('Смешаные')
        self.baton_search.clicked.connect(self.click_search)
        self.baton_map.clicked.connect(self.click_map)
        self.baton_sat.clicked.connect(self.click_sat)
        self.baton_mixed.clicked.connect(self.click_mixed)

    def click_search(self):
        pass

    def click_map(self):
        self.tmap = 'map'
        self.getImage()
        self.pixmap = QPixmap(self.map_file)
        self.image.setPixmap(self.pixmap)

    def click_sat(self):
        self.tmap = 'sat'
        self.getImage()
        self.pixmap = QPixmap(self.map_file)
        self.image.setPixmap(self.pixmap)


    def click_mixed(self):
        self.tmap = 'sat%2Cskl'
        self.getImage()
        self.pixmap = QPixmap(self.map_file)
        self.image.setPixmap(self.pixmap)

    def closeEvent(self, event):
        """При закрытии формы подчищаем за собой"""
        os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
