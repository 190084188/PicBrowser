import numpy as np
import cv2 as cv
import math

def get_pers_pts(event, x, y, flags, param):
    global points_img
    if event == cv.EVENT_LBUTTONDOWN:
        if points_img is None:
            points_img = img.copy()
        image = points_img
        # 绘制绿色圆点标记选择的点
        cv.circle(image, (x, y), 3, (0, 255, 0), -1)  # 第三个参数为选点尺寸大小，第四个参数为选点标记颜色，第五个参数表示颜色填充整个圆
        # 显示带有标记的图像
        namedWindow = 'Points choose'
        cv.imshow(namedWindow, image)
        points.append([x, y])
        if len(points) == 4:
            cv.destroyWindow(namedWindow)
def bi_interportate(img,y,x,y0,x0,k):
    q11 = img[y0, x0,k]
    q21 = img[y0, x0 + 1,k]
    q12 = img[y0 + 1, x0,k]
    q22 = img[y0 + 1, x0 + 1,k]
    value1 = (q11 * (x0+1 - x) + q21 * (x - x0))
    value2 = (q12 * (x0+1 - x) + q22 * (x - x0))
    q = (value1 * (y0+1 - y) + value2 * (y - y0))
    return q
def bilinear_zoom(img,rate=1.1):
    h,w,c = img.shape
    if rate == 1:
        new_img = img.copy()
    return new_img
    #print(h,w,c)
    # 计算放大后的尺寸
    new_h = int(h*rate)
    new_w = int(w*rate)
    scale = new_w / w
    # 将放大后的坐标映射到原始坐标范围
    h_s = np.arange(0,new_h,dtype=np.uint8)
    w_s = np.arange(0,new_w,dtype=np.uint8)
    img_zoom = np.zeros([new_h, new_w, c], dtype=np.uint8)
    for i in range(new_h):
        for j in range(new_w):
            for k in range(c):
                # 左上角坐标
                hs = i / scale + 0.5 * (1 / scale - 1)
                ws = j / scale + 0.5 * (1 / scale - 1)
                if hs <= 0:
                    hs = 0
                if ws <= 0:
                    ws = 0
                if hs >= h - 1:
                    hs = h - 2
                if ws >= w - 1:
                    ws = w - 2
                h0 = int(hs)
                w0 = int(ws)
                # 获得四个点的像素值
                if h0 < h - 1 and w0 < w - 1:
                    img_zoom[i][j][k] = bi_interportate(img,hs,ws,h0,w0,k)
    # 创建一个空白的放大后尺寸的图像
    #print(h0,w0)
    return img_zoom

def bilinear_skew(img,angel=0):
    angle = angel * math.pi / 180
    h,w,c = img.shape
    skew_matrix = np.array([[1, math.tan(angle), 0],
                            [0, 1, 0]], dtype=np.float32)
    img = cv.warpAffine(img, skew_matrix, (w, h))
    img_skew = np.zeros([h, w, c], dtype=np.uint8)
    for i in range(h):
        for j in range(w):
            for k in range(c):
                hs = i
                ws = j
                if hs <= 0:
                    hs = 0
                if ws <= 0:
                    ws = 0
                if hs >= h - 1:
                    hs = h - 2
                if ws >= w - 1:
                    ws = w - 2
                h0 = int(hs)
                w0 = int(ws)
                img_skew[i][j][k] = bi_interportate(img, hs, ws, h0, w0, k)
    return img_skew

def bilinear_perspect(img):
    h, w, c = img.shape
    cv.imshow('Points choose', img)
    cv.setMouseCallback('Points choose', get_pers_pts,img)
    cv.waitKey(0)
    # 计算透视变换矩阵
    pts1 = np.float32(points)
    pts2 = np.float32([[0, 0], [w, 0], [0, h], [w, h]])
    M = cv.getPerspectiveTransform(pts1, pts2)
    #img_pers = np.zeros(img.shape, img.dtype)
    img_pers = cv.warpPerspective(img,M,(w,h))
    return img_pers
img = cv.imread('1.jpg')
#img_zoom = bilinear_zoom(img,1.5)
#img_skew = bilinear_skew(img,30)
#cv.imshow('1',img_skew)

points = []
points_img = None
img_p = bilinear_perspect(img)
cv.imshow('perspective',img_p)
cv.waitKey()
cv.destroyAllWindows()
