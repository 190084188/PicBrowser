import cv2
import numpy as np
from scipy import stats

# 读取图像
img = cv2.imread('../qipan.bmp')
# 转化为灰度图
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# Canny边缘检测
edges = cv2.Canny(gray, 50, 150)
# Hough变换检测线段
lines = cv2.HoughLinesP(edges, 1, np.pi/180, 160, maxLineGap=250)
for line in lines:
    x1,y1,_,_ = line[0]
    cv2.circle(img,(x1,y1),1,(0,0,255),10)
# 提取所有线段端点
x = lines[:,0, [0,2]].ravel()
y = lines[:,0, [1,3]].ravel()
# 鲁棒最小二乘拟合
slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
# 生成拟合直线
line_x = np.arange(img.shape[1])
line_y = slope * line_x + intercept
# 绘制拟合直线
line_x = line_x.astype(int)
line_y = line_y.astype(int)
cv2.line(img, (line_x[0], line_y[0]), (line_x[-1], line_y[-1]), (0,0,255), 2)
cv2.namedWindow('robust_lines',cv2.WINDOW_NORMAL)
# 显示结果
cv2.imshow('robust_lines', img)
cv2.waitKey(0)
cv2.destroyAllWindows()