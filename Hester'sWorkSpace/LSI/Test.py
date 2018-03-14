import parser
import os
files= os.listdir("../files")

st=parser.suite("files/0a0d18ea967e5bf27172f06facb75be3.json")
print(parser.st2list(st, line_info=False, col_info=False))