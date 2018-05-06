#!/usr/bin/env python3
import javalang
from Interfaces import FCIConverter as conv
from Interfaces import LogWriter as lg
import pickle
import hashlib
from JavaAST import Results
import redis
import os

q1=open("/Users/hester/Desktop/Final-Year-Project/Hester'sWorkSpace/JavaAST/testCases/java1",'r').read()
q2=open("/Users/hester/Desktop/Final-Year-Project/Hester'sWorkSpace/JavaAST/testCases/java2",'r').read()
q3=open("/Users/hester/Desktop/Final-Year-Project/Hester'sWorkSpace/JavaAST/testCases/java3",'r').read()

class JavaAST():
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)  # host是redis主机，需要redis服务端和客户端都启动 redis默认端口是6379
    lw = lg.LogWriter()
    path = "/Users/hester/Desktop/JavaProgram/testACM/src/testACM"  # path name
    index_path = '/Users/hester/Desktop/finalYearProject/CodexIndexJavaAST.pik'

    weights = {}  # {weight:[fileNames] }
    fileIndex={} #{fileName: {weight:{nodeHash:(startLine,EndLine)] } }
    files = []
    documents = {}

    # these parameters should be tuned
    matchingThreshold = 0.6
    weightThreshold = 10  # weight outweigh weightThreshold will be taken into consideration
    blockThreshold = 50  # weight outweigh the blockthreshold means this node will be a code block which should be included into the global searching
    pageNum = 10
    wholeSimilarity = 0
    matchingBlock = {}  # {docID: (the startline and endline of the matching blocks)}.
    blockWeights = {}  # {docID: (startline, endline): weight of the biggest matching block}
    expireTime = 30

    def readFiles(self):
        self.lw.write_info_log("reading files...")
        self.files = os.listdir(self.path)  # get all the file names
        self.files.remove('.DS_Store')
        for file in self.files:  # go through the folder
            if not os.path.isdir(file):  # judge if it is a folder
                # self.documents[file] = conv.to_dic(self.path + "/" + file)
                self.documents[file]=open(self.path+'/'+file,'r').read()
                if len(self.documents[file].strip()) > 0:
                    try:
                        tree = javalang.parse.parse(self.documents[file])
                    except(SyntaxError):
                        self.lw.write_error_log("syntax error! " + file)
                        continue
                    # remove strings and variable names
                    self.fileIndex[file] = {}
                    names = []  # self defined name
                    self.index(tree, file, names,{}, {}, False)
                    # print(self.fileIndex[file])
                else:
                    self.documents.pop(file)
        self.files = list(self.documents.keys())

        self.lw.write_info_log("get " + str(len(self.documents)) + " documents")
        # use pickle module to save data into file 'CodexIndexAST.pik'
        with open(self.index_path, 'wb')as f:
            pickle.dump(self.weights, f, True)
            pickle.dump(self.fileIndex, f, True)

        # self.names=[]
        # tree=javalang.parse.parse(q3)
        # self.fileIndex['q3'] = {}
        # self.index(tree, 'q3')
        # print('#############################################')
        # for weight in self.fileIndex['q2']:
        #     if weight in self.fileIndex['q3']:
        #         print(weight)
        #         print(self.fileIndex['q2'][weight])
        #         print(self.fileIndex['q3'][weight])
        #     else:
        #         print(weight)
        #
        # print(self.fileIndex['q2'])
        # print(self.fileIndex['q3'])


    def index(self, root, fileName,names, nestHash, qLineNums, nestedDic):
        weight = 1
        min = 0
        max = 0
        i = 0
        startLine = 0
        endLine = 0
        # print('-----------------------')
        # print(root)
        attriValues =''  # "attr1 attr2 attr3"
        if isinstance(root, list) and len(root) == 0:
            return (weight, min, max, '')
        hashAttris = None
        if not isinstance(root, list):
            # if hasattr(root, "_position"):
            #     print(root._position)
            if isinstance(root, javalang.ast.Node):
                children =list(root.children)
            elif isinstance(root, tuple):
                children = root
            else:
                return (weight, min, max, attriValues)
            #get attributes information
            hasContent=False
            if hasattr(root, 'attrs'):
                attriValues+='( '
                for a in root.attrs:
                    v = root.__getattribute__(a)
                    if a is not 'documentation':
                        # remove identifier names
                        #except javalang.tree.ReferenceType, javalang.tree.ReferenceType,
                        if a is 'name' and ((not isinstance(root,javalang.tree.ReferenceType) and not isinstance(root,javalang.tree.ReferenceType)) or v in names):
                            if v not in names:
                                # print('================')
                                # print(v)
                                names.append(v)
                            children.remove(v)
                            continue
                        elif a is 'member':
                            # PROBLEM: if the member is a method name not in self.names(defined below the current node), we will fail to ignore it
                            if v in names:
                                # print('~~~~~~~~~~~~~~~~~~~~~~~~~')
                                # print(v)
                                children.remove(v)
                                continue
                        elif a == 'qualifier':
                            # remove printing out
                            if v == 'System.out':
                                return (0, min, max,None)
                            elif v in names:
                                children.remove(v)
                                continue
                        elif v=='MethodInvocation':
                            if hasattr(v,'qualifier') and v.__getattribute__('qualifier')=='System.out':
                                return (0, min, max,None)
                        # ignore values like strings, numbers, booleans, null
                        elif a == 'value' and type(v) is str:
                            children.remove(v)
                            continue
                        elif v != None and v != '' and not (isinstance(v, list) and len(v) == 0):
                            if not isinstance(v,list):
                                if isinstance(v, javalang.tree.MethodInvocation) and hasattr(v,'attrs') and  v.__getattribute__('qualifier')=='System.out':
                                    return (0, min, max, None)

                                hasContent=True
                                attriValues+=str(v)+": "

                            if isinstance(v, (javalang.ast.Node, tuple, list)):
                                children.remove(v)
                                # print(v)
                                t = self.index(v, fileName,names, nestHash,qLineNums,nestedDic)

                                weight += t[0]
                                if t[1] > 0:
                                    startLine = t[1]
                                    if i == 0:
                                        min = startLine
                                    elif startLine < min:
                                        min = startLine
                                    i += 1
                                if t[2] > 0:
                                    endLine = t[2]
                                    if endLine > max:
                                        max = endLine
                                    i += 1
                                if t[3] != ''and t[3] is not None and t[3]!='( ':
                                    hasContent=True
                                    attriValues += t[3] + ', '
                    else:
                        children.remove(v)
            if len(children)>0:
                if not hasattr(root, 'attrs'):
                    attriValues += '( '

                for child in children:
                    #ignore some meaningless nodes
                    if child != None and child != '' and not isinstance(child, list) and child not in names:
                        attriValues+=str(child)+': '
                    if isinstance(child, (javalang.ast.Node, tuple, list)):
                        t=self.index(child,fileName,names, nestHash,qLineNums,nestedDic)

                        weight += t[0]
                        if t[1] > 0:
                            startLine = t[1]
                            if i == 0:
                                min = startLine
                            elif startLine < min:
                                min = startLine
                            i += 1
                        if t[2] > 0:
                            endLine = t[2]
                            if endLine > max:
                                max = endLine
                            i += 1
                        if t[3] is not '' and t[3] is not None and t[3]!='( ':
                            hasContent=True
                            attriValues+=t[3]+', '

            if hasContent:
                attriValues += ' )'
            else:
                #no brackets
                attriValues=attriValues.lstrip('( ')
            #work out line number
            if hasattr(root, "_position"):
                lineNo=root._position[0]
                if min == 0 and max == 0:
                    min = lineNo
                    max = lineNo

            # put the weight into weights
            if weight >= self.weightThreshold:
                if not nestedDic:
                    if weight in self.weights:
                        if fileName not in self.weights[weight]:
                            self.weights[weight].append(fileName)
                    else:
                        self.weights[weight] = [fileName]

                #hash the attribute values list
                m = hashlib.md5()
                m.update(attriValues.encode("utf8"))
                hashAttris = m.hexdigest()

                # print(',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,')
                # print(self.fileIndex[fileName])
                #put the node into fileIndex
                if weight not in self.fileIndex[fileName]:
                    self.fileIndex[fileName][weight]={}
                self.fileIndex[fileName][weight][hashAttris]=(min,max)

                # print(weight)
                # print(attriValues)
                # print((str(root),hashAttris,min,max))
                #put all its childern in this file into the current node
                if nestedDic:
                    nestHash[(weight,hashAttris,min,max)]={}
                    qLineNums[hashAttris]=(min,max)
                    for w in self.fileIndex[fileName]:
                        if w<weight:
                            keys=list(self.fileIndex[fileName][w].keys())
                            for k in keys :
                                t=self.fileIndex[fileName][w][k]
                                if t[0]>=min and t[1]<=max:
                                    # print('11111111111111111111111111111111')
                                    # print((w,k,t[0],t[1]))
                                    # print((weight,hashAttris,min,max))
                                    # the block is the sub node of the current node
                                    nestHash[(weight,hashAttris,min,max)][(w,k,t[0],t[1])]={}
                                    self.fileIndex[fileName][w].pop(k)

                    #put the children in nestHash into the current node
                    keys2=list(nestHash.keys())
                    for k in keys2:
                        if k in nestHash:
                            if k[0]<weight and k[2]>=min and k[3]<=max:
                                # print('!!!!!!!!!!!!!!!!!!!!!!!!!')
                                # print(k)
                                # print((weight,hashAttris,min,max))
                                nestHash[(weight,hashAttris,min,max)][k]=nestHash.pop(k)

            return (weight, min, max, attriValues)



        else:
            l=[]
            length=len(root)
            j=0
            while j < length:
                r=root[j]
                rStr=''
                if r != None and r != '':
                    t=self.index(r, fileName,names, nestHash,qLineNums, nestedDic)
                    weight += t[0]
                    if t[1] > 0:
                        startLine = t[1]
                        if i == 0:
                            min = startLine
                        elif startLine < min:
                            min = startLine
                        i += 1
                    if t[2] > 0:
                        endLine = t[2]
                        if endLine > max:
                            max = endLine
                        i += 1
                    if t[3] is not None:
                        rStr += str(r) + ':'
                        if t[3] is not '':
                            rStr+=t[3]
                        else:
                            rStr +=''
                        l.append(rStr)
                        j+=1
                    else:
                        root.pop(j)
                        length-=1
                else:
                    root.pop(j)
                    length -= 1

            if len(l)>0:
                #sort the list in order to ignore the code order change
                l.sort()
                attriValues+='[ '+''.join(l)+' ]'
            return (weight, min, max, attriValues)


            # interface to front end. Input query, return a Result instance

    def getResults(self, query, page):
        globalSimilarity = 0
        matchingBlocks = {}
        componentDocuments = []
        if not self.r.exists(query):  # if the result is not in the redis
            #read pickle file
            if os.path.exists(self.index_path):
                rfile = open(self.index_path, 'rb')
                self.weights = pickle.load(rfile)
                self.fileIndex = pickle.load(rfile)
            else:
                self.readFiles()

            # store the result of the query into redis
            matchingLines = {}  # {fileName:[(qStart,qEnd, fStart,fEnd)]}
            similarities = self.search(query, matchingLines)
            if similarities == None:
                self.lw.write_error_log('Pickle files not found!')
                return None
            elif similarities == 0:
                return 0
            # get the normal relevant documents and the suspected plagiarized documents
            globalSimilarity = self.wholeSimilarity
            matchingBlocks = self.matchingBlock
            documentList = sorted(similarities, key=similarities.get, reverse=True)
            plagiarismList = [] #[sorted plagiarised files]
            i = 0
            for d in documentList:
                if similarities[d] > self.matchingThreshold:
                    plagiarismList.append(d)
                    i += 1
                else:
                    break
            documentList = documentList[i:]
            componentDocuments = list(matchingBlocks.keys())
            # store data into the redis server
            self.lw.write_info_log("storing results into redis in form of list")
            self.r.rpush(query, plagiarismList)
            self.r.rpush(query, documentList)
            self.r.rpush(query, matchingLines)
            if globalSimilarity != 0 and len(matchingBlocks) != 0:
                if len(plagiarismList) > 0:
                    if globalSimilarity >= similarities[plagiarismList[0]] and globalSimilarity >= self.matchingThreshold:
                        self.r.rpush(query, globalSimilarity)
                        self.r.rpush(query, matchingBlocks)
                        self.r.rpush(query, componentDocuments)
                    else:
                        globalSimilarity = 0
                        matchingBlocks = {}
                        componentDocuments = []
                else:
                    #if no plagiarised case is found, display the component programs
                    self.r.rpush(query, globalSimilarity)
                    self.r.rpush(query, matchingBlocks)
                    self.r.rpush(query, componentDocuments)

        # get the result list of this query from redis
        else:
            self.lw.write_info_log("geting results from redis")
            plagiarismList = eval(self.r.lindex(query, 0))
            documentList = eval(self.r.lindex(query, 1))
            matchingLines = eval(self.r.lindex(query, 2))
            if self.r.llen(query) >= 6:
                globalSimilarity = eval(self.r.lindex(query, 3))
                matchingBlocks = eval(self.r.lindex(query, 4))
                componentDocuments = eval(self.r.lindex(query, 5))

        self.r.expire(query, self.expireTime)  # expire after 30s

        # encalsulate results into the object:Result
        documentListLength = len(documentList)
        plagiarismListLength = len(plagiarismList)
        matchingblocksLength = len(componentDocuments)
        length = documentListLength + plagiarismListLength + matchingblocksLength
        results = Results.Results(numOfResults=length, matchingLines=matchingLines,
                                  globalSimilarity=globalSimilarity, matchingBlocks=matchingBlocks)
        disMatchingBlocks = []
        disPlagiarismList = []
        disDocumentList = []
        if (page - 1) * self.pageNum < matchingblocksLength:  # need to display the maching blocks
            disMatchingBlocks = componentDocuments[
                                (page - 1) * self.pageNum: min(page * self.pageNum, matchingblocksLength)]
            results.setComponentDocuments(disMatchingBlocks)

        if (
            page - 1) * self.pageNum < matchingblocksLength + plagiarismListLength and page * self.pageNum >= matchingblocksLength:
            # need to display the plagiarism documents
            if len(disMatchingBlocks) == 0 and page > 1:  # not start from 0
                disPlagiarismList = plagiarismList[(page - 1) * self.pageNum - matchingblocksLength: min(
                    (page * self.pageNum - matchingblocksLength), plagiarismListLength)]
            else:  # start from 0
                disPlagiarismList = plagiarismList[0: min(self.pageNum, plagiarismListLength)]
            results.setPlagiarismList(disPlagiarismList)

        if page * self.pageNum > matchingblocksLength + plagiarismListLength:  # need to dispaly the relevant documents
            if len(disMatchingBlocks) == 0 and len(disPlagiarismList) == 0 and (
                page - 1) * self.pageNum <= length:  # not start from 0
                disDocumentList = documentList[
                                  (page - 1) * self.pageNum - matchingblocksLength - plagiarismListLength: min(
                                      (page * self.pageNum - matchingblocksLength - plagiarismListLength),
                                      documentListLength)]
            elif (page - 1) * self.pageNum <= length:  # start from 0
                disDocumentList = documentList[0: min((self.pageNum - matchingblocksLength - plagiarismListLength),
                                                      documentListLength)]
            else:
                self.lw.write_error_log("page number out of range")
                return None
            results.setDocumentList(disDocumentList)

        print('==============')
        results.toString()
        return results


    def search(self, query, matchingLines): # matchingLines {fileName:[(qStart,qEnd, fStart,fEnd)]}
        # refresh the global variables
        self.wholeSimilarity = 0
        self.matchingBlock = {}
        self.blockWeights = {}
        qTree = {}  # {(weight,nodeHash,startLine, endLine):{nested dictionaries}}
        qLineNums={}

        root = javalang.parse.parse(query)
        self.fileIndex['query'] = {}
        names=[]
        self.index(root,'query',names, qTree,qLineNums,True)
        # print(qTree)
        # print(qLineNums)
        self.fileIndex.pop('query')
        similarities={} # {fileName:score}
        maxWeight=list(qTree.keys())[0][0]
        self.similarities(qTree,self.weights,similarities,maxWeight,qLineNums,matchingLines)

        # work out the global similarity
        for dic in self.blockWeights:
            biggestKey = sorted(self.blockWeights[dic], key=self.blockWeights[dic].get, reverse=True)[0]
            if self.blockWeights[dic][biggestKey] > self.blockThreshold:
                ds = list(self.matchingBlock.keys())
                store = True
                for d in ds:
                    block = self.matchingBlock[d]
                    # do not store in if the new block is included in some block within the matchBlock
                    if biggestKey[0] >= block[0] and biggestKey[1] <= block[1]:
                        store = False
                        break
                    # delete the older block included in the new block
                    elif biggestKey[0] <= block[0] and biggestKey[1] >= block[1]:
                        self.matchingBlock.pop(d)
                        self.wholeSimilarity -= self.blockWeights[d][block] / maxWeight

                    # deal with the block that have some part overlapping with old blocks (store the one with bigger weight)
                    elif (biggestKey[0] <= block[1] and biggestKey[0] >= block[0]) or (
                            biggestKey[1] <= block[1] and biggestKey[1] >= block[0]):
                        if self.blockWeights[dic][biggestKey] > self.blockWeights[d][block]:
                            self.matchingBlock.pop(d)
                            self.wholeSimilarity -= self.blockWeights[d][block] / maxWeight
                        else:
                            store = False
                            break

                # store the new block
                if store:
                    self.matchingBlock[dic] = biggestKey
                    self.wholeSimilarity += self.blockWeights[dic][biggestKey] / maxWeight

        return similarities

    # calculate the similarities between corpus and query
    def similarities(self, qTree, weights, similarities, maxWeight,qLineNums, matchingLines):
        #matchingBlock: {docID: (the startline and endline of the matching blocks)}.
        #blockWeights: {docID: (qStartline, qEndline): weight of the biggest matching block}
        if maxWeight is None:
            maxWeight = 1
        for w in qTree:
            if isinstance(w, tuple):
                find = False
                if w[0] in weights:
                    for file in weights[w[0]]:
                        #check if the nodeHash is in this file
                        if w[1] in self.fileIndex[file][w[0]]:
                            find = True
                            qs = w[2]
                            qe = w[3]
                            fs = self.fileIndex[file][w[0]][w[1]][0]
                            fe = self.fileIndex[file][w[0]][w[1]][1]
                            if file in similarities:
                                matchingLines[file].append((qs, qe, fs, fe))
                                similarities[file] += w[0] / maxWeight
                            else:
                                matchingLines[file] = [(qs, qe, fs, fe)]
                                similarities[file] = w[0] / maxWeight

                            # merge lines in query program to construct the code blocks
                            forwMerge = False
                            BackMerge = False
                            if file not in self.blockWeights:
                                self.blockWeights[file] = {}
                            elif (qs, qe) in self.blockWeights[file]:
                                if w[0] > self.blockWeights[file][(qs, qe)]:
                                    self.blockWeights[file][(qs, qe)] = w[0]
                                continue
                            keys = list(self.blockWeights[file].keys())
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
                                self.blockWeights[file][(qs, qe)] = w[0]
                if not find and qTree[w] is not None:
                    if len(qTree[w]) > 0:
                        self.similarities(qTree[w], weights, similarities, maxWeight,qLineNums, matchingLines)




