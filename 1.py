import cv2
import numpy as np

def calc_histogram(image):
    hist = cv2.calcHist([image], [0], None, [256], [0, 256])
    return hist

def histogram_equalization(image):
    hist = calc_histogram(image)
    cdf = hist.cumsum()
    cdf_m = np.ma.masked_equal(cdf,0)
    cdf_m = (cdf_m - cdf_m.min())*255/(cdf_m.max()-cdf_m.min())
    cdf = np.ma.filled(cdf_m,0).astype('uint8')
    img2 = cdf[image]
    return img2

img = cv2.imread('1.jpg', 0)
hist = cv2.calcHist([img], [0], None, [256], [0, 256])
# 计算累积分布函数
cdf = hist.cumsum()
# 归一化
cdf_m = np.ma.masked_equal(cdf, 0)
cdf_m = (cdf_m - cdf_m.min()) * 255 / (cdf_m.max()-cdf_m.min())
cdf = np.ma.filled(cdf_m, 0).astype('uint8')
# 直方图均衡化
img2 = cdf[img]
hist = calc_histogram(img)
img_eq = histogram_equalization(img)

cv2.imshow('image', img)
cv2.imshow('image_eq', img_eq)
cv2.imshow('img_eq_cv', img2)
cv2.waitKey(0)
cv2.destroyAllWindows()