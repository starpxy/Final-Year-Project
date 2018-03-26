import redis
from Interfaces import LogWriter as lg
import os
import ast
from Interfaces import FCIConverter as conv
from Interfaces import LogWriter as lg
from AST import MyVisitor as mv
import pickle

class ASTSearching:
    r = redis.Redis(host='localhost', port=6379,decode_responses=True)  # host是redis主机，需要redis服务端和客户端都启动 redis默认端口是6379
    lw = lg.LogWriter()
    path = "/Users/hester/Desktop/Final-Year-Project/Hester'sWorkSpace/files"  # path name
    files = []
    documents = {}
    code=[]
    astTrees={}
    hashTrees={}#{(weight, fileName): {nested dictionaries with hash values in stand of nodes} }
    visitor = mv.MyVisitor()
    weights={}#{weight:[fileNames] }
    lineNums={}
    # these parameters should be tuned
    matchingThreshold=80
    weightThreshold=5 #
    def __init__(self):
        pass

    #parse the corpus
    def ReadFiles(self):
        self.lw.write_info_log("reading files...")
        self.files = os.listdir(self.path)  # get all the file names
        self.files.remove('.DS_Store')
        for file in self.files:  # go through the folder
            if not os.path.isdir(file):  # judge if it is a folder
                self.documents[file] = conv.to_dic(self.path + "/" + file)
                root=ast.parse(self.documents[file]['code'])
                #remove strings and variable names
                self.visitor.visit(root)
                tree=ast.dump(root)
                self.astTrees[file]=tree
                hTree={}
                # self.lineNums[file]={}
                self.hashTree(file,root,hTree)
                self.hashTrees[file] =hTree
        self.lw.write_info_log("get " + str(len(self.documents)) + " documents")
        # use pickle module to save data into file 'CodexIndexAST.pik'
        with open('CodexIndexAST.pik', 'wb')as f:
            pickle.dump(self.weights, f, True)
            pickle.dump(self.hashTrees, f, True)

    #compare if two queries are the same using hash functions
    def compareQueries(self, query1, query2):
        h1=self.nodeToHash(query1)
        h2 = self.nodeToHash(query2)
        return h1==h2

    #parse a query
    def nodeToHash(self, node):
        qRoot = ast.parse(node)
        self.visitor.visit(qRoot)
        qt = ast.dump(qRoot)
        h=hash(qt)
        return h


    #work out the hash values and weights of every node in the corpus
    def hashTree(self,fileName, node, tree):
        nodeStr=hash(ast.dump(node))
        tree[nodeStr] = {}
        weight=1
        # startLine=getattr(node, "lineno", "None")
        i=0
        # endLine = startLine
        for n in ast.iter_child_nodes(node):
            i+=1
            weight+=self.hashTree(fileName, n, tree[nodeStr])
            # l = self.lineNums[fileName][hash(n)][1]
            # if l > endLine:
            #     endLine = l
        # self.lineNums[fileName][nodeStr]=(startLine,endLine)
        if i==0:
            tree[nodeStr]=None
        #if weight of this node is bigger than 4, store it into weights
        if weight>=self.weightThreshold:
            tree[(weight,nodeStr)]=tree.pop(nodeStr)
            if weight in self.weights:
                self.weights[weight].append(fileName)
            else:
                    self.weights[weight]=[fileName]
        return weight


    #break the query tree into nodes and calculate their weights
    def queryWeight(self, qNode, tree):
        weight=1
        qStr=hash(ast.dump(qNode))
        tree[qStr]={}
        i=0
        for n in ast.iter_child_nodes(qNode):
            i+=1
            weight+=self.queryWeight(n,tree[qStr])
        if i==0:
            tree[qStr]=None
        if weight>=self.weightThreshold:
            tree[(weight,qStr)]=tree.pop(qStr)
        return weight

    #search plagiarism code with query
    def search(self, query):
        if os.path.exists("CodexIndexAST.pik"):
            rfile = open('CodexIndexAST.pik', 'rb')
            self.weights = pickle.load(rfile)
            self.hashTrees=pickle.load(rfile)
        qTree={}
        qNode=ast.parse(query)
        self.visitor.visit(qNode)
        self.queryWeight(qNode,qTree)
        print("qTree:  ",end='')
        print(qTree)
        maxWeight=list(qTree.keys())[0][0]
        similarities={}
        self.similarities(qTree,self.hashTrees,self.weights,similarities,None)
        sorteKeys=sorted(similarities,key=similarities.get,reverse=True)
        print("similarities")
        for k in sorteKeys:
            if similarities[k]>self.matchingThreshold:
                print('match!: ',end='')
            print(str(k)+": "+str(similarities[k]))


    # calculate the similarities between corpus and query
    def similarities(self,qTree, hashTrees, weights,similarities,maxWeight):
        if maxWeight is None:
            maxWeight=1
        for w in qTree:
            if isinstance(w,tuple):
                find=False
                if w[0] in list(weights.keys()):
                    for file in weights[w[0]]:
                        v=self.dict_get(hashTrees[file],w,None)
                        if v is not None:
                            find=True
                            if file in similarities:
                                similarities[file]+=w[0]/maxWeight
                            else:
                                similarities[file] =w[0]/maxWeight
                        #insertion punishment
                        # else:
                        #     if file in similarities:
                        #         similarities[file]-=w[0]/maxWeight
                        #     else:
                        #         similarities[file] = -w[0]/maxWeight
                if not find and len(qTree[w])>0:
                    self.similarities(qTree[w],hashTrees,weights,similarities,maxWeight)


    #find a key in a nested dictionary
    def dict_get(self, d, objkey, default):
        tmp = d

        for k, v in tmp.items():
            #if find the key, delete this node (avoid repeated searching)
            if k == objkey:
                return tmp.pop(k)
            else:
                if isinstance(v,dict):
                    ret = self.dict_get(v, objkey, default)
                    if ret is not default:
                        return ret
        return default




    def import_in(self,filename):
        q1 = open("/Users/hester/Desktop/Final-Year-Project/Hester'sWorkSpace/AST/q1", 'r').read()
        dic = conv.to_dic(file_name=filename)
        # print(dic['code'])
        return  self.compareQueries(dic['code'],q1)



