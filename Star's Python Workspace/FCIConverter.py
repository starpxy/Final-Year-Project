'''
@author: Star

@time: 06-03-2018

This is to convert Formatted Code interface into JSON or read JSON file into FCI object

'''
import os
import json
import hashlib
from LogWriter import LogWriter
from FormattedCodeInterface import FormattedCodeInterface

def to_json_str(fci_object):
    if isinstance(fci_object,FormattedCodeInterface):
        dic = fci_object.to_dictionary()
        return json.dumps(dic,sort_keys=True)
    else:
        lw = LogWriter()
        lw.write_error_log("Method 'to_json' in FCIConverter requires an FCI type of object as parameter!")
        exit()

def to_json_file(path,fci_object):
    to_write = to_json_str(fci_object)
    if not os.path.exists(path):
        os.mkdir(path)
    m = hashlib.md5()
    m.update(to_write.encode("utf8"))
    f_name = m.hexdigest()
    f = open(path+"/"+f_name+".json","w",encoding="utf-8")
    f.write(to_write)
    f.close()

# def to_dic(file_name):
#