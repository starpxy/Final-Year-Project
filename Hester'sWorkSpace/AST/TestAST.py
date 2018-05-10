from AST import ASTSearching as asts
import time
#combined test cases
combined1=open("/Users/hester/Desktop/Final-Year-Project/Hester'sWorkSpace/AST/Testcases/combined_1/combined1", 'r').read()#combine multiple programs
combined2=open("/Users/hester/Desktop/Final-Year-Project/Hester'sWorkSpace/AST/Testcases/combined_2/combine2", 'r').read()#combine multiple programs

#change ordert test cases

modify1=open("/Users/hester/Desktop/Final-Year-Project/Hester'sWorkSpace/AST/Testcases/change_order/modify_1", 'r').read()
p1=open("/Users/hester/Desktop/Final-Year-Project/Hester'sWorkSpace/AST/Testcases/change_order/python1", 'r').read()

modify2=open("/Users/hester/Desktop/Final-Year-Project/Hester'sWorkSpace/AST/Testcases/change_order/modify_2", 'r').read()
p2=open("/Users/hester/Desktop/Final-Year-Project/Hester'sWorkSpace/AST/Testcases/change_order/python2", 'r').read()

# q1=open("/Users/hester/Desktop/Final-Year-Project/Hester'sWorkSpace/AST/Testcases/q1",'r').read()#copy one program

# time_start = time.clock()

astSearch=asts.ASTSearching()

# time_end = time.clock()
# print("ini: ")
# print(time_end-time_start)


# time_start = time.clock()

result=astSearch.getResults(modify2,1)

# time_end = time.clock()
# print("whole: ")
# print(time_end-time_start)



# astSearch.import_in("/Users/hester/Desktop/finalYearProject/files/02fdc1f2367e925cfc7619e1d877b9e6.json")
