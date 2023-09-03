import cv2 as cv
img = cv.imread('1.jpg')
w = int(img.shape[1] * 5)
h = int(img.shape[0] * 5)
img_origin = cv.resize(img,(w,h))
cv.imshow('1',img_origin)
cv.waitKey()