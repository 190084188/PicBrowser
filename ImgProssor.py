import sys
import os
import cv2 as cv
import numpy as np

img_path = '1.jpg'


class ImgPross:

    def __init__(self, img, img_path=None):
        if isinstance(img, str):
            self.img_o = cv.imread(img)
            self.img_path = img
        elif isinstance(img, np.ndarray):
            self.img_o = img
            self.img_path = img_path
        else:
            raise TypeError("输入类型必须是字符串文件路径或ndarray")
        self.img = self.img_o

    def show(self, window_name=None):
        if window_name is None:
            filename = os.path.basename(self.img_path)
            window_name = os.path.splitext(filename)[0]
        cv.imshow(window_name, self.img)
        cv.waitKey()
        cv.destroyAllWindows()

    def origin(self):
        self.img = self.img_o

    def gray(self):
        img_g = cv.cvtColor(self.img, cv.COLOR_BGR2GRAY)
        self.img = img_g
        return img_g

    def rotate(self, angle):
        (h, w) = self.img.shape[:2]
        center = (w // 2, h // 2)
        M = cv.getRotationMatrix2D(center, angle, 1.0)
        img_r = cv.warpAffine(self.img, M, (w, h))
        self.img = img_r
        return img_r

    def invert(self):
        img_i = 255 - self.img
        self.img = img_i
        return img_i


img = cv.imread(img_path)
img = ImgPross(img, img_path)
img.invert()
img.show()
