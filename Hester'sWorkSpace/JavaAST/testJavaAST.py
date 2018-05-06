from JavaAST import java_AST
#Main.java
q1=open("/Users/hester/Desktop/Final-Year-Project/Hester'sWorkSpace/JavaAST/testCases/java1",'r').read()

q2=open("/Users/hester/Desktop/Final-Year-Project/Hester'sWorkSpace/JavaAST/testCases/java2",'r').read()
combined1=open("/Users/hester/Desktop/Final-Year-Project/Hester'sWorkSpace/JavaAST/testCases/combined1",'r').read()

ast=java_AST.JavaAST()
ast.getResults(combined1,1)