import random
import cv2
import numpy as np

# 读取图像
img = cv2.imread('../qipan.bmp')

# 转化为灰度图
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Canny边缘检测
edges = cv2.Canny(gray, 50, 150)

# Hough变换检测线段
lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 160, maxLineGap=250)

# 绘制检测到的线段
for line in lines:
    x1, y1, x2, y2 = line[0]
    cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 10)


# 自定义的robust拟合直线函数
def robust_fit_line(points, threshold):
    best_fit = None
    max_inlier_cnt = 0

    for i in range(100):

        # 随机选择两个点
        sample = random.sample(list(points), 2)
        x1, y1 = sample[0]
        x2, y2 = sample[1]

        # 拟合一条过这两点的直线
        k = (y2 - y1) / (x2 - x1)
        b = y1 - k * x1

        # 计算点到直线的距离
        distances = np.abs(points[:, 1] - (k * points[:, 0] + b))

        # 统计在阈值内的内点数
        inlier_cnt = np.sum(distances < threshold)

        # 更新最佳拟合直线
        if inlier_cnt > max_inlier_cnt:
            max_inlier_cnt = inlier_cnt
            best_fit = [k, b]

    return best_fit


# 生成6个在附近的内点
inliers = []
k = 1
b = 10
for i in range(6):
    x = random.randint(100, 500)
    y = k * x + b + random.randint(-3, 3)
    inliers.append([x, y])

# 生成1个外点
outlier = [random.randint(0, 640), random.randint(0, 480)]

# 合并所有点
points = np.array(inliers + [outlier])

# 稳健拟合直线
fit_line = robust_fit_line(points, 100)

# 画出拟合直线
img2 = np.zeros((512, 512, 3), np.uint8)
cv2.line(img2, (0, int(fit_line[1])), (511, int(fit_line[0] * 511 + fit_line[1])), (0, 255, 0), 2)

# 画出所有样本点
for pt in points:
    cv2.circle(img2, (pt[0], pt[1]), 5, (0, 0, 255), -1)

# 显示结果
cv2.namedWindow('edge', cv2.WINDOW_NORMAL)
cv2.imshow('edge', img)
cv2.imshow('fitting', img2)
cv2.waitKey(0)
cv2.destroyAllWindows()