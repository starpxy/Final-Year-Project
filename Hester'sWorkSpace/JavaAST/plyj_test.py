from plyj import parser
import plyj.model as m
p=parser.Parser()
tree = p.parse_file("/Users/hester/Desktop/Final-Year-Project/Hester'sWorkSpace/JavaAST/testCases/java1")

for type_decl in tree.type_declarations:
    print(type_decl.name)
    if type_decl.extends is not None:
        print(' -> extending ' + type_decl.extends.name.value)
    if len(type_decl.implements) is not 0:
        print(' -> implementing ' + ', '.join([type.name.value for type in type_decl.implements]))

    print('fields:')
    for field_decl in [decl for decl in type_decl.body if type(decl) is m.FieldDeclaration]:
        for var_decl in field_decl.variable_declarators:
            if type(field_decl.type) is str:
                type_name = field_decl.type
            else:
                type_name = field_decl.type.name.value
            print('    ' + type_name + ' ' + var_decl.variable.name)

    print('methods:')
