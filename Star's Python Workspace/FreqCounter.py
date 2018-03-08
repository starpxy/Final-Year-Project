'''
@author: Star

@time: 06-03-2018

'''
import os
from LogWriter import LogWriter
import FCIConverter
from FormattedCodeInterface import FormattedCodeInterface

class FreqCounter:
    files = ''
    fci_list = []
    dic = {}

    def __init__(self, file_path):
        lw = LogWriter()
        lw.write_info_log("Initialize the Frequency Counter Class")
        if not os.path.exists(file_path):
            lw.write_error_log("Path "+file_path+" doesn't exist!")
            exit()
        else:
            files = os.listdir(file_path)
            self.files = files
            for file in files:
                if len(file)==37:
                    if not os.path.isdir(file):
                        try:
                            f = FCIConverter.to_fciObject(file_path+"/"+file)
                            self.fci_list.append(f)
                        except:
                            lw.write_error_log("File type error!")
    def get_frequency_list(self):
        for o in self.fci_list:
            content = o.get_content()
            tokens = str(content).split(' ')
            print(tokens)

def main():
    fc = FreqCounter("files")
    fc.get_frequency_list()

if __name__ == '__main__':
    main()
