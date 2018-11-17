# -*- coding:utf-8 -*-
#
# Created by Drogo Zhang
#
# On 2018-10-01


import http.client
import urllib.parse
import requests
import util.json_util as ju
import json
import urllib

encoding = 'utf-8'


# values = urllib.parse.urlencode(data).encode(encoding='UTF8')
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = {"Content-type": "application/json", 'User-Agent': user_agent}
url = "http://10.66.4.114:9999/"
conn = http.client.HTTPConnection("10.66.4.114", 9999)


# user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
#
# headers = {}
data = ju.encode_json_dir("datasets/own_data/testB/timg.jpg", "success", "monet")
# print("dictionary:")
# for key in data.keys():
#     print("key:", key, "   ", "type", type(key))
#     print("value:", data[key], "   ", "type", type(data[key]))
#
# print("\n\nurllib.parse.urlencode:")
# print(urllib.parse.urlencode(data, encoding))
# exit()
conn.request('POST', url, urllib.parse.urlencode(data, encoding), headers)
response = conn.getresponse()
print(response.status, response.reason)
data = response.read().decode(encoding)
print(data)
conn.close()
