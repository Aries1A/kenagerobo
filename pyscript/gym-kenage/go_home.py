from get_position import get_position
import numpy as np
from Q_request_handler import POST
import time
from udp import send_goHome

X_HOME = 264
Y_HOME = 135

def go_home():
    #位置確認
    #Home positionにいるならgoHome=0で止まるまで待ってbreak
    #いないならgoHome=1
    while(1):
        pos_x,pos_y = get_position(1)
        print(pos_x,pos_y,distance(pos_x,pos_y,X_HOME,Y_HOME))
        if(distance(pos_x,pos_y,X_HOME,Y_HOME) < 64): #ホームポジションに戻った時
            send_goHome(0)
            print("home now")
            break
        else:#ホームから離れているとき
            send_goHome(1)
        time.sleep(0.2)
def leave_home():
    send_goHome(-1)

def stop_roll():
    pos_x,pos_y = get_position(1)
    if distance(pos_x,pos_y,X_HOME,Y_HOME)<30:
        send_goHome(0)
    else:
        send_goHome(-1)

def distance(x1,y1,x2,y2):
    a = np.array([x1, y1])
    b = np.array([x2, y2])
    u = b - a
    return np.linalg.norm(u)
