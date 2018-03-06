# coding=utf-8
"""
Created on 05/03/2018
Author: Ciarán
"""

import os
from LogWriter import LogWriter

class log:

    def __init__(self):
        self.log = open(os.path.join(os.curdir, 'log.txt'), 'w')

    def write_to_log(self, info):
        self.log
def main():
    lw = LogWriter()
    os.mkdir("logs_test")
    lw.write_error_log("test")
if __name__ == '__main__':
    main()