# coding=utf8
# author:Star
import os
import CodexMRS.vendor.FCIConverter as fc


class Master:
    __block_size = 100
    __max_block_num = 10
    __blocks = []
    __mappers = []
    __reducers = []

    def init_blocks(self, file_dir):
        for temp in os.walk(file_dir):
            file_names = temp[2]
            total_num = len(file_names)
            for i in range(1, int(total_num / self.__block_size), 1):
                self.__blocks.append({i: file_names[i:min((total_num - i * self.__block_size), self.__block_size)]})


if __name__ == '__main__':
    Master().init_blocks("/Users/quanyewu/Desktop/files")
