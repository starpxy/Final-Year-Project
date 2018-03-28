import redis
from Interfaces import LogWriter as lg
import os
import ast
from Interfaces import FCIConverter as conv
from Interfaces import LogWriter as lg
from AST import MyVisitor as mv
import pickle
import hashlib
from AST import Results

class ASTSearching:
    r = redis.Redis(host='localhost', port=6379,decode_responses=True)  # host是redis主机，需要redis服务端和客户端都启动 redis默认端口是6379
    lw = lg.LogWriter()
    path = "/Users/hester/Desktop/Final-Year-Project/Hester'sWorkSpace/files"  # path name
    files = []
    documents = {}
    hashTrees={}#{fileName: {nodeHash: {nested dictionaries with hash values in stand of nodes} } }
    visitor = mv.MyVisitor()
    weights={}#{weight:[fileNames] }
    lineNums={}#{fileName: {nodeHash: (startLine, endLine)}}
    # these parameters should be tuned
    matchingThreshold=0.6
    weightThreshold=10 #
    pageNum=10
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
                try:
                    root=ast.parse(str(self.documents[file]['code']))
                except(SyntaxError):
                    self.lw.write_error_log("syntax error! " + file)
                    continue
                #remove strings and variable names
                self.visitor.visit(root)
                hTree={}
                self.lineNums[file]={}
                self.Indexing(root, self.lineNums[file], self.weights, file, hTree)
                self.hashTrees[file] =hTree

        self.lw.write_info_log("get " + str(len(self.documents)) + " documents")
        # use pickle module to save data into file 'CodexIndexAST.pik'
        with open('CodexIndexAST.pik', 'wb')as f:
            pickle.dump(self.weights, f, True)
            pickle.dump(self.hashTrees, f, True)
            pickle.dump(self.lineNums,f,True)

    #turn every document root into index
    def Indexing(self, node, lineNums, weights, fileName, hashTrees):
        weight = 1
        min = 0
        max = 0
        i = 0
        startLine = 0
        endLine = 0

        if isinstance(node, ast.AST):
            m = hashlib.md5()
            m.update(ast.dump(node).encode("utf8"))
            nodeStr = m.hexdigest()
            hashTrees[nodeStr] = {}
            for n, m in ast.iter_fields(node):
                tuple = self.Indexing(m, lineNums, weights, fileName, hashTrees[nodeStr])
                weight += tuple[0]
                if tuple[1] > 0:
                    startLine = tuple[1]
                    if i == 0:
                        min = startLine
                    elif startLine < min:
                        min = startLine
                    i += 1
                if tuple[2] > 0:
                    endLine = tuple[2]
                    if endLine > max:
                        max = endLine
                    i += 1
            if node._attributes:
                lineNo = getattr(node, 'lineno')
                if min == 0 and max == 0:
                    min = lineNo
                    max = lineNo
            if weight >= self.weightThreshold:
                if weight in weights:
                    if fileName not in weights[weight]:
                        weights[weight].append(fileName)
                else:
                    weights[weight] = [fileName]

                lineNums[nodeStr] = (min, max)
                if len(hashTrees[nodeStr]) == 0:
                    hashTrees[nodeStr] = None
            else:
                hashTrees.pop(nodeStr)

            return (weight, min, max)

        elif isinstance(node, list):
            for x in node:
                tuple = self.Indexing(x, lineNums, weights, fileName, hashTrees)
                weight += tuple[0]
                if tuple[1] > 0:
                    startLine = tuple[1]
                    if i == 0:
                        min = startLine
                    elif startLine < min:
                        min = startLine
                    i += 1
                if tuple[2] > 0:
                    endLine = tuple[2]
                    if endLine > max:
                        max = endLine
                    i += 1

            return (weight, min, max)
        return (weight, min, max)

    #interface to front end. Input query, return a Result instance
    def getResults(self,query,page):
        if not self.r.exists(query):  # if the result is not in the redis
            # store the result of the query into redis
            matchingLines = {}  # {fileName:[(qStart,qEnd, fStart,fEnd)]}
            similarities = self.search(query, matchingLines)
            keys=list(similarities.keys())
            for k in keys:
                if similarities[k] < self.matchingThreshold:
                    similarities.pop(k)
                    matchingLines.pop(k)
            sorteKeys = sorted(similarities, key=similarities.get, reverse=True)
            # print('------')
            # print(sorteKeys)
            if len(sorteKeys)==0:
                return Results.Results(0, [],{})
            self.lw.write_info_log("storing results into redis in form of list")
            self.r.rpush(query, sorteKeys)
            self.r.rpush(query,matchingLines)

        # get the result list of this query from redis
        else:
            self.lw.write_info_log("geting results from redis")
            sorteKeys=eval(self.r.lindex(query, 0))
            matchingLines=eval(self.r.lindex(query,1))

        self.r.expire(query, 30)  # expire after 30s
        if page * self.pageNum<len(sorteKeys):
            results=Results.Results(len(sorteKeys),sorteKeys[(page - 1) * self.pageNum : page * self.pageNum],matchingLines)
        else:
            results = Results.Results(len(sorteKeys), sorteKeys[(page - 1) * self.pageNum: ],matchingLines)

        print('==============')
        print(results.getDocumentList())
        # print("similarities")
        # for k in sorteKeys:
        #     print(str(k) + ": " + str(similarities[k]), end='  in:  ')
        #     print(matchingLines[k])
        return results





    #break the query tree into nodes and calculate their weights
    def queryWeight(self,node, lineNums, tree):
        weight = 1
        min = 0
        max = 0
        i = 0
        startLine = 0
        endLine = 0

        if isinstance(node, ast.AST):
            m = hashlib.md5()
            m.update(ast.dump(node).encode("utf8"))
            nodeStr = m.hexdigest()
            tree[nodeStr] = {}
            for n, m in ast.iter_fields(node):
                tuple = self.queryWeight(m, lineNums, tree[nodeStr])
                weight += tuple[0]
                if tuple[1] > 0:
                    startLine = tuple[1]
                    if i == 0:
                        min = startLine
                    elif startLine < min:
                        min = startLine
                    i += 1
                if tuple[2] > 0:
                    endLine = tuple[2]
                    if endLine > max:
                        max = endLine
                    i += 1
            if node._attributes:
                lineNo = getattr(node, 'lineno')
                if min == 0 and max == 0:
                    min = lineNo
                    max = lineNo
            if weight >= self.weightThreshold:
                # print('-----------')
                # print("weight= " + str(weight))
                # print(ast.dump(node, include_attributes=True))
                lineNums[nodeStr] = (min, max)
                # print(lineNums[nodeStr])
                tree[(weight, nodeStr)] = tree.pop(nodeStr)
                if len(tree[(weight, nodeStr)]) == 0:
                    tree[(weight, nodeStr)] = None
                # print(tree[(weight, nodeStr)])
            else:
                tree.pop(nodeStr)

            return (weight, min, max)

        elif isinstance(node, list):
            for x in node:
                tuple = self.queryWeight(x, lineNums, tree)
                weight += tuple[0]
                if tuple[1] > 0:
                    startLine = tuple[1]
                    if i == 0:
                        min = startLine
                    elif startLine < min:
                        min = startLine
                    i += 1
                if tuple[2] > 0:
                    endLine = tuple[2]
                    if endLine > max:
                        max = endLine
                    i += 1

            return (weight, min, max)
        return (weight, min, max)

    #search plagiarism code with query
    def search(self, query,matchingLines):
        if os.path.exists("CodexIndexAST.pik"):
            rfile = open('CodexIndexAST.pik', 'rb')
            self.weights = pickle.load(rfile)
            self.hashTrees=pickle.load(rfile)
            self.lineNums=pickle.load(rfile)

        qTree={}#{(weight,nodeHash):{nested dictionaries}}
        qLineNums={}#{nodeHash:(start,end)}
        qNode=ast.parse(query)
        self.visitor.visit(qNode)
        print(ast.dump(qNode, include_attributes=True))
        self.queryWeight(qNode,qLineNums,qTree)
        print("qTree:  ",end='')
        print(qTree)
        print(qLineNums)
        maxWeight=list(qTree.keys())[0][0]
        similarities={}#{fileName:score}
        self.similarities(qTree,self.hashTrees,self.weights,similarities,maxWeight,qLineNums,self.lineNums,matchingLines)
        return similarities


    # calculate the similarities between corpus and query
    def similarities(self,qTree, hashTrees, weights,similarities,maxWeight, qLineNums, lineNums,matchingLines):
        if maxWeight is None:
            maxWeight=1
        for w in qTree:
            if isinstance(w,tuple):
                find=False
                if w[0] in list(weights.keys()):
                    for file in weights[w[0]]:
                        v=self.dict_get(w[0], hashTrees[file],w[1],'Not Found', weights, file)
                        if v != 'Not Found':
                            find=True
                            qs=qLineNums[w[1]][0]
                            qe=qLineNums[w[1]][1]
                            fs=lineNums[file][w[1]][0]
                            fe=lineNums[file][w[1]][1]
                            if file in similarities:
                                matchingLines[file].append((qs,qe,fs,fe))
                                similarities[file]+=w[0]/maxWeight
                            else:
                                matchingLines[file]=[(qs,qe,fs,fe)]
                                similarities[file] =w[0]/maxWeight
                                #insertion punishment
                                # else:
                                #     if file in similarities:
                                #         similarities[file]-=w[0]/maxWeight
                                #     else:
                                #         similarities[file] = -w[0]/maxWeight
                if not find and qTree[w] is not None:
                    if len(qTree[w])>0:
                        self.similarities(qTree[w],hashTrees,weights,similarities,maxWeight,qLineNums, lineNums,matchingLines)


    #find a key in a nested dictionary
    def dict_get(self,weight, d, objkey, default, weights,fileName):
        for k, v in d.items():
            #if find the key, delete this node (avoid repeated searching)
            if k == objkey:
                # weights[weight].remove(fileName)
                return d.pop(k)
            else:
                if isinstance(v,dict):
                    # if  k[0]>objkey[0]:
                    ret = self.dict_get(weight,v, objkey, default, weights,fileName)
                    if ret is not default:
                        return ret
        return default




    def import_in(self,filename):
        q1 = open("/Users/hester/Desktop/Final-Year-Project/Hester'sWorkSpace/AST/q1", 'r').read()
        dic = conv.to_dic(file_name=filename)
        print(dic['code'])
        # return  self.compareQueries(dic['code'],q1)


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
            m = hashlib.md5()
            m.update(qt.encode("utf8"))
            h = m.hexdigest()
            return h



