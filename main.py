import os
import sys

import requests
from PyQt5.QtCore import Qt
from pynput import keyboard
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
        print(1)

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
        print(222)
        if event.key() == 16777238:
            self.spn += self.spn / 10
            self.getImage()
            self.pixmap = QPixmap(self.map_file)
            self.image.setPixmap(self.pixmap)
        if event.key() == 16777239:
            self.spn -= self.spn / 10
            self.getImage()
            self.pixmap = QPixmap(self.map_file)
            self.image.setPixmap(self.pixmap)
            print(self.spn)
        if event.key() == Qt.Key_Left:
            self.X -= 0.01
            print(self.X)
        if event.key() == Qt.Key_Right:
            self.X += 0.01
            print(self.X, 'R')
        if event.key() == Qt.Key_Up:
            self.Y -= 0.01
            print(self.Y)
        if event.key() == Qt.Key_Down:
            self.Y += 0.01
            print(self.Y, 'D')

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
        toponym_to_find = self.line1.text()
        geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

        geocoder_params = {
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
            "geocode": toponym_to_find,
            "format": "json"}

        response = requests.get(geocoder_api_server, params=geocoder_params)

        if not response:
            # обработка ошибочной ситуации
            pass

        # Преобразуем ответ в json-объект
        json_response = response.json()
        # Получаем первый топоним из ответа геокодера.
        toponym = json_response["response"]["GeoObjectCollection"][
            "featureMember"][0]["GeoObject"]
        # Координаты центра топонима:
        toponym_coodrinates = toponym["Point"]["pos"]
        # Долгота и широта:
        self.X, self.Y = toponym_coodrinates.split(" ")
        self.getImage()
        self.pixmap = QPixmap(self.map_file)
        self.image.setPixmap(self.pixmap)
        #  delta = "0.005"

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


