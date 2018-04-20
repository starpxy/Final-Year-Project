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
    path = "/Users/hester/Desktop/finalYearProject/files"  # path name
    files = []
    documents = {}
    hashTrees={}#{fileName: {nodeHash: {nested dictionaries with hash values in stand of nodes} } }
    visitor = mv.MyVisitor()
    weights={}#{weight:[fileNames] }
    lineNums={}#{fileName: {nodeHash: (startLine, endLine)}}
    # these parameters should be tuned
    matchingThreshold=0.6
    weightThreshold=10 #weight outweigh weightThreshold will be taken into consideration
    blockThreshold=50 #weight outweigh the blockthreshold means this node will be a code block which should be included into the global searching
    pageNum=10
    wholeSimilarity=0
    matchingBlock={} # {docID: (the startline and endline of the matching blocks)}.
    blockWeights={} #{docID: (startline, endline): weight of the biggest matching block}
    def __init__(self):
        pass

    #parse the corpus
    def ReadFiles(self):
        self.lw.write_info_log("reading files...")
        self.files = os.listdir(self.path)  # get all the file names
        # self.files.remove('.DS_Store')
        for file in self.files:  # go through the folder
            if not os.path.isdir(file):  # judge if it is a folder
                self.documents[file] = conv.to_dic(self.path + "/" + file)
                try:
                    root=ast.parse(str(self.documents[file]['content']))
                except(SyntaxError):
                    self.lw.write_error_log("syntax error! " + file)
                    # self.documents[file].close()
                    continue
                #remove strings and variable names
                self.visitor.visit(root)
                hTree={}
                self.lineNums[file]={}
                self.Indexing(root, self.lineNums[file], self.weights, file, hTree)
                self.hashTrees[file] =hTree
                # self.documents[file].close()

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
        globalSimilarity=0
        matchingBlocks={}
        componentDocuments=[]
        if not self.r.exists(query):  # if the result is not in the redis
            # store the result of the query into redis
            matchingLines = {}  # {fileName:[(qStart,qEnd, fStart,fEnd)]}
            similarities = self.search(query, matchingLines)
            globalSimilarity=self.wholeSimilarity
            matchingBlocks=self.matchingBlock
            documentList=sorted(similarities,key=similarities.get,reverse=True)
            if similarities==None:
                self.lw.write_error_log('Pickle files not found!')
                return None
            elif similarities==0:
                return 0
            #get the normal relevant documents and the suspected plagiarized documents
            plagiarismList=[]
            i=0
            for d in documentList:
                if similarities[d]>self.matchingThreshold:
                    plagiarismList.append(similarities[d])
                    i+=1
                else:
                    break
            documentList=documentList[i: ]
            componentDocuments=list(matchingBlocks.keys())
            #store data into the redis server
            self.lw.write_info_log("storing results into redis in form of list")
            self.r.rpush(query, plagiarismList)
            self.r.rpush(query, documentList)
            self.r.rpush(query, matchingLines)
            if globalSimilarity!=0 and len(matchingBlocks)!=0:
                if len(plagiarismList)>0:
                    if globalSimilarity>=similarities[plagiarismList[0]]and globalSimilarity>=self.matchingThreshold:
                        self.r.rpush(query, globalSimilarity)
                        self.r.rpush(query, matchingBlocks)
                        self.r.rpush(query,componentDocuments)
                else:
                    self.r.rpush(query, globalSimilarity)
                    self.r.rpush(query, matchingBlocks)
                    self.r.rpush(query, componentDocuments)

        # get the result list of this query from redis
        else:
            self.lw.write_info_log("geting results from redis")
            plagiarismList=eval(self.r.lindex(query, 0))
            documentList=eval(self.r.lindex(query,1))
            matchingLines=eval(self.r.lindex(query,2))
            if self.r.llen(query)>=6:
                globalSimilarity=eval(self.r.lindex(query,3))
                matchingBlocks=eval(self.r.lindex(query,4))
                componentDocuments=eval(self.r.lindex(query,5))

        self.r.expire(query, 30)  # expire after 30s

        #encalsulate results into the object:Result
        documentListLength=len(documentList)
        plagiarismListLength=len(plagiarismList)
        matchingblocksLength=len(componentDocuments)
        length=documentListLength+plagiarismListLength+matchingblocksLength
        results=Results.Results(numOfResults=length,matchingLines=matchingLines,globalSimilarity=globalSimilarity,matchingBlocks=matchingBlocks)
        results.setNumOfResult(length)
        disMatchingBlocks=[]
        disPlagiarismList=[]
        disDocumentList=[]
        if (page-1)*self.pageNum<matchingblocksLength: #need to display the maching blocks
            disMatchingBlocks=componentDocuments[(page-1)*self.pageNum : min(page * self.pageNum,matchingblocksLength)]
            results.setComponentDocuments(disMatchingBlocks)

        if (page-1)*self.pageNum<matchingblocksLength+plagiarismListLength and page*self.pageNum>=matchingblocksLength:
            # need to display the plagiarism documents
            if len(disMatchingBlocks)==0 and page>1:#not start from 0
                disPlagiarismList= plagiarismList[(page-1)*self.pageNum - matchingblocksLength: min((page * self.pageNum - matchingblocksLength), plagiarismListLength)]
            else: #start from 0
                disPlagiarismList = plagiarismList[0 : min(self.pageNum, plagiarismListLength)]
            results.setPlagiarismList(disPlagiarismList)

        if page*self.pageNum > matchingblocksLength+plagiarismListLength:#need to dispaly the relevant documents
            if len(disMatchingBlocks)==0 and len(disPlagiarismList)==0 and (page-1)*self.pageNum<=length: #not start from 0
                disDocumentList=documentList[(page-1)*self.pageNum-matchingblocksLength-plagiarismListLength: min((page*self.pageNum-matchingblocksLength-plagiarismListLength),documentListLength)]
            elif (page-1)*self.pageNum<=length: #start from 0
                disDocumentList = documentList[0: min((self.pageNum-matchingblocksLength-plagiarismListLength),documentListLength)]
            else:
                self.lw.write_error_log("page number out of range")
                return None
            results.setDocumentList(disDocumentList)

        print('==============')
        results.toString()
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
                lineNums[nodeStr] = (min, max)
                tree[(weight, nodeStr)] = tree.pop(nodeStr)
                if len(tree[(weight, nodeStr)]) == 0:
                    tree[(weight, nodeStr)] = None
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
        # refresh the global variables
        self.wholeSimilarity = 0
        self.matchingBlock = {}
        self.blockWeights={}

        if os.path.exists("CodexIndexAST.pik"):
            rfile = open('CodexIndexAST.pik', 'rb')
            self.weights = pickle.load(rfile)
            self.hashTrees=pickle.load(rfile)
            self.lineNums=pickle.load(rfile)
        else:
            return None

        qTree={}#{(weight,nodeHash):{nested dictionaries}}
        qLineNums={}#{nodeHash:(start,end)}
        try:
            qNode=ast.parse(query)
        except(SyntaxError):
            self.lw.write_error_log("syntax error in qeury! " )
            return 0
        self.visitor.visit(qNode)
        print(ast.dump(qNode, include_attributes=True))
        self.queryWeight(qNode,qLineNums,qTree)
        print("qTree:  ",end='')
        print(qTree)
        print(qLineNums)
        maxWeight=list(qTree.keys())[0][0]
        similarities={}#{fileName:score}
        self.similarities(qTree,self.hashTrees,self.weights,similarities,maxWeight,qLineNums,self.lineNums,matchingLines)

        #work out the global similarity
        for dic in self.blockWeights:
            biggestKey=sorted(self.blockWeights[dic],key=self.blockWeights[dic].get,reverse=True)[0]
            if self.blockWeights[dic][biggestKey] >self.blockThreshold:
                ds=list(self.matchingBlock.keys())
                store=True
                for d in ds:
                    block=self.matchingBlock[d]
                    #do not store in if the new block is included in some block within the matchBlock
                    if biggestKey[0]>=block[0]  and biggestKey[1]<=block[1]:
                        store=False
                        break
                    #delete the older block included in the new block
                    elif biggestKey[0]<=block[0]  and biggestKey[1]>=block[1]:
                        self.matchingBlock.pop(d)
                        self.wholeSimilarity -= self.blockWeights[d][block] / maxWeight

                    #deal with the block that have some part overlapping with old blocks (store the one with bigger weight)
                    elif (biggestKey[0] <= block[1] and biggestKey[0]>=block[0]) or (biggestKey[1] <= block[1] and biggestKey[1]>=block[0]):
                        if self.blockWeights[dic][biggestKey]> self.blockWeights[d][block]:
                            self.matchingBlock.pop(d)
                            self.wholeSimilarity -= self.blockWeights[d][block] / maxWeight
                        else:
                            store = False
                            break

                # store the new block
                if store:
                    self.matchingBlock[dic]=biggestKey
                    self.wholeSimilarity+=self.blockWeights[dic][biggestKey]/maxWeight

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

                            # merge lines in query program to construct the code blocks
                            forwMerge = False
                            BackMerge = False
                            if file not in self.blockWeights:
                                self.blockWeights[file] = {}
                            elif (qs, qe) in self.blockWeights[file]:
                                if w[0]>self.blockWeights[file][(qs, qe)]:
                                    self.blockWeights[file][(qs, qe)] = w[0]
                                continue
                            keys=list(self.blockWeights[file].keys())
                            for mLines in keys:
                                if mLines[1] < qs:
                                    insertion = False
                                    # check insertion
                                    for k in qLineNums:
                                        lines = qLineNums[k]
                                        if (lines[0] > mLines[1] and lines[0] < qs) or (
                                                        lines[1] > mLines[1] and lines[1] < qs):
                                            insertion = True
                                            break
                                    if not insertion:
                                        self.blockWeights[file][(mLines[0], qe)] = w[0] + self.blockWeights[file][
                                            mLines]
                                        self.blockWeights[file].pop(mLines)
                                        forwMerge = True
                                elif mLines[0] > qe:
                                    insertion = False
                                    # check insertion
                                    for lines in qLineNums.values():
                                        if (lines[1] < mLines[0] and lines[1] > qe) or (
                                                        lines[0] < mLines[0] and lines[0] > qe):
                                            insertion = True
                                            break
                                    if not insertion:
                                        self.blockWeights[file][(qs, mLines[1])] = w[0] + self.blockWeights[file][
                                            mLines]
                                        self.blockWeights[file].pop(mLines)
                                        BackMerge = True
                                if forwMerge and BackMerge:
                                    break
                            if not forwMerge and not BackMerge:
                                self.blockWeights[file][(qs,qe)]=w[0]

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



