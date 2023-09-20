import cv2
import numpy as np
points = []
img = cv2.imread('1.jpg')
def click_event(event, x, y, flags, param):
    imgcopy = img.copy()
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(img, (x, y), 5, (0, 0, 255), -1)
        points.append((x, y))
        if len(points) == 4:
            cv2.destroyAllWindows()


cv2.imshow('image', img)
h,w,c=img.shape
cv2.setMouseCallback('image', click_event)
cv2.waitKey(0)
pts1 = np.float32(points)
pts2 = np.float32([[0,0],[w,0],[0,h],[w,h]])

M = cv2.getPerspectiveTransform(pts1,pts2)
result = cv2.warpPerspective(img,M,(w,h))
cv2.imshow('dst',result)
cv2.waitKey()
cv2.destroyAllWindows()