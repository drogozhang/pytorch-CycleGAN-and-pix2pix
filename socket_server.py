# -*- coding:utf-8 -*-
#
# Created by Drogo Zhang
#
# On 2018-09-17

import threading
import socket
import util.json_util as ju
import test
import time

encoding = 'utf-8'
BUFSIZE = 8192

host = "10.66.4.114"
port = 9999
address = (host, port)
real_img_save_path = "datasets/own_data/testA/"
generate_img_save_path = "results/generate_images/"
style_list = ['monet', 'cezanne', 'ukiyoe', 'vangogh']

# a read thread, read data from remote


class Reader(threading.Thread):
    def __init__(self, client):
        threading.Thread.__init__(self)
        self.client = client

    def run(self):
        data = ""
        while True:
            temp = self.client.recv(BUFSIZE)
            if temp:
                data += str(temp, encoding)
                print(str(temp, encoding))
                if str(temp, encoding).endswith("}"):
                    break
            else:
                break
        try:
            string = data
            style = ju.decode_json(string, real_img_save_path + "temp.jpg") if ju.decode_json(string,
                                                                                              real_img_save_path + "temp.jpg") else ""
            if style not in style_list:
                raise KeyError(
                    "Not include this style. Please make sure your style in followed: " + "  ".join(style_list))
        except Exception as e:
            fail_reason = "This string too long!" if "{}".format(e).startswith("Ulti") else "{}".format(e)
            self.client.sendall(bytes(ju.encode_json("", "fail", "", fail_reason), encoding=encoding))

        else:
            test.main(style)
            self.client.sendall(
                bytes(ju.encode_json(generate_img_save_path + "temp.png", "success", style), encoding=encoding))
        self.client.close()


    def readline(self):
        rec = self.inputs.readline()
        if rec:
            string = bytes.decode(rec, encoding)
            if len(string) > 2:
                string = string[0:-2]
            else:
                string = ' '
        else:
            string = False
        return string


# a listen thread, listen remote connect
# when a remote machine request to connect, it will create a read thread to handle
class Listener(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.sock.setblocking(0)
        # self.sock.settimeout(0.5)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(address)
        self.sock.listen(5)

    def run(self):
        print("listener started")
        while True:
            client, cltadd = self.sock.accept()
            Reader(client).start()
            cltadd = cltadd
            print("accept a connect")


lst = Listener()  # create a listen thread
lst.start()  # then start


