from get_position import get_position
import numpy as np
from Q_request_handler import POST
import time
from udp import send_goHome

X_HOME = 0
Y_HOME = 45
progress = 0

def go_home(n):
    #位置確認
    #Home positionにいるならgoHome=0で止まるまで待ってbreak
    #いないならgoHome=1
    while(1):
        pos_x,pos_y = get_position(n)
        print(pos_x,pos_y,distance(pos_x,pos_y,X_HOME,Y_HOME))
        if(distance(pos_x,pos_y,X_HOME,Y_HOME) < 40): #ホームポジションに戻った時
            # send_goHome(0)
            print("home now")
            # send_goHome(-1)
            # time.sleep(3)
            # send_goHome(0)
            break
        else:#ホームから離れているとき
            # send_goHome(1)
            pass

def leave_home(pos_x,pos_y,post_pos_x,post_pos_y):
    pos_d =  distance(post_pos_x,post_pos_y,X_HOME,Y_HOME)
    cur_d = distance(pos_x,pos_y,X_HOME,Y_HOME)
    progress = cur_d - pos_d
    print("progress:{}".format(progress))
    roll_second = progress % 60 + 2
    print("roll_second={}".format(roll_second))
    if progress > 40:
        send_goHome(-1)
        time.sleep(roll_second)
        send_goHome(0)
    else:
        send_goHome(0)

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
