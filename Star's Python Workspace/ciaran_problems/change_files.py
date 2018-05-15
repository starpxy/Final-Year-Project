# coding=utf8
# author:Star
# time:13/05/2018

import os
import json
import CodexMRS.vendor.FCIConverter as fc


def convert(origin_str):
    after = ''
    buffer = 0
    for i in origin_str:
        if i == '\\':
            print('in')
            buffer += 1
        else:
            if buffer != 0:
                print(buffer)
                for j in range(int(buffer / 4)):
                    after += r'\\'
            after += i
            buffer = 0
    return after


path = "/Users/quanyewu/Desktop/files/so_50k"

list_dirs = os.walk(path)
for root, dirs, files in list_dirs:
    i = 0
    for file in files:
        # print(path + "/" + file)
        obj = fc.to_fciObject(path + "/" + file)
        # obj.set_code()
        # dic = obj.to_dictionary()
        # to_write = json.dumps(dic)
        to_write = obj.get_code()
        print(to_write)
        print('---------------------')
        print(convert(to_write))
        print('==============================')
        i += 1
        if i == 3:
            break
            # f = open(path + "/" + file, 'w')
            # f.write(to_write)
