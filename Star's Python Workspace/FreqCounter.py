'''
@author: Star

@time: 06-03-2018

'''
from LogWriter import LogWriter

class FreqCounter:

    lw = ''
    files = ''

    def __init__(self,path=''):
        lw = LogWriter()
        lw.write_info_log("Initialize the Frequency Counter Class")


def main():
    fc = FreqCounter()

if __name__ == '__main__':
    main()