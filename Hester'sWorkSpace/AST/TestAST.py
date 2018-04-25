from AST import ASTSearching as asts
import time
q=open("/Users/hester/Desktop/Final-Year-Project/Hester'sWorkSpace/AST/Testcases/q", 'r').read()#combine multiple programs
q1=open("/Users/hester/Desktop/Final-Year-Project/Hester'sWorkSpace/AST/Testcases/q1",'r').read()#copy one program

# print(astSearch.compareQueries(query1,query2))
time_start = time.clock()
astSearch=asts.ASTSearching()
time_end = time.clock()
print("ini: ")
print(time_end-time_start)


time_start = time.clock()
result=astSearch.getResults(q,1)
time_end = time.clock()
print("whole: ")
print(time_end-time_start)
result.toString()


# astSearch.import_in("/Users/hester/Desktop/Final-Year-Project/Hester'sWorkSpace/files/1b1bf356cb26e4b5674b613969b56e49.json")
