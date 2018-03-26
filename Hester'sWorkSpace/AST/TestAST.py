from AST import ASTSearching as asts
import ast
astSearch=asts.ASTSearching()
astSearch.ReadFiles()
query1=open("/Users/hester/Desktop/Final-Year-Project/Hester'sWorkSpace/AST/query",'r').read()
query2=open("/Users/hester/Desktop/Final-Year-Project/Hester'sWorkSpace/AST/query2", 'r').read()
q=open("/Users/hester/Desktop/Final-Year-Project/Hester'sWorkSpace/AST/q", 'r').read()
q1=open("/Users/hester/Desktop/Final-Year-Project/Hester'sWorkSpace/AST/q1",'r').read()
# print(astSearch.compareQueries(query1,query2))
# print(astSearch.import_in("/Users/hester/Desktop/Final-Year-Project/Hester'sWorkSpace/files/0a0d18ea967e5bf27172f06facb75be3.json"))
astSearch.search(q)