import os
import sys
import shutil

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QFileDialog, QPushButton


class PhotoAlbum(QWidget):
    def __init__(self):
        super().__init__()
        self.left = 100
        self.top = 100
        self.width = 1200
        self.height = 800
        self.title = 'Photo Album'
        self.icon = 'icon.png'
        self.directory = './images/'
        self.album = 'New Album'
        i = 0
        while self.album in os.listdir(self.directory):
            i += 1
            self.album = 'New Album (' + str(i) + ')'
        self.album = './images/' + self.album
        os.mkdir(self.album)
        self.counter = 0
        self.files = []
        files = os.listdir(self.directory)
        for file in files:
            file_name, ext = os.path.splitext(file)
            if not (ext != '.jpg' and ext != '.png' and ext != '.gif') or os.path.isdir(file):
                self.files.append(file)
        self.initUI()

    def initUI(self):
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon(self.icon))
        self.label = QLabel(self)
        self.label.setGeometry(50, 50, self.width - 50, self.height - 50)
        if len(self.files) != 0:
            pixmap = QPixmap(self.directory + self.files[self.counter])
            pixmap = pixmap.scaled(pixmap.width() // 2, pixmap.height() // 2)
            self.label.setPixmap(pixmap)

        button_next = QPushButton('Next', self)
        button_next.move(120, 20)
        button_next.clicked.connect(self.go_next)

        button_previous = QPushButton('Previous', self)
        button_previous.move(20, 20)
        button_previous.clicked.connect(self.go_previous)

        button_change_directory = QPushButton('Change Directory', self)
        button_change_directory.move(250, 20)
        button_change_directory.clicked.connect(self.change_directory)

        button_delete = QPushButton('Delete', self)
        button_delete.move(400, 20)
        button_delete.clicked.connect(self.delete)

        button_add_to_current_album = QPushButton('Add to album', self)
        button_add_to_current_album.move(550, 20)
        button_add_to_current_album.clicked.connect(self.add_to_current_album)

        self.show()

    def add_to_current_album(self):
        if len(self.files) == 0:
            return
        print(self.directory + self.files[self.counter])
        print(self.album)
        shutil.copy(self.directory + self.files[self.counter], self.album)
        return

    def delete(self):
        if len(self.files) == 0:
            return
        else:
            self.files.remove(self.files[self.counter])
        if len(self.files) == 0:
            self.label.hide()
            return
        else:
            self.counter = self.counter % len(self.files)
            self.load_image(self.directory + self.files[self.counter])

    def change_directory(self):
        directory = QFileDialog.getExistingDirectory(self)
        if directory == '':
            return
        self.directory = directory + '/'
        self.files = []
        self.counter = 0
        files = os.listdir(self.directory)
        for file in files:
            file_name, ext = os.path.splitext(file)
            if not (ext != '.jpg' and ext != '.png' and ext != '.gif') or os.path.isdir(file):
                self.files.append(file)
        self.load_image(self.directory + self.files[self.counter])
        self.label.show()

    def go_next(self):
        if len(self.files) == 0:
            return
        self.counter = (self.counter + 1) % len(self.files)
        self.load_image(self.directory + self.files[self.counter])

    def go_previous(self):
        if len(self.files) == 0:
            return
        self.counter = (self.counter - 1) % len(self.files)
        self.load_image(self.directory + self.files[self.counter])

    def keyPressEvent(self, e):
        key = e.key()
        if key == Qt.Key_Escape:
            self.close()
        elif key == Qt.Key_D:
            self.go_next()
        elif key == Qt.Key_A:
            self.go_previous()
        elif key == Qt.Key_C:
            self.change_directory()
        elif key == Qt.Key_E:
            self.delete()

    def load_image(self, file_name):
        pixmap = QPixmap(file_name)
        pixmap = pixmap.scaled(pixmap.width() // 2, pixmap.height() // 2)
        self.label.setPixmap(pixmap)


def main():
    app = QApplication(sys.argv)
    photo_album = PhotoAlbum()
    sys.exit(app.exec_())


if __name__ == '__main__':
    # Back up the reference to the exceptionhook
    sys._excepthook = sys.excepthook


    def my_exception_hook(exctype, value, traceback):
        # Print the error and traceback
        print(exctype, value, traceback)
        # Call the normal Exception hook after
        sys._excepthook(exctype, value, traceback)
        sys.exit(1)

        # Set the exception hook to our wrapping function


    sys.excepthook = my_exception_hook
    try:
        main()
    except:
        print("Exiting")
