import ast
class MyVisitor(ast.NodeVisitor):
    def generic_visit(self, node):
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Str(self, node):
        node=None

    def visit_Name(self, node):
        if node.id!='print': #ignore identity names
            node.id=''
        else:
            node=None
            return None
        ast.NodeVisitor.generic_visit(self, node)

    def visit_alias(self, node):
        node.asname=''
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Expr(self, node):#remove print
        if isinstance(node.value, ast.Call):
            if isinstance(node.value.func,ast.Name):
                if node.value.func.id=='print':
                    node=None
                    return None
        ast.NodeVisitor.generic_visit(self, node)

    def visit_ClassDef(self,node):
        if hasattr(node,'name'):
            node.name=''
        ast.NodeVisitor.generic_visit(self, node)

    def visit_FunctionDef(self,node):
        if hasattr(node,'name'):
            # print(node)
            node.name=''
        ast.NodeVisitor.generic_visit(self, node)


