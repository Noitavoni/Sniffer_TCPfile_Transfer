from scapy.all import *
import getEntName
import platform
import time
import threading
import socket
import os
import getName

HOST = '192.168.10.248'
PORT = 9999
BUF_SIZE = 1024
FILENAME_PATTERN = 'data'
number_of_packet=50
HOST_IP = getName.getHostIP()


class SniffData(object):
    @staticmethod
    def packet_callback(packet):
        #print(packet.show())
        pass

    def ChoosePlatform(self):
        global file_seq_num
        SystemPlatform = platform.system()
        print(SystemPlatform)

        if SystemPlatform =='Darwin':
            data = sniff(count=number_of_packet)
            wrpcap('data%d.pcap'%file_seq_num, data)
            file_seq_num += 1
            print(file_seq_num)

        elif SystemPlatform =='Windows':
            print('This is windows')
            data = sniff(prn=SniffData.packet_callback, count=number_of_packet)
            wrpcap('data%d.%s.pcap' % (file_seq_num, HOST_IP), data)
            file_seq_num += 1

        elif SystemPlatform =='Linux':
            print('This is Linux')
            data = sniff(prn=SniffData.packet_callback)
            wrpcap('data%d.%s.pcap'%(file_seq_num, HOST_IP), data)

        else:
            raise ValueError('Sniffer has not been implemented on this platform')


class SendData():
    def filesDir(self, path):
        file_list = list()
        files = os.listdir(path)
        for fl in files:
            if fl.startswith(FILENAME_PATTERN):
                file_list.append(fl)
            else:
                pass
        return file_list

    def sendFile(self, filename):
        name = os.getcwd() + '\\' + filename
        file_name = os.path.basename(name)
        file_size = os.stat(name).st_size
        sk.sendall((file_name + '|' + str(file_size)).encode())
        data = sk.recv(1024)
        print(data)
        send_size = 0
        f = open(name, 'rb')
        Flag = True
        while Flag:
            if send_size + 1024 > file_size:
                data = f.read(file_size - send_size)
                Flag = False
            else:
                data = f.read(1024)
                send_size += 1024
            sk.sendall(data)
        f.close()
        os.remove(filename)


if __name__ == "__main__":
    ip_port = (HOST, PORT)
    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sk.connect(ip_port)
    file_seq_num = 0
    test = SniffData()
    test2 = SendData()
    while True:
        t1 = threading.Thread(target=test.ChoosePlatform)
        t1.start()
        t1.join()
        PATH = os.getcwd()
        sender = test2.filesDir(PATH)
        for file in sender:
            t2 = threading.Thread(target=test2.sendFile(file))
            t2.start()
    sk.close()






