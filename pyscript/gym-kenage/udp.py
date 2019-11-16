from socket import socket, AF_INET, SOCK_DGRAM
def send_goHome(goHome):
    ADDRESS = "192.168.2.102" # M5Stack address
    PORT = 8000
    s = socket(AF_INET, SOCK_DGRAM)
    s.sendto(str(goHome).encode(), (ADDRESS, PORT))
    s.close()

def send_pos(pos_x,pos_y):
    ADDRESS = "192.168.2.100" # M5Stack address
    PORT = 8000
    s = socket(AF_INET, SOCK_DGRAM)
    message = "{},{}".format(pos_x,pos_y)
    s.sendto(message.encode(), (ADDRESS, PORT))
    s.close()
