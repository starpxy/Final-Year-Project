'''
@author: Star

@time: 06-03-2018

This is to convert Formatted Code interface into JSON or read JSON file into FCI object

'''
import os
import json
import hashlib
from LogWriter import LogWriter
from FCI.FormattedCodeInterface import FormattedCodeInterface


def to_json_str(fci_object):
    if isinstance(fci_object, FormattedCodeInterface):
        dic = fci_object.to_dictionary()
        return json.dumps(dic, sort_keys=True)
    else:
        lw = LogWriter()
        lw.write_error_log("Method 'to_json' in FCIConverter requires an FCI type of object as parameter!")
        exit()


def to_local_json_file(path, fci_object):
    to_write = to_json_str(fci_object)
    if not os.path.exists(path):
        os.mkdir(path)
    m = hashlib.md5()
    m.update(to_write.encode("utf8"))
    f_name = m.hexdigest()
    fci_object.set_id(f_name)
    to_write = to_json_str(fci_object)
    f = open(path + "/" + f_name + ".json", "w", encoding="utf-8")
    f.write(to_write)
    f.close()


def to_master_json_file(path, fci_object, connection):
    to_write = to_json_str(fci_object)
    if not connection.isdir(path):
        connection.mkdir(path)
    m = hashlib.md5()
    m.update(to_write.encode("utf8"))
    f_name = m.hexdigest()
    fci_object.set_id(f_name)
    to_write = to_json_str(fci_object)
    f = connection.open_file(path + "/" + f_name + ".json", "w")
    f.write(to_write)
    f.close()


def to_dic(file_name):
    if not os.path.exists(file_name):
        lw = LogWriter()
        lw.write_error_log("File " + file_name + " doesn't exist!")
    else:
        f = open(file_name, 'r', encoding="utf-8")
        dic = json.load(f)
        return dic


def to_fciObject(file_name):
    return FormattedCodeInterface().from_dictionary(to_dic(file_name))
