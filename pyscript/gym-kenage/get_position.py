import cv2
import random
x = 90
y = 180

#Webカメラで位置を測定
def get_position():
    global x,y
    pos_x = random.randint(0,90)
    pos_y = random.randint(0,90)
    # pos_x = x
    # pos_y = y
    # y -= 80
    return pos_x,pos_y

def get_angle():
    robo_angle = random.randint(0,360)
    return robo_angle
