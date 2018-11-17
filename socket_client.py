# -*- coding:utf-8 -*-
#
# Created by Drogo Zhang
#
# On 2018-09-17


import socket
import util.json_util as ju

HOST = '10.66.4.114'
PORT = 9999
BUFSIZE = 8192
encoding = 'utf-8'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

count = 1
while True:
    if count == 2:
        s.close()
        exit()
    msg = bytes(ju.encode_json("datasets/own_data/testB/timg.jpg", "success", "monet"), encoding=encoding)

    if len(msg) == 0:
        continue
    elif msg == "exit":
        break
    s.send(msg)
    # s.close()
    # s.connect((HOST, PORT))
    count += 1
    data = s.recv(BUFSIZE)
    print('Received', str(data, encoding=encoding))

s.close()
