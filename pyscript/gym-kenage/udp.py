from socket import socket, AF_INET, SOCK_DGRAM
def send_goHome(goHome):
    ADDRESS = "157.82.207.141" # M5Stack address
    PORT = 8000
    s = socket(AF_INET, SOCK_DGRAM)
    s.sendto(str(goHome).encode(), (ADDRESS, PORT))
    s.close()
 
