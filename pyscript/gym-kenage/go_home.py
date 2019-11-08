from get_position import get_position
import numpy as np
from Q_request_handler import POST
import time

X_HOME = 90
Y_HOME = 0

def go_home():
    #位置確認
    #Home positionにいるならgoHome=0で止まるまで待ってbreak
    #いないならgoHome=1
    while(1):
        pos_x,pos_y = get_position()
        print(pos_x,pos_y,distance(pos_x,pos_y,X_HOME,Y_HOME))
        if(distance(pos_x,pos_y,X_HOME,Y_HOME) < 50):
            POST(name="set_goHome",data="0")
            time.sleep(5)
            while(int(POST(name="get_moving"))):
                time.sleep(1)
            break
        else:
            while(int(POST(name="get_moving"))):
                time.sleep(1)
            POST(name="set_goHome",data="1")
            time.sleep(1)



def distance(x1,y1,x2,y2):
    a = np.array([x1, y1])
    b = np.array([x2, y2])
    u = b - a
    return np.linalg.norm(u)
