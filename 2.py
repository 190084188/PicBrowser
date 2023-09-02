import sys
import cv2
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QFileDialog, QVBoxLayout
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt


class ImageViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Image Viewer')
        self.button = QPushButton('Open Image', self)
        self.button.clicked.connect(self.open_image)
        self.image_label = QLabel(self)
        self.image_label.resize(500, 500)
        self.image_label.setScaledContents(True)
        self.image = None

        layout = QVBoxLayout()
        layout.addWidget(self.button)
        layout.addWidget(self.image_label)
        self.setLayout(layout)

    def open_image(self):
        fname, _ = QFileDialog.getOpenFileName(self, 'Open Image', '.', 'Image Files (*.jpg *.png)')
        if fname:
            self.image = cv2.imread(fname)
            qimg = QImage(self.image.data, self.image.shape[1], self.image.shape[0], QImage.Format_RGB888).rgbSwapped()
            pixmap = QPixmap.fromImage(qimg)
            self.image_label.setPixmap(pixmap)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    viewer = ImageViewer()
    viewer.show()
    sys.exit(app.exec_())