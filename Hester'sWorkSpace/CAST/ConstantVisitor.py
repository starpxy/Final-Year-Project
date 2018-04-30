from pycparser.c_ast import NodeVisitor

class ConstantVisitor(NodeVisitor):

    def visit_Constant(self, node):
        self.values=0

    def visit_EmptyStatement(self):
        node=''

    def visit_ID(self,node):
        print('.....')
        node.name=''

    # def generic_visit(self, node):
    #     try:
    #         self.ID=''
    #     except:
    #         print('======')
