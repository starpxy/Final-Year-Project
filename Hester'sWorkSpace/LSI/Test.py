import parser
import os
files= os.listdir("../files")

st=parser.suite(files[1])
print(parser.st2list(st, line_info=False, col_info=False))