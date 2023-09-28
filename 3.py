import cv2
import numpy as np
# 读取图片
img = cv2.imread('chair.bmp')
# 灰度图
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# 边缘检测
edges = cv2.Canny(gray, 50, 150, apertureSize=3)
# BGR -> RGB
img_RGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
img_Show = img_RGB.copy()
# 霍夫直线变化
lines = cv2.HoughLines(edges, 1, np.pi / 180, 160)
# 绘制检测到的直线
for line in lines:
    # (r, θ)
    rho, theta = line[0]
    # 通过(r, θ)获取到(x0,y0)
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a * rho
    y0 = b * rho
    # 获得(x1,y1),(x2,y2)
    x1 = int(x0 + 1000 * (-b))
    y1 = int(y0 + 1000 * a)
    x2 = int(x0 - 1000 * (-b))
    y2 = int(y0 - 1000 * a)
    # 绘制直线
    cv2.line(img_RGB, (x1, y1), (x2, y2), (255, 0, 0), 2)
# 显示图片
cv2.imshow('result', img_RGB)
cv2.waitKey()
cv2.destroyAllWindows()
