# -*- coding:utf-8 -*-
#
# Created by Drogo Zhang
#
# On 2018-10-12
import cv2

dataroot = "datasets/own_data/testA/"

img = cv2.imread(dataroot + "temp.jpg")
img_shape = tuple([item * 2 for item in img.shape[:-1]])

img = cv2.resize(img, img_shape, interpolation=cv2.INTER_CUBIC)
print(img.shape[0:2])
