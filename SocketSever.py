#!/usr/bin/python27
#coding:utf-8

import socketserver
import os
import time

BUF_SIZE = 1024
PORT = 9999
PCAP_STORE_PATH = r'C:\Users\Jerry\PycharmProjects\Cookbook\PCAP'


class myserver(socketserver.StreamRequestHandler):

    def handle(self):
        base_path = PCAP_STORE_PATH
        conn = self.request
        print('connected...')
        while True:
            pre_data = conn.recv(BUF_SIZE)
            print(len(pre_data))
            print('===================')
            if len(pre_data) == 0:
                time.sleep(2)
                continue
            file_name,file_size = pre_data.split(('|').encode())
            recv_size = 0
            file_dir = os.path.join(base_path.encode(),file_name)
            conn.send('send file'.encode())
            f = open(file_dir, 'wb')

            print(file_size)
            flag = True
            while flag:
                if int(file_size) > recv_size:
                    data = conn.recv(BUF_SIZE)
                    recv_size += len(data)
                else:
                    break
                f.write(data)
            print('upload successed')
            f.close()
            print('传输完成')
            time.sleep(3)


if __name__ == '__main__':
    print('Begin to Listen')
    instance = socketserver.ThreadingTCPServer(('0.0.0.0', PORT), myserver)
    instance.serve_forever()
