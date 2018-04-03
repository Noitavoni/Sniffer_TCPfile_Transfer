#--coding:utf-8--
import psutil
import socket


def getNetworkcardName():
    cardname = []
    info = psutil.net_if_addrs()
    for k, v in info.items():
        for item in v:
            if item[0] == 2 and not item[1] == '127.0.0.1':
                cardname.append(k)
    onlyName = cardname[0]
    return onlyName
    #return cardname


def getHostIP():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


if __name__ == '__main__':
    t = getNetworkcardName()
    print(getHostIP())
    print(t)
