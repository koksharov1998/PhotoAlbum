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
        self.title = album_name
        self.files = files
        self.counter = 0
        self.labels = []
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        i = -1
        for file in self.files:
            i += 1
            self.labels.append(QLabel(self))
            label = self.labels[i]
            label.setGeometry(10 + 110 * (i % (self.width // 110)), 10 + 110 * (i // (self.height // 110)), 100, 100)
            pixmap = QPixmap(file)
            pixmap = pixmap.scaled(100, 100)
            label.setPixmap(pixmap)
            label.clicked.connect(self.delete)
            label.show()

    def keyPressEvent(self, e):
        key = e.key()
        if key == Qt.Key_Escape:
            self.close()
