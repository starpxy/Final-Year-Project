from __future__ import print_function
import argparse
import sys
from pycparser import c_parser, c_ast, parse_file

q1=open("/Users/hester/Desktop/Final-Year-Project/Hester'sWorkSpace/CAST/testCases/c1",'r').read()
sys.path.extend(['.', '..'])

if __name__ == "__main__":
    argparser = argparse.ArgumentParser('Dump AST')
    argparser.add_argument('filename', help='name of file to parse')
    args = argparser.parse_args()

    ast = parse_file(args.filename, use_cpp=False)
    ast.show()
    #pycparser/c_parser.py