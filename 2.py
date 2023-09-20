import cv2
import numpy as np
#读取图片
src = cv2.imread('fish.bmp', cv2.IMREAD_UNCHANGED)
#设置卷积核
def set_kernel(size = 3,type = 1 ):
    if type == 1:
        kernel = np.ones((size, size), np.uint8)
    elif type == 2:
        kernel = np.zeros((size,size),np.uint8)
        if size%2 != 0:
            kernel[int(size/2-0.5)].fill(1)
            kernel[:int(size/2-0.5)].fill(1)
        else:
            kernel[size/2].fill(1)
            kernel[:size/2].fill(1)

kernel = set_kernel(3,2)
#图像腐蚀处理
erosion = cv2.erode(src, kernel)
#显示图像
cv2.imshow("src", src)
cv2.imshow("result", erosion)
#等待显示
cv2.waitKey(0)
cv2.destroyAllWindows()