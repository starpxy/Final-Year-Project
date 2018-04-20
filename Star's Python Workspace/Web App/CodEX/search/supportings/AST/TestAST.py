from search.supportings.AST import ASTSearching as asts

# astSearch=asts.ASTSearching()
# astSearch.ReadFiles()

q=open("Testcases/q", 'r').read()#combine multiple programs
astSearch=asts.ASTSearching()
astSearch.getResults(q,1)