from Q_request_handler import POST
from udp import send_pos
#Webカメラで位置を測定
import cv2
import math
import numpy as np
import os

pos_x = 0
pos_y = 45
post_pos_x = 0
post_pos_y = 45

# 線分ABと線分CDの交点を求める関数
def _calc_cross_point(pointA, pointB, pointC, pointD):
    cross_point = (0,0)
    bunbo = (pointB[0] - pointA[0]) * (pointD[1] - pointC[1]) - (pointB[1] - pointA[1]) * (pointD[0] - pointC[0])
    # 直線が平行な場合
    if (bunbo == 0):
        return False, cross_point
    vectorAC = ((pointC[0] - pointA[0]), (pointC[1] - pointA[1]))
    r = ((pointD[1] - pointC[1]) * vectorAC[0] - (pointD[0] - pointC[0]) * vectorAC[1]) / bunbo
    s = ((pointB[1] - pointA[1]) * vectorAC[0] - (pointB[0] - pointA[0]) * vectorAC[1]) / bunbo
    # rを使った計算の場合
    distance = ((pointB[0] - pointA[0]) * r, (pointB[1] - pointA[1]) * r)
    cross_point = [int(pointA[0] + distance[0]), int(pointA[1] + distance[1])]
    return cross_point


A = [68, 540]
B = [559,659]
C = [1053,16]
D = [1086,560]
S1 = [23,177] #左上
S2 = A #左下
S3 = C #右上
S4 = _calc_cross_point(A,B,C,D)  #右下
width = 270 * 3
height = 90 * 3


def get_position(n):
    global pos_x,pos_y,post_pos_x,post_pos_y
    cap = cv2.VideoCapture(n)
    if not cap.isOpened():
        return
    ret, frame = cap.read()

    # 変換前後の対応点を設定
#     p_original = np.float32([ [240,213],[72,510], [1121,220], [1280, 522]])
    p_original = np.float32([S1,S2,S3, S4])
    p_trans = np.float32([[0,0], [0,height], [width,0], [width,height]])
    # 変換マトリクスと射影変換
    M = cv2.getPerspectiveTransform(p_original, p_trans)
    trans = cv2.warpPerspective(frame, M, (width, height))
    trans = cv2.cvtColor(trans, cv2.COLOR_BGR2GRAY)

    # 画像の読み込み
    img_src1 = cv2.imread("../imgs/baseline/base_0.jpg", 0)
    # img_src2 = cv2.imread("./img_square/camera_capture_2.jpg", 0)
    img_src2 = trans

    # print(img_src1.shape)
    # print(img_src2.shape)


    # 背景画像との差分を算出
    img_diff = cv2.absdiff(img_src2, img_src1)

    # 差分を二値化
    img_diffm = cv2.threshold(img_diff, 20, 255, cv2.THRESH_BINARY)[1]
    # 膨張処理、収縮処理を施してマスク画像を生成
    operator = np.ones((3, 3), np.uint8)
    img_dilate = cv2.dilate(img_diffm, operator, iterations=4)
    img_mask = cv2.erode(img_dilate, operator, iterations=4)
    kernel = np.ones((5,5),np.float32)/40
    img_mask = cv2.filter2D(img_mask,-1,kernel)

    # マスク画像を使って対象を切り出す
    img_dst = cv2.bitwise_and(img_src2, img_mask)
    image, contours, hierarchy = cv2.findContours(img_dst,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        # 輪郭に外接する円を取得する。
        center, radius = cv2.minEnclosingCircle(cnt)
        area = cv2.contourArea(cnt)
#         print(area)
        if(area>1200 and area < 3000):
            pos_x = center[0] / img_src1.shape[1]  * width / 3
            pos_y = center[1] / img_src1.shape[0] * height / 3
            print(pos_x,pos_y,area)
    # cv2.imshow('frame',img_dst)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    send_pos(pos_x,pos_y)
    return pos_x,pos_y

def change_base(n):
    cap = cv2.VideoCapture(n)
    if not cap.isOpened():
        print("no camera")
    ret, frame = cap.read()

    # 変換前後の対応点を設定
    p_original = np.float32([S1,S2,S3, S4])
    width = 270 * 3
    height = 90 * 3
    p_trans = np.float32([[0,0], [0,height], [width,0], [width,height]])# 変換マトリクスと射影変換
    M = cv2.getPerspectiveTransform(p_original, p_trans)
    trans = cv2.warpPerspective(frame, M, (width, height))
    cv2.imshow('frame',trans)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    base_path = os.path.join("../imgs/baseline/", "base")
    return cv2.imwrite('{}_{}.{}'.format(base_path, 0, "jpg"), trans)

def get_angle():
    robo_angle = int(POST(name="get_angle"))
    print("robo_angle= {}".format(robo_angle))
    return robo_angle

def get_goal():
    goal_x = 260
    goal_y = 45
    return goal_x, goal_y

if __name__ == '__main__':
    print(change_base(1))

    # get_position(1)
