# -*- coding:utf-8 -*-
#
# Created by Drogo Zhang
#
# On 2018-10-01

from http.server import BaseHTTPRequestHandler, HTTPServer
from os import path
from urllib.parse import urlparse
import urllib
import json
import util.json_util as ju
import test

encoding = 'utf-8'
BUFSIZE = 8192

host = "10.66.4.114"
port = 9999
address = (host, port)
real_img_save_path = "datasets/own_data/testA/"
generate_img_save_path = "results/generate_images/"
style_list = ['monet', 'cezanne', 'ukiyoe', 'vangogh', 'ink']


class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):
    # POST
    def do_POST(self):
        try:
            length = int(self.headers['Content-Length'])
            read_data = self.rfile.read(length)
            # post_data = urllib.parse.parse_qs(read_data.decode('utf-8'))
            post_data = json.loads(read_data.decode('utf-8'))
            for key in post_data.keys():
                post_data[key] = post_data[key]
            string = post_data
            print("Received a post in ", post_data['date'])
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            style = ju.decode_json_dir(string, real_img_save_path + "temp.jpg")
            if style not in style_list:
                raise KeyError(
                    "Not include this style. Please make sure your style in followed: " + "  ".join(style_list))
            test.main(style)
        except Exception as e:
            fail_reason = "This string too long!" if "{}".format(e).startswith("Ulti") else "{}".format(e)
            response_json_dir = ju.encode_json_dir("", "fail", "", fail_reason)
            print("Response is ", response_json_dir['msg'])
            self.wfile.write(bytes(json.dumps(response_json_dir), encoding))
        else:
            response_json_dir = ju.encode_json_dir(generate_img_save_path + "temp.png", "success", style)
            self.wfile.write(bytes(ju.encode_json(generate_img_save_path + "temp.png", "success", style), encoding))
            print("Response is ", response_json_dir['msg'])

    def do_GET(self):
        try:
            data = {'Brother': 'plz dont look this page anymore, do give post request!'}
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(data).encode())
        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)


def run():
    address = "10.66.4.114"
    port = 9999
    print('starting server, port', port)

    # Server settings
    server_address = (address, port)
    httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
    print('running server...')
    httpd.serve_forever()


if __name__ == '__main__':
    run()
