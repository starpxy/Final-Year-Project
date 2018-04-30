from pycparser import c_parser
from CAST import ConstantVisitor as visitor
q1=open("/Users/hester/Desktop/Final-Year-Project/Hester'sWorkSpace/CAST/testCases/c1",'r').read()
text = u"""
void func(x,y,z)
{
  x = y+z;
  z=y;
  return x;
}
"""
parser = c_parser.CParser()
ast = parser.parse(q1)
ast.show()
visit=visitor.ConstantVisitor()
visit.visit(ast)
print('---------------')
ast.show(offset=2)
#rewrite the AST
# assign=ast.ext[0].body.block_items[0]
# print(assign.rvalue.left.name)
# assign.rvalue.left.name='x'
# ast.show(offset=2)
