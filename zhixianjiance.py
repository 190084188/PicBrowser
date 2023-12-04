import cv2
import numpy as np
# 读取输入图片
img = cv2.imread('chair.bmp')
# 将彩色图片灰度化
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(img, (3,3), 0)#高斯模糊，去噪
# 使用Canny边缘检测
edges = cv2.Canny(gray, 50, 150, apertureSize=3)
# lines =cv2.HoughLinesP(image, rho, theta, threshold, minLineLength,maxLineGap)
# 其中：
#  image 是输入图像，即源图像，必须为 8 位的单通道二值图像。
#  rho 为以像素为单位的距离 r 的精度。一般情况下，使用的精度是 1。
#  theta 是角度 的精度。一般情况下，使用的精度是 np.pi/180，表示要搜索可能的角度。
#  threshold 是阈值。该值越小，判定出的直线越多；值越大，判定出的直线就越少。
#  minLineLength 用来控制“接受直线的最小长度”的值，默认值为 0。
#  maxLineGap 用来控制接受共线线段之间的最小间隔，即在一条线中两点的最大间隔。
#  如果两点间的间隔超过了参数 maxLineGap 的值， 就认为这两点不在一条线上。默认值为 0。
#  返回值 lines 是由 numpy.ndarray 类型的元素构成的，其中每个元素都是一对浮点数，表示检测到的直线的参数，即(r, θ)。
lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 100,None, 100,4)
# 遍历每一条直线
for line in lines:
    x1, y1, x2, y2 = line[0]
    cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
cv2.imshow("result", img)
cv2.waitKey(0)
cv2.destroyAllWindows()