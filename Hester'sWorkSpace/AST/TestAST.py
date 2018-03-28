from AST import ASTSearching as asts
import ast
import hashlib
from AST import MyVisitor as mv

q=open("/Users/hester/Desktop/Final-Year-Project/Hester'sWorkSpace/AST/q", 'r').read()
q1=open("/Users/hester/Desktop/Final-Year-Project/Hester'sWorkSpace/AST/q1",'r').read()

# print(astSearch.compareQueries(query1,query2))

astSearch=asts.ASTSearching()
# astSearch.import_in("/Users/hester/Desktop/Final-Year-Project/Hester'sWorkSpace/files/25408d35aed107a4c9321ddb89ef64d6.json")
# astSearch.ReadFiles()
astSearch.getResults(q1,1)
# astSearch.search(str(q1))

# hashTrees={}#{fileName: {nodeHash: {nested dictionaries with hash values in stand of nodes} } }
# weights={}#{weight:[fileNames] }
# lineNums={}#{(fileName, nodeHash): (startLine, endLine)}


def _format1(node, lineNums, weights, fileName,hashTrees):
    weight=1
    min = 0
    max = 0
    i = 0
    startLine = 0
    endLine = 0

    if isinstance(node, ast.AST):
        m = hashlib.md5()
        m.update(ast.dump(node).encode("utf8"))
        nodeStr = m.hexdigest()
        hashTrees[nodeStr]={}
        for n, m in ast.iter_fields(node):
            tuple = _format1(m, lineNums, weights, fileName, hashTrees[nodeStr])
            weight += tuple[0]
            if tuple[1] >0:
                startLine = tuple[1]
                if i == 0:
                    min = startLine
                elif startLine < min:
                    min = startLine
                i += 1
            if tuple[2] >0:
                endLine = tuple[2]
                if endLine > max:
                    max = endLine
                i += 1
        if node._attributes:
            lineNo = getattr(node, 'lineno')
            if min == 0 and max == 0:
                min = lineNo
                max = lineNo
        if weight>=5:
            print('-----------')
            print("weight= "+str(weight))
            if weight in weights:
                if fileName not in weights[weight]:
                    weights[weight].append(fileName)
            else:
                weights[weight]=[fileName]

            print(ast.dump(node, include_attributes=True))
            lineNums[nodeStr] = (min, max)
            print(lineNums[ nodeStr])
            if len(hashTrees[nodeStr])==0:
                hashTrees[nodeStr]=None
            print(hashTrees[nodeStr])
        else:
            hashTrees.pop(nodeStr)


        return (weight, min,max)

    elif isinstance(node, list):
        for x in node:
            tuple=_format1(x,lineNums, weights,fileName,hashTrees)
            weight+=tuple[0]
            if tuple[1] >0:
                startLine = tuple[1]
                if i == 0:
                    min = startLine
                elif startLine < min:
                    min = startLine
                i += 1
            if tuple[2] >0:
                endLine = tuple[2]
                if endLine > max:
                    max = endLine
                i += 1


        return (weight, min, max)
    return (weight, min, max )





# visitor = mv.MyVisitor()
# qNode=ast.parse(q1)
# print(ast.dump(qNode,include_attributes=True))
# visitor.visit(qNode)
# print(ast.dump(qNode,include_attributes=True))
# print(ast.dump(qNode, include_attributes=True))
# print(ast.dump(qNode,annotate_fields=False, include_attributes=True))
# lineNums={}
# weights={}
# # _format1(qNode,lineNums,weights, 'test',hashTrees)
# queryWeight(qNode,lineNums,hashTrees)
# print('\n\n')
# print(hashTrees)
# print(lineNums)



# #work out the hash values and weights of every node in the corpus
    # def hashTree(self,fileName, node, tree):
    #     m = hashlib.md5()
    #     m.update(ast.dump(node).encode("utf8"))
    #     nodeStr = m.hexdigest()
    #
    #     startLine=getattr(node, "lineno", 1)
    #     print(startLine)
    #     self.lineNums[(fileName,nodeStr)]=startLine
    #     tree[nodeStr] = {}
    #     weight=1
    #     # if startLine ==-1:
    #     #     startLine=1
    #     i=0
    #     # endLine = startLine
    #     for n in ast.iter_child_nodes(node):
    #         i+=1
    #         weight+=self.hashTree(fileName, n, tree[nodeStr])
    #         # l = self.lineNums[fileName][hash(n)][1]
    #         # if l > endLine:
    #         #     endLine = l
    #     # self.lineNums[fileName][nodeStr]=(startLine,endLine)
    #     if i==0:
    #         tree[nodeStr]=None
    #     #if weight of this node is bigger than 4, store it into weights
    #     if weight>=self.weightThreshold:
    #         tree[(weight,nodeStr)]=tree.pop(nodeStr)
    #         if weight in self.weights:
    #             if fileName not in self.weights[weight]:
    #                 self.weights[weight].append(fileName)
    #         else:
    #                 self.weights[weight]=[fileName]
    #     return weight


