import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

# 计算灰度直方图
def select_roi(event, x, y, flags, param):
    global drawing, top_left_pt, bottom_right_pt  # 在函数内部使用这些变量时，引用或修改已经存在于全局作用域中的变量。
    if event == cv.EVENT_LBUTTONDOWN:  # 如果鼠标事件为左键按下
        drawing = True  # 绘图状态开始
        top_left_pt = (x, y)  # 将按下的坐标赋值

    elif event == cv.EVENT_LBUTTONUP:  # 如果鼠标事件为左键释放
        drawing = False  # 绘图状态结束
        bottom_right_pt = (x, y)  # 将抬起的坐标赋值

        cv.rectangle(img, top_left_pt, bottom_right_pt, (0, 0, 255), 2)  # 用红色，线宽为2的线绘图

def calcGrayHist(grayimage):
    # 灰度图像矩阵的高，宽
    rows, cols = grayimage.shape

    # 存储灰度直方图
    grayHist = np.zeros([256], np.uint64)
    for r in range(rows):
        for c in range(cols):
            grayHist[grayimage[r][c]] += 1

    return grayHist

# 阈值分割：直方图技术法
def threshTwoPeaks(image):

    #转换为灰度图
    if len(image.shape) == 2:
        gray = image
    else:
        gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    # 计算灰度直方图
    histogram = calcGrayHist(gray)
    # 寻找灰度直方图的最大峰值对应的灰度值
    maxLoc = np.where(histogram == np.max(histogram))
    firstPeak = maxLoc[0][0] #灰度值
    # 寻找灰度直方图的第二个峰值对应的灰度值
    measureDists = np.zeros([256], np.float32)
    for k in range(256):
        measureDists[k] = pow(k - firstPeak, 2) * histogram[k] #综合考虑 两峰距离与峰值
    maxLoc2 = np.where(measureDists == np.max(measureDists))
    secondPeak = maxLoc2[0][0]
    print('双峰为：',firstPeak,secondPeak)
    # 找到两个峰值之间的最小值对应的灰度值，作为阈值
    thresh = 0
    if firstPeak > secondPeak:  # 第一个峰值再第二个峰值的右侧
        temp = histogram[int(secondPeak):int(firstPeak)]
        minloc = np.where(temp == np.min(temp))
        thresh = secondPeak + minloc[0][0] + 1
    else:  # 第一个峰值再第二个峰值的左侧
        temp = histogram[int(firstPeak):int(secondPeak)]
        minloc = np.where(temp == np.min(temp))
        thresh = firstPeak + minloc[0][0] + 1

    # 找到阈值之后进行阈值处理，得到二值图
    threshImage_out = gray.copy()
    # 大于阈值的都设置为255
    threshImage_out[threshImage_out > thresh] = 255
    threshImage_out[threshImage_out <= thresh] = 0
    return thresh, threshImage_out

if __name__ == "__main__":
    img = cv.imread('baboon.png')
    drawing = False  # 用于记录是否正在绘制矩形的状态，初始为Flase
    top_left_pt, bottom_right_pt = (-1, -1), (-1, -1)  # 矩形的左上角顶点坐标和矩形的右下角顶点坐标初始化
    cv.namedWindow('ROI Selection')  # 创建一个窗口
    cv.setMouseCallback('ROI Selection', select_roi)  # 在创建的窗口中传入回调函数
    while True:
        cv.imshow('ROI Selection', img)
        if cv.waitKey(1) == 27:  # 按下ESC键退出，执行下面的提取代码
            break

    # 提取ROI区域
    print("矩形左上角横坐标:", top_left_pt[0])
    print("矩形左上角纵坐标:", top_left_pt[1])
    print("矩形右下角横坐标:", bottom_right_pt[0])
    print("矩形右下角纵坐标:", bottom_right_pt[1])
    roi = img[top_left_pt[1]:bottom_right_pt[1],
          top_left_pt[0]:bottom_right_pt[0]]  # 图像切片的第一个参数是高度，第二个参数是宽度,并且图像的最左上角坐标是（0，0）
    cv.imshow('ROI', roi)
    img_gray = cv.cvtColor(roi, cv.COLOR_RGB2GRAY)
    #灰度直方图曲线
    hist = cv.calcHist([img_gray], [0], None, [256], [0, 255]) #对图像像素的统计分布，它统计了每个像素（0到L-1）的数量。
    plt.plot(hist)
    #灰度直方图
    plt.hist(img_gray.ravel(), 256), plt.title('hist') #ravel()方法将数组维度拉成一维数组
    thresh, img_sep = threshTwoPeaks(roi)
    print('灰度阈值为:',thresh)
    cv.imshow('nose', img_sep)
    cv.waitKey()
    cv.destroyAllWindows()


