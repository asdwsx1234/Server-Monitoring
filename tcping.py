import socket
import sys
import time
NORMAL=0
ERROR=1
TIMEOUT=5

def ping(ip, port, timeout=TIMEOUT):
    try:
        cs=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        address=(ip,port)
        status=cs.connect_ex(address)
        cs.settimeout(timeout)
        if status != NORMAL:
            return ERROR
        else:
            return NORMAL
    except Exception as e:
        print(ERROR)
        print("error:%s" %e)

#if __name__ == '__main__':
#    print(ping('120.92.176.156',3724))
#ping('192.168.1.102',9999)
