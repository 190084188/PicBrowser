# 开发第一个基于PyQt5的桌面应用

import sys
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage

import Mainwindow
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QFileDialog
import os
import cv2 as cv
import numpy as np


class ImageViewer(QMainWindow, Mainwindow.Ui_MainWindow):
    def __init__(self):
        super(ImageViewer, self).__init__()
        self.img_qt = None
        self.pixmap = None
        self.img = None
        self.img_origin = None
        self.setupUi(self)
        self.scale = 1  # 图片默认缩放比例
        self.label.wheelEvent = self.wheelEvent  # 给label添加滚轮事件
        self.label.mousePressEvent = self.mousePressEvent
        # 连接信号和槽
        self.Open_Pic.triggered.connect(self.open_image)
        self.graypb.clicked.connect(self.gray)
        self.originpb.clicked.connect(self.origin)
        self.invertpb.clicked.connect(self.invert)
        self.rotatepb.clicked.connect(self.rotate)

    def open_image(self):
        img_path, _ = QFileDialog.getOpenFileName(self, 'Open Image', '.', 'Image Files (*.jpg *.png *.jpeg)')
        if img_path:
            # 读取图片
            img = cv.imread(img_path)
            self.img_origin = img
            # 将 OpenCV 图片转换为 QImage
            img = QImage(img, img.shape[1], img.shape[0], QImage.Format_RGB888).rgbSwapped()
            self.img_qt = img
            self.img = img
            self.pixmap = QPixmap.fromImage(img)
            # 显示图片
            self.piclabel.setPixmap(QPixmap.fromImage(img))

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            self.scale += 0.1
        else:
            self.scale -= 0.1

        if self.scale < 0.1:
            self.scale = 0.1

        self.resize_image()  # 放大缩小图片

    def resize_image(self):
        if self.img is None:
            return

        w = int(self.img.width() * self.scale)
        h = int(self.img.height() * self.scale)
        img = self.img.scaled(w, h, Qt.KeepAspectRatio)
        self.piclabel.setPixmap(QPixmap.fromImage(img))

    def gray(self):
        if self.img is None:
            return

        img = cv.cvtColor(self.img_origin, cv.COLOR_BGR2GRAY)
        img = QImage(img, img.shape[1], img.shape[0], QImage.Format_Grayscale8)
        self.img = img
        self.piclabel.setPixmap(QPixmap.fromImage(img))

    def origin(self):
        if self.img is None:
            return
        self.img = self.img_qt
        self.piclabel.setPixmap(QPixmap.fromImage(self.img))

    def invert(self):
        if self.img is None:
            return
        img = 255 - self.img_origin
        img = QImage(img, img.shape[1], img.shape[0], QImage.Format_RGB888).rgbSwapped()
        self.img = img
        self.piclabel.setPixmap(QPixmap.fromImage(img))

    def rotate(self, angle=90):
        if self.img is None:
            return
        (h, w) = self.img_origin.shape[:2]
        center = (w // 2, h // 2)
        M = cv.getRotationMatrix2D(center, angle, 1.0)
        img = cv.warpAffine(self.img, M, (w, h))
        img = QImage(img, img.shape[1], img.shape[0], QImage.Format_RGB888).rgbSwapped()
        self.img = img
        self.piclabel.setPixmap(QPixmap.fromImage(img))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = ImageViewer()
    main.show()
    sys.exit(app.exec_())
