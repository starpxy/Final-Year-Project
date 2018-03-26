import ast
from AST import MyVisitor as mv

file = open("/Users/hester/Desktop/Final-Year-Project/Hester'sWorkSpace/AST/code.py", "r")
source = file.read()
root = ast.parse(source)
expre=ast.dump(root,include_attributes=True)
visitor=mv.MyVisitor()
for node in ast.iter_child_nodes(root):
    print(ast.dump(node, include_attributes=True))

visitor.visit(root)
for node in ast.iter_child_nodes(root):
    print(ast.dump(node, include_attributes=True))

#throw away print out and variable names
# def clean(expre):
def iterateNodes(r):
    for node in ast.walk(r):
        # if not isinstance(node, ast.NameConstant):
        if isinstance(node, ast.FunctionDef) or isinstance(node, ast.ClassDef) or isinstance(node, ast.Module):
            print(ast.get_docstring(node))
        #     # iterateNodes(node.code())
        #     print(node.__getattribute__('body'))
        # else:
            try:
                print(node.lineno, end=' ')
            except:
                print(" ")
            print(ast.dump(node))
