# coding=utf8
# author:Star
# time:13/05/2018

import os
import json
import CodexMRS.vendor.FCIConverter as fc

path = "/Users/quanyewu/Desktop/files/lsi"

list_dirs = os.walk(path)
for root, dirs, files in list_dirs:
    for file in files:
        print(path + "/" + file)
        obj = fc.to_fciObject(path + "/" + file)
        obj.set_code('')
        dic = obj.to_dictionary()
        to_write = json.dumps(dic)
        # print(to_write)
        f = open(path + "/" + file, 'w')
        f.write(to_write)
