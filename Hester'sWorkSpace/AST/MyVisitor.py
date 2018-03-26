import ast
class MyVisitor(ast.NodeTransformer):
    # def generic_visit(self,node):
    #     print('========')
    #     l=getattr(node, "lineno", "-1")
    #     print(l)
    #     if l =='-1':
    #         print('000000000')
    #         ast.fix_missing_locations(node)
    #     print(getattr(node, "lineno", "None"))

    def visit_Str(self, node):
        return None

    def visit_Name(self, node):
        if node.id!='print': #ignore identity names
            node.id=''
        return node

    def visit_alias(self, node):
        node.asname=''
        return node

    def visit_Expr(self, node):#remove print
        if node.value.func=="Name(id='print', ctx=Load())":
            return None


