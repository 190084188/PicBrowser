import sys
import cv2
import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap, QPainter
from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow
from PyQt5 import QtGui
import demo  # 界面代码文件


class ImageViewer(QMainWindow, demo.Ui_MainWindow):

    def __init__(self):
        super(ImageViewer, self).__init__()
        self.img_r = None
        self.img_cv = None
        self.pixmap = None
        self.img = None

        self.setupUi(self)
        self.scale = 1  # 图片默认缩放比例
        self.label.wheelEvent = self.wheelEvent  # 给label添加滚轮事件
        self.label.mousePressEvent = self.mousePressEvent
        #self.label.setScaledContents(True)

        # 连接信号和槽
        self.action1.triggered.connect(self.open_image)
        self.pushButton .clicked.connect(self.rotate)


    def open_image(self):
        img_path, _ = QFileDialog.getOpenFileName(self, 'Open Image', '.', 'Image Files (*.jpg *.png *.jpeg)')

        if img_path:
            # 读取图片
            img = cv2.imread(img_path)
            self.img_cv = img
            self.img_r = img
            print(img.shape[1], img.shape[0])
            # 将 OpenCV 图片转换为 QImage
            img = QImage(img, img.shape[1], img.shape[0], QImage.Format_RGB888).rgbSwapped()

            img = img.scaled(self.label.size(), Qt.KeepAspectRatio)
            self.img = img
            # 显示图片
            self.label.setPixmap(QPixmap.fromImage(img))

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            self.scale *= 1.1
        else:
            self.scale *= 0.9


        self.resize_image()  # 放大缩小图片

    def resize_image(self):
        if self.img is None:
            return

        w = int(self.img.width() * self.scale)
        h = int(self.img.height() * self.scale)
        img = self.img.scaled(w, h, Qt.KeepAspectRatio)
        self.label.setPixmap(QPixmap.fromImage(img))

    def rotate(self):
        if self.img is None:
            return
        if self.r_angle.toPlainText() == ' ':
            angle = 90
        else:
            angle = self.r_angle.toPlainText()
        (h, w) = self.img_cv.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, int(angle), 1.0)
        img = cv2.warpAffine(self.img_r, M, (w, h))
        self.img_r = img
        img = QImage(img, img.shape[1], img.shape[0], QImage.Format_RGB888).rgbSwapped()
        self.img = img
        self.label.setPixmap(QPixmap.fromImage(img))



if __name__ == '__main__':
    app = QApplication(sys.argv)
    viewer = ImageViewer()
    viewer.show()
    sys.exit(app.exec_())