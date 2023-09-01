import sys
from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow, QGraphicsView, QGraphicsScene, QAction
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
import cv2
import os


class ImageViewer(QMainWindow):

    def __init__(self):
        super().__init__()

        self.image = QImage()
        self.pixmap = QPixmap()

        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)

        self.openAction = QAction("Open File", self)
        self.openAction.triggered.connect(self.openFile)

        self.openFolderAction = QAction("Open Folder", self)
        self.openFolderAction.triggered.connect(self.openFolder)

        self.grayAction = QAction("Grayscale", self)
        self.grayAction.triggered.connect(self.grayscale)

        self.rotateAction = QAction("Rotate", self)
        self.rotateAction.triggered.connect(self.rotate)

        self.invertAction = QAction("Invert", self)
        self.invertAction.triggered.connect(self.invert)

        self.zoomInAction = QAction("Zoom In", self)
        self.zoomInAction.triggered.connect(self.zoomIn)

        self.zoomOutAction = QAction("Zoom Out", self)
        self.zoomOutAction.triggered.connect(self.zoomOut)

        self.toolbar = self.addToolBar("File")
        self.toolbar.addAction(self.openAction)
        self.toolbar.addAction(self.openFolderAction)

        self.toolbar2 = self.addToolBar("Edit")
        self.toolbar2.addAction(self.grayAction)
        self.toolbar2.addAction(self.rotateAction)
        self.toolbar2.addAction(self.invertAction)
        self.toolbar2.addAction(self.zoomInAction)
        self.toolbar2.addAction(self.zoomOutAction)

        self.setCentralWidget(self.view)

    def openFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Image")
        if fileName:
            self.openImage(fileName)

    def openFolder(self):
        folderPath = QFileDialog.getExistingDirectory(self, "Open Folder")
        if folderPath:
            self.openImagesInFolder(folderPath)

    def openImage(self, fileName):
        self.image.load(fileName)
        self.pixmap = QPixmap.fromImage(self.image)
        self.setImage()

    def openImagesInFolder(self, folderPath):
        files = [os.path.join(folderPath, f) for f in os.listdir(folderPath) if f.endswith('.jpg')]
        for f in files:
            self.openImage(f)

    def setImage(self):
        self.scene.clear()
        self.scene.addPixmap(self.pixmap)
        self.view.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)

    def grayscale(self):
        img = cv2.cvtColor(self.image.toImage().bits(), cv2.COLOR_BGR2GRAY)
        h, w = self.image.height(), self.image.width()
        gray = QImage(img.data, w, h, w, QImage.Format_Grayscale8)
        self.pixmap = QPixmap.fromImage(gray)
        self.setImage()

    def rotate(self):
        self.image = self.image.transformed(QTransform().rotate(90))
        self.pixmap = QPixmap.fromImage(self.image)
        self.setImage()

    def invert(self):
        inverted = 255 - self.image.toImage().bits()
        h, w = self.image.height(), self.image.width()
        img = QImage(inverted, w, h, w, self.image.format())
        self.pixmap = QPixmap.fromImage(img)
        self.setImage()

    def zoomIn(self):
        self.view.scale(1.2, 1.2)

    def zoomOut(self):
        self.view.scale(1 / 1.2, 1 / 1.2)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ImageViewer()
    window.show()
    app.exec_()