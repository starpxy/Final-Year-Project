# coding=utf8
# author:Star
import os
import CodexMRS.vendor.FCIConverter as fc

class Master:
    __blocks = []
    __mappers = []
    __reducers = []

    def init_blocks(self,file_dir):
        for temp in os.walk(file_dir):
            file_names = temp[2]

if __name__ == '__main__':
    Master().init_blocks("/Users/quanyewu/Desktop/Final-Year-Project/Star's Python Workspace/Web App/CodEX/search/supportings/files")