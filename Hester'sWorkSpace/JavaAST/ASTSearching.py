import javalang
q1=open("/Users/hester/Desktop/Final-Year-Project/Hester'sWorkSpace/JavaAST/testCases/java1",'r').read()
tokens = list(javalang.tokenizer.tokenize(q1))
# for token in tokens:
#     print(token.value,end='  ')
#     print(token.position, end='   ')
#     print(token.__class__)

tree=javalang.parse.parse(q1)

# for path, node in tree:
#     print (path,end=' : ')
#     print(node, end=' : ')

structure=list(tree.__iter__())[:-1][:-1]
print(structure)
for tuple in structure:
    print(tuple)