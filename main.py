import os
import sys

import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtWidgets import QPushButton, QLineEdit

SCREEN_SIZE = [600, 450]


class Example(QWidget):
    def __init__(self):
        super().__init__()
        X,Y = 37.530887,55.703118
        spn = 0.002
        tmap = 'map'
        self.getImage(X,Y,spn,tmap)
        self.initUI()

    def getImage(self,X,Y,spn,tmap):
        map_request = f"http://static-maps.yandex.ru/1.x/?ll={X},{Y}&spn={spn},0.002&l={tmap}"
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
    def closeEvent(self, event):
        """При закрытии формы подчищаем за собой"""
        os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())