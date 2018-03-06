'''
@author: Star

@time: 06-03-2018

'''
import os
from LogWriter import LogWriter
from FormattedCodeInterface import FormattedCodeInterface

class FreqCounter:
    lw = ''
    files = ''
    fci_list = []
    dic = {}

    def __init__(self, path):
        lw = LogWriter()
        lw.write_info_log("Initialize the Frequency Counter Class")
        if not os.path.exists(path):
            lw.write_error_log("")
            exit()

def main():
    fc = FreqCounter()


if __name__ == '__main__':
    main()
