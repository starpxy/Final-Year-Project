from AST import ASTSearching as asts
import ast
import hashlib
from AST import MyVisitor as mv

q=open("/Users/hester/Desktop/Final-Year-Project/Hester'sWorkSpace/AST/Testcases/q", 'r').read()#combine multiple programs
q1=open("/Users/hester/Desktop/Final-Year-Project/Hester'sWorkSpace/AST/Testcases/q1",'r').read()#copy one program

# print(astSearch.compareQueries(query1,query2))

astSearch=asts.ASTSearching()
# astSearch.import_in("/Users/hester/Desktop/Final-Year-Project/Hester'sWorkSpace/files/1b1bf356cb26e4b5674b613969b56e49.json")
# astSearch.ReadFiles()
astSearch.getResults(q,9)
# astSearch.search(str(q1))
