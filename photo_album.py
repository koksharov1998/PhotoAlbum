import os
import shutil
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QFileDialog, QPushButton, QLineEdit, QComboBox, QListWidget

from thumbnails_window import ThumbnailsWindow


class PhotoAlbum(QWidget):
    def __init__(self):
        super().__init__()
        self.left = 100
        self.top = 100
        self.width = 1500
        self.height = 900
        self.title = 'Photo Album'
        self.icon = 'icon.png'
        self.directory = os.getcwd() + '/images/'
        self.album = 'New Album'
        i = 0
        while self.album in os.listdir(self.directory):
            i += 1
            self.album = 'New Album (' + str(i) + ')'
        self.counter = 0
        self.files = self.get_all_photo(self.directory)
        self.initUI()

    def initUI(self):
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon(self.icon))
        self.label = QLabel(self)
        self.label.setGeometry(50, 50, self.width - 50, self.height - 50)

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

        self.line_name_of_photo = QLineEdit(self)
        self.line_name_of_photo.move(550, 30)

        button_add_to_current_album = QPushButton('Add to album', self)
        button_add_to_current_album.move(550, 60)
        button_add_to_current_album.clicked.connect(self.add_to_current_album)

        line_name_of_album = QLineEdit(self)
        line_name_of_album.move(700, 30)
        line_name_of_album.setText(self.album)
        line_name_of_album.textChanged[str].connect(self.get_new_name_of_album)

        button_create_new_album = QPushButton('Create a new album', self)
        button_create_new_album.move(700, 60)
        button_create_new_album.clicked.connect(self.create_new_album)

        button_short_look = QPushButton('Look Album', self)
        button_short_look.move(860, 50)
        button_short_look.clicked.connect(self.create_thumbnails)
        self.thumbnails_window = None

        self.list_of_files = QListWidget(self)
        self.list_of_files.addItems(self.files)
        self.list_of_files.resize(500, 200)
        self.list_of_files.move(900, 600)
        self.list_of_files.itemClicked.connect(self.load_image_from_list)

        self.load_image()
        self.show()

    def create_thumbnails(self):
        if not self.album in os.listdir('./images/'):
            return
        self.thumbnails_window = ThumbnailsWindow(self.album, self.get_all_photo('./images/' + self.album + '/', []))
        self.thumbnails_window.show()


    def load_image_from_list(self):
        self.counter = self.list_of_files.currentRow()
        self.load_image()

    def get_new_name_of_album(self, text):
        self.album = text

    def create_new_album(self):
        if not self.album in os.listdir('./images/'):
            os.mkdir('./images/' + self.album)
        else:
            return

    def add_to_current_album(self):
        if not self.album in os.listdir('./images/'):
            return
        if len(self.files) == 0:
            return
        temp_file_name = self.files[self.counter].replace('\\', '/')
        shutil.copy(self.files[self.counter], './images/' + self.album)
        os.rename('./images/' + self.album + '/' + temp_file_name.split('/')[-1],
                  './images/' + self.album + '/' + self.line_name_of_photo.text())
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
            self.load_image()

    def get_all_photo(self, directory, lisss=[]):
        for file in os.listdir(directory):
            file = os.path.join(directory, file)
            if os.path.isdir(file):
                l2 = self.get_all_photo(file, lisss)
            else:
                file_name, ext = os.path.splitext(file)
                if not (ext != '.jpg' and ext != '.png' and ext != '.gif') or os.path.isdir(file):
                    lisss.append(file)
        return lisss

    def change_directory(self):
        directory = QFileDialog.getExistingDirectory(self)
        if directory == '':
            return
        self.directory = directory + '/'
        self.files = []
        self.counter = 0

        self.files = self.get_all_photo(self.directory, self.files)
        if len(self.files) == 0:
            self.list_of_files.hide()
            self.label.hide()
            self.line_name_of_photo.setText('')
        else:
            self.list_of_files.clear()
            self.list_of_files.addItems(self.files)
            self.list_of_files.show()
            self.load_image()
            self.label.show()

    def go_next(self):
        if len(self.files) == 0:
            return
        self.counter = (self.counter + 1) % len(self.files)
        self.load_image()

    def go_previous(self):
        if len(self.files) == 0:
            return
        self.counter = (self.counter - 1) % len(self.files)
        self.load_image()

    def keyPressEvent(self, e):
        key = e.key()
        if key == Qt.Key_Escape:
            self.close()

    def load_image(self):
        if len(self.files) == 0:
            return
        pixmap = QPixmap(self.files[self.counter])
        pixmap = pixmap.scaled(pixmap.width() // 2, pixmap.height() // 2)
        self.label.setPixmap(pixmap)
        temp_file_name = self.files[self.counter].replace('\\', '/')
        self.line_name_of_photo.setText(temp_file_name.split('/')[-1])


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

# Пример использования:
# import dlib
# from sys import argv
# from skimage.io import imread
# import numpy as np

# detector = dlib.get_frontal_face_detector()
# sp = dlib.shape_predictor('face_landmarks.dat')
# facerec = dlib.face_recognition_model_v1('face_recognition.dat')

# def get_face_desc(file):
# img = imread(file)
# face = sp(img, detector(img, 1)[0])
# return facerec.compute_face_descriptor(img, face)

# v1 = np.array(get_face_desc(argv[1]))
# v2 = np.array(get_face_desc(argv[2]))
# d = np.sqrt(sum((v1 - v2) ** 2))

# print("Same" if d < 0.6 else "Not same")
# print(d)
