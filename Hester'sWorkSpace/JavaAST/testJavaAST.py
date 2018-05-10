from JavaAST import java_AST

q2=open("/Users/hester/Desktop/Final-Year-Project/Hester'sWorkSpace/JavaAST/testCases/combine_2/java2",'r').read()
combined1=open("/Users/hester/Desktop/Final-Year-Project/Hester'sWorkSpace/JavaAST/testCases/combine_2/combine2",'r').read()

#change identifier name test cases
c1=open("/Users/hester/Desktop/Final-Year-Project/Hester'sWorkSpace/JavaAST/testCases/identifer_name_change/java1",'r').read()
modify_1=open("/Users/hester/Desktop/Final-Year-Project/Hester'sWorkSpace/JavaAST/testCases/identifer_name_change/modify_1",'r').read()

c2=open("/Users/hester/Desktop/Final-Year-Project/Hester'sWorkSpace/JavaAST/testCases/identifer_name_change/java2",'r').read()
modify_2=open("/Users/hester/Desktop/Final-Year-Project/Hester'sWorkSpace/JavaAST/testCases/identifer_name_change/modify_2",'r').read()

#change code order tast cases
d1=open("/Users/hester/Desktop/Final-Year-Project/Hester'sWorkSpace/JavaAST/testCases/change_order/java1",'r').read()
modify_3=open("/Users/hester/Desktop/Final-Year-Project/Hester'sWorkSpace/JavaAST/testCases/change_order/modify_1",'r').read()

d2=open("/Users/hester/Desktop/Final-Year-Project/Hester'sWorkSpace/JavaAST/testCases/change_order/java2",'r').read()
modify_4=open("/Users/hester/Desktop/Final-Year-Project/Hester'sWorkSpace/JavaAST/testCases/change_order/modify_2",'r').read()

#output insertion test cases
e1=open("/Users/hester/Desktop/Final-Year-Project/Hester'sWorkSpace/JavaAST/testCases/output_insertion/java1",'r').read()
modify_5=open("/Users/hester/Desktop/Final-Year-Project/Hester'sWorkSpace/JavaAST/testCases/output_insertion/modify_1",'r').read()

e2=open("/Users/hester/Desktop/Final-Year-Project/Hester'sWorkSpace/JavaAST/testCases/output_insertion/java2",'r').read()
modify_6=open("/Users/hester/Desktop/Final-Year-Project/Hester'sWorkSpace/JavaAST/testCases/output_insertion/modify_2",'r').read()

#mixed test case
f1=open("/Users/hester/Desktop/Final-Year-Project/Hester'sWorkSpace/JavaAST/testCases/mixed/java1",'r').read()
f2=open("/Users/hester/Desktop/Final-Year-Project/Hester'sWorkSpace/JavaAST/testCases/mixed/java2",'r').read()
f3=open("/Users/hester/Desktop/Final-Year-Project/Hester'sWorkSpace/JavaAST/testCases/mixed/java3",'r').read()
modify_7=open("/Users/hester/Desktop/Final-Year-Project/Hester'sWorkSpace/JavaAST/testCases/mixed/mixed_1",'r').read()



ast=java_AST.JavaAST()
ast.getResults(modify_7,1)


# ast.import_in('/Users/hester/Desktop/finalYearProject/JavaFiles/java3/adf88a3e3c4bb07398ae9de744e1f5bc.json')