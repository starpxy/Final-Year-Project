from JavaAST import java_AST
#Main.java
q1=open("/Users/hester/Desktop/Final-Year-Project/Hester'sWorkSpace/JavaAST/testCases/combine_2/java1",'r').read()

q2=open("/Users/hester/Desktop/Final-Year-Project/Hester'sWorkSpace/JavaAST/testCases/combine_2/java2",'r').read()
combined1=open("/Users/hester/Desktop/Final-Year-Project/Hester'sWorkSpace/JavaAST/testCases/combine_2/combine2",'r').read()

c1=open("/Users/hester/Desktop/Final-Year-Project/Hester'sWorkSpace/JavaAST/testCases/identifer_name_change/java1",'r').read()

ast=java_AST.JavaAST()

ast.getResults(c1,1)

# ast.import_in('/Users/hester/Desktop/finalYearProject/JavaFiles/java3/aa9cff52fb04847c545236d776815d0e.json')