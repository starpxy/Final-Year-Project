'''
@author: Star

@time: 06-03-2018

This is to convert Formatted Code interface into JSON or read JSON file into FCI object

'''
import os
import json
import hashlib
from Interfaces.LogWriter import LogWriter
from Interfaces.FormattedCodeInterface import FormattedCodeInterface


def to_json_str(fci_object):
    if isinstance(fci_object, FormattedCodeInterface):
        dic = fci_object.to_dictionary()
        return json.dumps(dic, sort_keys=True)
    else:
        lw = LogWriter()
        lw.write_error_log("Method 'to_json' in FCIConverter requires an FCI type of object as parameter!")
        exit()


def to_json_file(path, fci_object):
    to_write = to_json_str(fci_object)
    if not os.path.exists(path):
        os.mkdir(path)
    m = hashlib.md5()
    m.update(to_write.encode("utf8"))
    f_name = m.hexdigest()
    f = open(path + "/" + f_name + ".json", "w", encoding="utf-8")
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

ob1 = FormattedCodeInterface()
ob1.set_content("The Neatest Little Guide to Stock Market Investing")
to_json_file("../files",ob1)
ob2 = FormattedCodeInterface()
ob2.set_content("Investing For Dummies, 4th Edition")
to_json_file("../files",ob2)
ob3 = FormattedCodeInterface()
ob3.set_content("The Little Book of Common Sense Investing: The Only Way to Guarantee Your Fair Share of Stock Market Returns")
to_json_file("../files",ob3)
ob4 = FormattedCodeInterface()
ob4.set_content("The Little Book of Value Investing")
to_json_file("../files",ob4)
ob5 = FormattedCodeInterface()
ob5.set_content("Value Investing: From Graham to Buffett and Beyond")
to_json_file("../files",ob5)
ob6 = FormattedCodeInterface()
ob6.set_content("Rich Dad's Guide to Investing: What the Rich Invest in, That the Poor and the Middle Class Do Not!")
to_json_file("../files",ob6)
ob7 = FormattedCodeInterface()
ob7.set_content("Investing in Real Estate, 5th Edition")
to_json_file("../files",ob7)
ob8 = FormattedCodeInterface()
ob8.set_content("Stock Investing For Dummies")
to_json_file("../files",ob8)
ob9 = FormattedCodeInterface()
ob9.set_content("Rich Dad's Advisors: The ABC's of Real Estate Investing: The Secrets of Finding Hidden Profits Most Investors Miss")
to_json_file("../files",ob9)

