import cv2
import numpy as np
def select_roi(event, x, y, flags, param):
    global drawing, top_left_pt, bottom_right_pt  # 在函数内部使用这些变量时，引用或修改已经存在于全局作用域中的变量。
    if event == cv2.EVENT_LBUTTONDOWN:  # 如果鼠标事件为左键按下
        drawing = True  # 绘图状态开始
        top_left_pt = (x, y)  # 将按下的坐标赋值

    elif event == cv2.EVENT_LBUTTONUP:  # 如果鼠标事件为左键释放
        drawing = False  # 绘图状态结束
        bottom_right_pt = (x, y)  # 将抬起的坐标赋值

        cv2.rectangle(img, top_left_pt, bottom_right_pt, (0, 0, 255), 2)  # 用红色，线宽为2的线绘图


img = cv2.imread('balloon.bmp')

# 转灰度图
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
drawing = False  # 用于记录是否正在绘制矩形的状态，初始为Flase
top_left_pt, bottom_right_pt = (-1, -1), (-1, -1)  # 矩形的左上角顶点坐标和矩形的右下角顶点坐标初始化
cv2.namedWindow('ROI Selection')  # 创建一个窗口
cv2.setMouseCallback('ROI Selection', select_roi)  # 在创建的窗口中传入回调函数
while True:
    cv2.imshow('ROI Selection', img)
    if cv2.waitKey(1) == 27:  # 按下ESC键退出，执行下面的提取代码
        break

print("矩形左上角横坐标:", top_left_pt[0])
print("矩形左上角纵坐标:", top_left_pt[1])
print("矩形右下角横坐标:", bottom_right_pt[0])
print("矩形右下角纵坐标:", bottom_right_pt[1])
img = img[top_left_pt[1]:bottom_right_pt[1],
      top_left_pt[0]:bottom_right_pt[0]]  # 图像切片的第一个参数是高度，第二个参数是宽度,并且图像的最左上角坐标是（0，0）
# OSTU二值化
ret, thresh = cv2.threshold(img, 0, 255, cv2.THRESH_OTSU)

# 查看二值化效果
cv2.imshow('binary image', thresh)
cv2.waitKey(0)
cv2.destroyAllWindows()