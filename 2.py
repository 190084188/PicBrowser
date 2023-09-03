import cv2
import numpy as np

img = cv2.imread("C:\\Users\\Lismoon\\Desktop\\logo.png")
cv2.imshow('src', img)
print(img.shape)

result = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)

for i in range(0, img.shape[0]):  # 访问所有行
    for j in range(0, img.shape[1]):  # 访问所有列
        if img[i, j, 0] > 200 and img[i, j, 1] > 200 and img[i, j, 2] > 200:
            result[i, j, 3] = 0

cv2.imwrite('C:\\Users\\Lismoon\\Desktop\\logo1.png', result, [int(cv2.IMWRITE_PNG_COMPRESSION), 0])
print(result.shape)
cv2.imshow('result', result)
B, G, R, A = cv2.split(result)
cv2.imshow('B', B)
cv2.imshow('G', G)
cv2.imshow('R', R)
cv2.imshow('A', A)

cv2.waitKey()
cv2.destroyAllWindows()
