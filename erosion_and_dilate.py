import cv2
import numpy as np
# 读取图片
src = cv2.imread('fish.bmp')
src = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)


# 设置卷积核
def set_kernel(size, types=1, value=255):
    value_inf = 255 - value
    if types == 1:
        k = np.zeros((size, size), np.uint8)
        k.fill(value)
    elif types == 2:
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
    position = []
    for i, row in enumerate(matrix):
        for j, value in enumerate(row):
            if value == number:
                position.append([i, j])
    return position


def my_erode(img, kernel, value):
    structure_position = get_element_position(kernel,value)
    match = 0
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
                x_end = i + k_size // 2+1
                y_start = j - k_size // 2
                y_end = j + k_size // 2+1
                roi = img[x_start:x_end,y_start:y_end]
                for structures in structure_position:
                    if roi[structures[0],structures[1]] == value:
                        match += 1
                if match == len(structure_position):
                    out[i,j]=value
                else:
                    out[i,j]=value_inf
            match = 0
    return out


def my_dilate(img,kernel,value):
    structure_position = get_element_position(kernel,value)
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
                x_end = i + k_size // 2+1
                y_start = j - k_size // 2
                y_end = j + k_size // 2+1
                roi = img[x_start:x_end,y_start:y_end]
                for m, n in structure_position:
                    if roi[m, n] == value:
                        out[i, j] = value  # 如果有匹配就为255
                        break
    return out


kernel = set_kernel(3, 2, 0)
# 图像腐蚀处理
erosion = my_erode(src, kernel,0)
dilate = my_dilate(src,kernel,0)
# 显示图像
cv2.imshow("erosion", erosion)
cv2.imshow("dilate",dilate)
# 等待显示
cv2.imshow("src", src)
cv2.waitKey(0)
cv2.destroyAllWindows()
