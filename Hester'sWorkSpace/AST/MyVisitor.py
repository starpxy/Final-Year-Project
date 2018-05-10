import ast
class MyVisitor(ast.NodeTransformer):
    def generic_visit(self, node):
        ast.NodeTransformer.generic_visit(self, node)
        return node

    def visit_Str(self, node):
        return node

    def visit_Name(self, node):
        if node.id!='print': #ignore identity names
            node.id=''
            ast.NodeTransformer.generic_visit(self, node)
        else:
            node=None
            return None
        return node

    def visit_alias(self, node):
        node.asname=''
        ast.NodeTransformer.generic_visit(self, node)
        return node

    def visit_Expr(self, node):#remove print
        if isinstance(node.value, ast.Call):
            if isinstance(node.value.func,ast.Name):
                if node.value.func.id=='print':
                    return None
        ast.NodeTransformer.generic_visit(self, node)
        return node
        #         else:
        #             print('1')
        #             ast.NodeVisitor.generic_visit(self, node)
        #     else:
        #         print('2')
        #         ast.NodeVisitor.generic_visit(self, node)
        # else:
        #     print('3')
        #     ast.NodeVisitor.generic_visit(self, node)

    def visit_ClassDef(self,node):
        if hasattr(node,'name'):
            node.name=''
        ast.NodeTransformer.generic_visit(self, node)
        return node

    def visit_FunctionDef(self,node):
        if hasattr(node,'name'):
            # print(node)
            node.name=''
        if hasattr(node,'args'):
            node.args=''
        ast.NodeTransformer.generic_visit(self, node)
        return node


