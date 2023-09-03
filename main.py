# 开发第一个基于PyQt5的桌面应用
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage, QIcon
import Mainwindow
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QFileDialog, QMessageBox
import os
import cv2 as cv


# 定义图片浏览器类，继承于之前的UI设计文件
class ImageViewer(QMainWindow, Mainwindow.Ui_MainWindow):
    def __init__(self):
        super(ImageViewer, self).__init__()
        self.img_cv = None  # opencv格式的图片
        self.cur_img_idx = None  # 用于文件夹显示图片的图片索引
        self.img_list = None  # 文件夹中图片组成的列表
        self.img_qt = None  # QImage格式的图片
        self.img = None  # 读取到的图片，下面使用的时候用这个，为QImage类型
        self.img_origin = None  # 原始图像，用于恢复原图
        self.setupUi(self)
        self.scale = 1  # 图片默认缩放比例
        self.piclabel.wheelEvent = self.wheelEvent  # 给piclabel添加滚轮事件
        self.piclabel.setAlignment(Qt.AlignCenter)  # Label中居中显示图片
        # 连接信号和槽
        self.Open_Pic.triggered.connect(self.open_image)  # 次级菜单中点击图片文件打开并显示图片
        self.Open_Filedir.triggered.connect(self.open_img_dir)  # 次级菜单中点击图片文件夹打开并显示图片
        self.graypb.clicked.connect(self.gray)  # 灰度化按钮
        self.originpb.clicked.connect(self.origin)  # 恢复原图按钮
        self.invertpb.clicked.connect(self.invert)  # 反色按钮
        self.rotatepb.clicked.connect(self.rotate)  # 旋转按钮
        self.after.clicked.connect(self.prev_img)  # 上一张按钮
        self.before.clicked.connect(self.next_img)  # 下一张按钮

# 打开--图片文件的实现函数
    def open_image(self):
        self.img_list = []  # 清空打开图片文件夹后生成得图片列表
        img_path, _ = QFileDialog.getOpenFileName(self, 'Open Image', '.', 'Image Files (*.jpg *.png *.jpeg)')
        if img_path:
            # 读取图片
            img = cv.imread(img_path)
            # 不改变图片比例的情况下自适应Label大小
            scale1 = self.piclabel.width() / img.shape[1]  # 计算比例
            scale2 = self.piclabel.height() / img.shape[0]
            self.scale = min(scale1, scale2)
            w = int(img.shape[1] * self.scale)
            h = int(img.shape[0] * self.scale)
            self.img_origin = cv.resize(img, (w, h))
            self.img_cv = self.img_origin
            # 将 OpenCV 图片转换为 QImage，由于OpenCV是BGR格式，所以要转换一下
            img = QImage(img, img.shape[1], img.shape[0], QImage.Format_RGB888).rgbSwapped()
            self.img = img
            w = int(self.img.width() * self.scale)
            h = int(self.img.height() * self.scale)
            img = self.img.scaled(w, h, Qt.KeepAspectRatio)
            self.img_qt = img
            # 显示图片
            self.piclabel.setPixmap(QPixmap.fromImage(img))

    def open_img_dir(self):
        img_dir = QFileDialog.getExistingDirectory(self, '选择图片文件夹')
        # 文件夹选中后执行
        if img_dir:
            img_files = [img_dir + '/' + img for img in os.listdir(img_dir) if
                         img.lower().endswith('.png') or img.lower().endswith('.jpg') or img.lower().endswith('.jpeg')]
            if len(img_files) > 0:
                self.img_list = img_files
                self.cur_img_idx = 0
                self.show_img()

    def show_img(self):
        img = cv.imread(self.img_list[self.cur_img_idx])  # 读取列表中的图片
        scale1 = self.piclabel.width() / img.shape[1]
        scale2 = self.piclabel.height() / img.shape[0]
        self.scale = min(scale1, scale2)
        w = int(img.shape[1] * self.scale)
        h = int(img.shape[0] * self.scale)
        self.img_origin = cv.resize(img, (w, h))
        self.img_cv = self.img_origin
        # 将 OpenCV 图片转换为 QImage
        img = QImage(img, img.shape[1], img.shape[0], QImage.Format_RGB888).rgbSwapped()
        self.img = img
        w = int(self.img.width() * self.scale)
        h = int(self.img.height() * self.scale)
        img = self.img.scaled(w, h, Qt.KeepAspectRatio)
        self.img_qt = img
        # 显示图片
        self.piclabel.setPixmap(QPixmap.fromImage(img))

    def prev_img(self):
        if len(self.img_list) == 0:
            QMessageBox.warning(self, "警告", "打开文件夹后使用", QMessageBox.Cancel)
            return
        self.cur_img_idx -= 1
        if self.cur_img_idx < 0:
            self.cur_img_idx = len(self.img_list) - 1
        self.show_img()

    def next_img(self):
        if len(self.img_list) == 0:
            QMessageBox.warning(self, "警告", "打开文件夹后使用", QMessageBox.Cancel)
            return
        self.cur_img_idx += 1
        if self.cur_img_idx >= len(self.img_list):
            self.cur_img_idx = 0
        self.show_img()

# 滚轮放缩图片
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
        self.piclabel.setPixmap(QPixmap.fromImage(img))

    def gray(self):
        if self.img is None:
            return
        img = cv.cvtColor(self.img_cv, cv.COLOR_BGR2GRAY)
        self.img_cv = img
        img = QImage(img, img.shape[1], img.shape[0], img.strides[0], QImage.Format_Grayscale8)
        self.img = img
        self.piclabel.setPixmap(QPixmap.fromImage(img))

    def origin(self):
        if self.img is None:
            return
        self.img_cv = self.img_origin
        self.img = self.img_qt
        self.piclabel.setPixmap(QPixmap.fromImage(self.img))

    def invert(self):
        if self.img is None:
            return
        img = 255 - self.img_cv
        self.img_cv = img
        img = QImage(img, img.shape[1], img.shape[0], img.strides[0], QImage.Format_RGB888).rgbSwapped()
        self.img = img
        self.piclabel.setPixmap(QPixmap.fromImage(img))

# 旋转实现函数
    def rotate(self):
        if self.img is None:
            return
        # 不输入角度的情况下默认角度为90
        if self.angleinput.toPlainText() == ' ':
            angle = 90
        else:
            # 读取文本框输入作为角度
            angle = self.angleinput.toPlainText()
        (h, w) = self.img_origin.shape[:2]
        center = (w / 2, h / 2)  # 设置旋转中心
        M = cv.getRotationMatrix2D(center, int(angle), 1.0)
        img = cv.warpAffine(self.img_cv, M, (w, h), borderValue=(243, 255, 234, 0))  # 设置边缘颜色与Label一致
        self.img_cv = img
        # 通过图片通道数判断是否是灰度图，若是则OpenCV转QImage时参数要变化
        channels = img.shape[2] if len(img.shape) == 3 else 1
        if channels == 1:
            img = QImage(img, img.shape[1], img.shape[0], img.strides[0], QImage.Format_Indexed8)
        else:
            img = QImage(img, img.shape[1], img.shape[0], img.strides[0], QImage.Format_RGB888).rgbSwapped()
        self.img = img
        self.piclabel.setPixmap(QPixmap.fromImage(img))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = ImageViewer()
    main.setWindowIcon(QIcon('C:\\Users\\Lismoon\\Desktop\\logo1.png'))
    main.setWindowTitle('图像浏览器1.0by李思民')
    main.show()
    sys.exit(app.exec_())
