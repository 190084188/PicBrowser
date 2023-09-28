import cv2
import numpy as np

# 读取图片
src = cv2.imread('fish.bmp')
src = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)


# 设置卷积核,size定义的是卷积核的大小，types是卷积核的类型（均值卷积核和十字），value是结构元素的值
def set_kernel(size, types=1, value=255):
    value_inf = 255 - value  # 背景
    if types == 1:  # 均值卷积核
        k = np.zeros((size, size), np.uint8)
        k.fill(value)
    elif types == 2:  # 十字卷积核
        k = np.zeros((size, size), np.uint8)
        k.fill(value_inf)
        if size % 2 != 0:
            k[int(size / 2 - 0.5)].fill(value)
            k[:, int(size / 2 - 0.5)].fill(value)
        else:
            k[size / 2].fill(value)
            k[:size / 2].fill(value)
    return k


def get_element_position(matrix, number):
    position = []  # 把位置存入列表中
    for i, row in enumerate(matrix):  # 对矩阵进行枚举，返回结构元素的位置
        for j, value in enumerate(row):
            if value == number:
                position.append([i, j])
    return position


# 传入待处理图片，卷积核和ROI的灰度值
def my_erode(img, kernel, value):
    # 先得到结构元素位置
    structure_position = get_element_position(kernel, value)
    # 设定匹配标志
    match = 0
    # 背景色
    value_inf = 255 - value
    h, w = img.shape
    k_size = len(kernel)
    out = img.copy()
    for i in range(h - 1):
        for j in range(w - 1):
            # 图像四边处理为背景色
            if i + 1 < k_size / 2 or j + 1 < k_size / 2 or h - 1 - i < k_size / 2 or w - 1 - j < k_size / 2:
                out[i, j] = value_inf
            else:
                # 得到roi区域的图像矩阵，大小和卷积核一样
                x_start = i - k_size // 2
                x_end = i + k_size // 2 + 1
                y_start = j - k_size // 2
                y_end = j + k_size // 2 + 1
                roi = img[x_start:x_end, y_start:y_end]
                for structures in structure_position:
                    if roi[structures[0], structures[1]] == value:
                        match += 1
                # 如果全匹配则保留，否则为背景色
                if match == len(structure_position):
                    out[i, j] = value
                else:
                    out[i, j] = value_inf
            match = 0
    return out


def my_dilate(img, kernel, value):
    structure_position = get_element_position(kernel, value)
    value_inf = 255 - value
    h, w = img.shape
    k_size = len(kernel)
    out = img.copy()
    for i in range(h - 1):
        for j in range(w - 1):
            if i + 1 < k_size / 2 or j + 1 < k_size / 2 or h - 1 - i < k_size / 2 or w - 1 - j < k_size / 2:
                out[i, j] = value_inf
            else:
                x_start = i - k_size // 2
                x_end = i + k_size // 2 + 1
                y_start = j - k_size // 2
                y_end = j + k_size // 2 + 1
                roi = img[x_start:x_end, y_start:y_end]
                for m, n in structure_position:
                    if roi[m, n] == value:
                        out[i, j] = value  # 如果有匹配就为255
                        break
    return out


# img = cv2.imread("fish.bmp", cv2.IMREAD_GRAYSCALE)
# v1 = cv2.Canny(img, 100, 200)  # 80为minVal(越小标准越低), 150为maxVal（越小标准越低）
# cv2.imshow('res', v1)
# kernel = set_kernel(3, 2, 0)
# ero_cv = cv2.erode(src, kernel)
# dilate_cv =cv2.dilate(src, kernel)
# # 图像腐蚀处理
# erosion = my_erode(src, kernel, 0)
# dilate = my_dilate(src, kernel, 0)
# # 显示图像
# cv2.imshow("erosion", erosion)
# cv2.imshow("dilate", dilate)
# cv2.imshow("erosion_cv", ero_cv)
# cv2.imshow("dilate_cv", dilate_cv)
# # 等待显示
# cv2.imshow("src", src)
chair = cv2.imread("chair.bmp")
cv2.waitKey(0)
cv2.destroyAllWindows()
