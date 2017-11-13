#coding:utf-8
# import cv2
# import numpy as np
# from matplotlib import pyplot as plt
import subprocess
from PIL import Image,ImageEnhance,ImageFilter

subprocess.call(["tesseract", './code.jpg', "output"])
with open("output.txt", 'r') as f:
    code = f.read()
    code = code.strip()
print code




def get_left_start_point(im):
    start_point = (0,0)
    found = False
    w, h = im.size
    data = list(im.getdata())
    for x in xrange(w):
        for y in xrange(h):
            if data[ y*w + x ] != white:
                found = True
                start_point = (x,y)
                break

        if found:
            break
    return start_point


def remove_line(im, aim):
    w, h = im.size
    data = list(im.getdata())

    for x, y in aim:
        curr = data[y * w + x]
        prev = data[(y - 1) * w + x]
        next = data[(y + 1) * w + x]

        if prev == black and next == black:
            continue

        if prev == black:
            data[y * w + x] = white
            data[(y - 1) * w + x] = white


        elif next == black:
            data[y * w + x] = white
            data[(y + 1) * w + x] = white

        else:
            data[y * w + x] = white









'''
# img_name = '2+.png'
#去除干扰线
im = Image.open('code.jpg')
#图像二值化
enhancer = ImageEnhance.Contrast(im)
im = enhancer.enhance(2)
im = im.convert('1')
data = im.getdata()
w,h = im.size
#im.show()
black_point = 0
for x in xrange(1,w-1):
    for y in xrange(1,h-1):
        mid_pixel = data[w*y+x] #中央像素点像素值
        if mid_pixel == 0: #找出上下左右四个方向像素点像素值
            top_pixel = data[w*(y-1)+x]
            left_pixel = data[w*y+(x-1)]
            down_pixel = data[w*(y+1)+x]
            right_pixel = data[w*y+(x+1)]

            #判断上下左右的黑色像素点总个数
            if top_pixel == 0:
                black_point += 1
            if left_pixel == 0:
                black_point += 1
            if down_pixel == 0:
                black_point += 1
            if right_pixel == 0:
                black_point += 1
            if black_point >= 3:
                im.putpixel((x,y),0)
            #print black_point
            black_point = 0

im.save('code1.jpg')
'''
