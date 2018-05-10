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

#modify identifier names
modify3=open("/Users/hester/Desktop/Final-Year-Project/Hester'sWorkSpace/AST/Testcases/identifier_name_modify/modify_1", 'r').read()
p3=open("/Users/hester/Desktop/Final-Year-Project/Hester'sWorkSpace/AST/Testcases/identifier_name_modify/python1", 'r').read()

modify4=open("/Users/hester/Desktop/Final-Year-Project/Hester'sWorkSpace/AST/Testcases/identifier_name_modify/modify_2", 'r').read()
p4=open("/Users/hester/Desktop/Final-Year-Project/Hester'sWorkSpace/AST/Testcases/identifier_name_modify/python2", 'r').read()

#output insertion testcases
modify5=open("/Users/hester/Desktop/Final-Year-Project/Hester'sWorkSpace/AST/Testcases/output_insertion/modify_1", 'r').read()
p5=open("/Users/hester/Desktop/Final-Year-Project/Hester'sWorkSpace/AST/Testcases/output_insertion/python1", 'r').read()

modify6=open("/Users/hester/Desktop/Final-Year-Project/Hester'sWorkSpace/AST/Testcases/output_insertion/modify_2", 'r').read()
p6=open("/Users/hester/Desktop/Final-Year-Project/Hester'sWorkSpace/AST/Testcases/output_insertion/python2", 'r').read()

#mixed plagiarized techs test case
mix=open("/Users/hester/Desktop/Final-Year-Project/Hester'sWorkSpace/AST/Testcases/mixed/mixed_test", 'r').read()

p7=open("/Users/hester/Desktop/Final-Year-Project/Hester'sWorkSpace/AST/Testcases/mixed/python3", 'r').read()


# q1=open("/Users/hester/Desktop/Final-Year-Project/Hester'sWorkSpace/AST/Testcases/q1",'r').read()#copy one program

# time_start = time.clock()

astSearch=asts.ASTSearching()

# time_end = time.clock()
# print("ini: ")
# print(time_end-time_start)


# time_start = time.clock()

result=astSearch.getResults(mix,1)

# time_end = time.clock()
# print("whole: ")
# print(time_end-time_start)



# astSearch.import_in("/Users/hester/Desktop/finalYearProject/files/07273cf3c2d15f70be016fe0cbc101b4.json")
