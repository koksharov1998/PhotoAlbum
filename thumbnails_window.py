from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QLabel


class ThumbnailsWindow(QWidget):
    def __init__(self, album_name, files):
        super().__init__()
        self.left = 200
        self.top = 200
        self.width = 500
        self.height = 500
        print(album_name)
        self.title = album_name
        self.files = files
        self.counter = 0
        self.labels = []
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        i = 0
        for file in self.files:
            i += 1
            label = QLabel(self)
            #label.setGeometry((50 * i) % self.width, (50 * (i // 5) % self.height), self.width - 50, self.height - 50)
            label.setGeometry(100 * i, 50 , self.width - 50, self.height - 50)
            pixmap = QPixmap(file)
            pixmap = pixmap.scaled(100, 100)
            label.setPixmap(pixmap)
            label.show()
            self.labels.append(QLabel(self))




    def keyPressEvent(self, e):
        key = e.key()
        if key == Qt.Key_Escape:
            self.close()
