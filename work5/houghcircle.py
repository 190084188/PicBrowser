import numpy as np
import cv2 as cv
# 读取图像
img = cv.imread('coins.bmp')
# 中值滤波去噪
img_blur = cv.medianBlur(img, 5)
# 转化为灰度图
img_gray = cv.cvtColor(img_blur, cv.COLOR_BGR2GRAY)
# 检测圆
circles = cv.HoughCircles(img_gray, cv.HOUGH_GRADIENT, 1, 50,
                          param1=200, param2=50, minRadius=50, maxRadius=0)
circles = np.uint16(np.around(circles))
# 绘制检测到的圆
for i in circles[0, :]:
    # 绘制圆轮廓
    cv.circle(img, (i[0], i[1]), i[2], (0, 255, 0), 10)
    # 绘制圆心
    cv.circle(img, (i[0], i[1]), 2, (0, 0, 255), 3)
# OpenCV窗口显示
cv.namedWindow('Detected Circles',cv.WINDOW_NORMAL)
cv.imshow('Detected Circles', img)
cv.waitKey(0)
cv.destroyAllWindows()