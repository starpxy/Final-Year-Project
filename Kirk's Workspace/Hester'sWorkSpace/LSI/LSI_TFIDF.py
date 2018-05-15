import numpy as np
# from scipy.linalg import *
from scipy import spatial
# import matplotlib.pyplot as plt
from scipy.sparse import *
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from Interfaces import FCIConverter as conv
from Interfaces import LogWriter as lg
import os
# import math
from LSI import Results
import pickle
import time
from scipy.sparse.linalg import svds

#singleton
# class Singleton(object):
#     _instance = None
#     def __new__(cls, *args, **kw):
#         if not cls._instance:
#             cls._instance = super(Singleton, cls).__new__(cls, *args, **kw)
#         return cls._instance

class LSI_TFIDF():
    lw = lg.LogWriter()
    # get files

    files = []
    documents = {}
    sortedDocuments = []
    contents = []
    X = None
    re = None
    word = None
    vectorizer = None
    tfidf = None
    s=None
    u=None
    d=None
    idf=None
    lineNo={}
    expireTime=30
    end_time=time.clock()

    def __init__(self):
        super(LSI_TFIDF, self).__init__()
        self.path = "C:\\Users\\soapk\\Desktop\\java1"  # path name
        self.index_path='C:\\Users\\soapk\\Desktop\\LSIindexTest_java1_noT.pik'

        # indexing
    def indexing(self):
        self.lw.write_info_log("reading files...")
        self.files = os.listdir(self.path)  # get all the file names
        if '.DS_Store' in self.files:
            self.files.remove('.DS_Store')
        fs = len(self.files)
        self.tfidf = TfidfVectorizer()
        i = 0
        while i < fs:  # go through the folder
            file = self.files[i]
            if not os.path.isdir(file):  # judge if it is a folder
                self.lw.write_info_log("preprocessing files..." + file)
                self.documents[file] = conv.to_dic(self.path + "/" + file)
                if len(self.documents[file]['content'].strip()) > 0:
                    self.contents.append(self.documents[file]['content'])
                    #store the line numbers of the term
                    self.lineNo[file]={}
                    j=0
                    for line in self.documents[file]['content'].split('\n'):
                        lineList=[line]
                        if len(lineList)>0:
                            try:
                                self.tfidf.fit_transform(lineList) #get the unique standard term of this line
                            except ValueError:
                                j += 1
                                continue
                            for term in self.tfidf.vocabulary_:
                                if term in self.lineNo[file]:
                                    self.lineNo[file][term].append(j)
                                else:
                                    self.lineNo[file][term]=[j]
                        j+=1
                    i+=1
                else:
                    self.documents.pop(file)
                    self.files.remove(file)
                    fs-=1
            else:
                self.files.remove(file)
        print('finish reading')
        # self.files = list(self.documents.keys())
        size=len(self.documents)
        self.lw.write_info_log("get " + str(size) + " documents")
        self.lw.write_info_log("indexing...")
        self.stopwords = ['and', 'edition', 'for', 'in', 'little', 'of', 'the', 'to', 'print']
        self.re = self.tfidf.fit_transform(self.contents).toarray().T  # tf-idf values
        self.idf=self.tfidf.idf_
        self.word=self.word=list(self.tfidf.vocabulary_.keys())

        #compression matrix
        self.re=dok_matrix(self.re)
        # self.X=dok_matrix(self.X)
        print("start SVD")
        # svd decomposition
        self.u, self.s, self.d = svds(self.re, k = 500, return_singular_vectors='u')
        print('start dumping')
        # store the index into the pickle
        with open(self.index_path, 'wb')as f:  # use pickle module to save data into file 'CodexIndex.pik'
            pickle.dump(self.s, f, True)
            pickle.dump(self.u, f, True)
            pickle.dump(self.d, f, True)
            pickle.dump(self.tfidf, f, True)
            pickle.dump(self.lineNo,f,True)
            print('finish')

    def getResult(self, query):
        self.vectorizer = CountVectorizer()
        # if there exist the pickle file, read it
        if os.path.exists(self.index_path):
            rfile = open(self.index_path, 'rb')
            self.s = pickle.load(rfile)
            self.u = pickle.load(rfile)
            self.d = pickle.load(rfile)
            self.tfidf = pickle.load(rfile)
            self.lineNo = pickle.load(rfile)

            self.idf = self.tfidf.idf_
            self.word = list(self.tfidf.vocabulary_.keys())
            self.files = list(self.lineNo.keys())

        else:  # if there is no such pickle file, indexing
            self.indexing()

        l = self.MatrixSearching(query, self.s,self.u, self.d.T)
        if l is None:
            return Results.Results(0)

        results=Results.Results(numOfResults=l[3],matchingLines=l[2],hitDocs=l[1],fullHitLines=l[0])



        return results  # return results



    def MatrixSearching(self, query, s, u, d):

        qFreq = self.vectorizer.fit_transform([query]).toarray().T  # make the vectorizer fit the query
        qWord = self.vectorizer.get_feature_names()  # the unique terms after preprocessing
        qArr = np.zeros([1, len(self.word)])

        # fill in the tf-idf into the empty Xq matrix
        ifEmpty = True
        j=0
        for w in qWord:
            i=qWord.index(w)
            if w in self.word:
                j = self.word.index(w)
                qArr[0][j] = qFreq[i] * self.idf[j]
                ifEmpty = False

        # give the warning and stop searching if no terms found
        if ifEmpty:
            self.lw.write_warning_log("Nothing found!")
            return None

        # similarities from Dq=X.T * T * S-1.
        sDiagno = np.diag(np.array(s))
        sInv = np.linalg.inv(sDiagno)
        Dq = np.dot(qArr, u)
        Dq = np.dot(Dq, sInv)

        matchingLines = {}  # {similarity:[(docName, [hit lines])] }
        hitDocs = {}  # {lengthHits:[(docName,[hit lines])]}
        fullHitLines = {}  # {fullHitNum:[(docName,[hit lines])]}
        length=0
        for i in range(len(d)):
            k=self.files[i]
            similarity=((np.dot(Dq, d[i])) / ((np.linalg.norm(Dq)) * (np.linalg.norm(d[i]))))[0]
            length+=1
            hitLines = []
            hitWords = 0
            commonLines = []
            ifFullHit=True
            for t in qWord:
                if t in self.lineNo[k]:
                    hitWords += 1
                    hitLines = list(set(hitLines).union(set(self.lineNo[k][t])))
                    if hitWords == 1:
                        commonLines = self.lineNo[k][t]
                    commonLines = list(set(commonLines).intersection(set(self.lineNo[k][t])))
                else:
                    ifFullHit=False
            lengthHit = len(hitLines) * hitWords
            if hitWords > 1 and ifFullHit:
                fullHit = len(commonLines)
            else:
                fullHit = 0
            if fullHit > 0:
                if fullHit in fullHitLines:
                    fullHitLines[fullHit].append((k, hitLines))
                else:
                    fullHitLines[fullHit] = [(k, hitLines)]
            elif lengthHit > 0:
                if lengthHit in hitDocs:
                    hitDocs[lengthHit].append((k, hitLines))
                else:
                    hitDocs[lengthHit] = [(k, hitLines)]
            else:
                if similarity>0:
                    if similarity not in matchingLines:
                        matchingLines[similarity]=[(k, hitLines)]
                    else:
                        matchingLines[similarity].append((k, hitLines))
                else:
                    # don't store it
                    length-=1

        return (fullHitLines,hitDocs,matchingLines,length)




    # #highlight the matching lines
    # def highlighting(self,ocurrence,qWord,similarities):
    #     if similarities is None:
    #         return None
    #     rT=self.X.T
    #     #construct matching lines
    #     machingLines=[]
    #     for doc in similarities:
    #         i=self.files.index(doc)
    #         if np.dot(rT[i], ocurrence[0]) >0:
    #             lines=[]
    #             lineNo=0
    #             for line in self.contents[i].split('\n'):
    #                 if line.strip() is '':
    #                     lineNo+=1
    #                     continue
    #                 try:
    #                     self.vectorizer.fit_transform([line])
    #                 except ValueError:
    #                     lineNo += 1
    #                     continue
    #                 else:
    #                     w = self.vectorizer.get_feature_names()
    #                     if len(list(set(w).intersection(set(qWord))))>0:
    #                         lines.append(lineNo)
    #                 lineNo+=1
    #             machingLines.append((doc, lines))
    #         else:
    #             machingLines.append((doc, []))
    #
    #     return machingLines




        # print(r.get('sortedDocuments'))  # 取出键name对应的值

        # throw away the low-frequency terms (terms appears only once)

        # i=0
        # while True:
        #     if i>=len(word):
        #         break
        #     if X[i]<2:
        #         word.pop(i)
        #         X=np.delete(X,i,0)
        #         re=np.delete(re,i,0)
        #     else:
        #         i+=1
        #
        # print(re.shape)


        # def printA(query):
        #     print('re\n')
        #     print(re)
        #     u, s, vt = svd(re, full_matrices=False)
        #     print("""\r""")
        #     print('u\n')
        #     print(u)
        #     print("""\r""")
        #     print('s\n')
        #     print(s)
        #     print("""\r""")
        #     print('vt\n')
        #     print(vt)
        #     print("""\r""")
        #     d = vt.T
        #
        #     plt.title("LSI Subspace with TF-IDF weight")
        #     plt.xlabel(u'dimention2')
        #     plt.ylabel(u'dimention3')
        #
        #     ut = u.T  # Transaction
        #     demention2 = ut[1]
        #     demention3 = ut[2]
        #     # draw terms
        #     for i in range(len(demention2)):
        #         plt.text(demention2[i], demention3[i], word[i])
        #         plt.plot(demention2[i], demention3[i], '*')  # draw points
        #
        #     vdemention2 = vt[1]  # we choose the 2nd and 3rd dimensions because the first dimension has little meaning
        #     vdemention3 = vt[2]
        #     # get query coordinates
        #     # get the term frequency
        #     qFreq = vectorizer.fit_transform([query]).toarray().T  # make the vectorizer fit the query
        #     qWord = vectorizer.get_feature_names()  # the unique terms after preprocessing
        #     qArr = np.zeros([1, len(word)])
        #     # fill in the term frequency into the empty Xq matrix
        #     for w in qWord:
        #         i = qWord.index(w)
        #         if w in word:
        #             j = word.index(w)
        #             idf = len(np.nonzero(re[j])[0])
        #             idf = (1 + len(files)) / (idf + 1)
        #             idf = math.log2(idf) + 1
        #             qArr[0][j] = qFreq[i] * idf
        #
        #     dX = np.dot(np.array(demention2), np.array(qArr))/len(qArr)
        #     dY = np.dot(np.array(demention3), np.array(qArr))/len(qArr)
        #     # draw query point
        #     plt.text(dX, dY, 'QUERY')
        #     plt.plot(dX, dY, 'ro')
        #     similarities={}
        #     for j in range(len(vdemention2)):
        #         plt.text(vdemention2[j], vdemention3[j], 'T' + str(j))
        #         plt.plot(vdemention2[j], vdemention3[j], '.')
        #         # calculate the eclidean distance similarity
        #         similarity=math.sqrt(math.pow((vdemention2[j]-dX),2)+math.pow((vdemention3[j]-dY),2))
        #         similarities[files[j]]=similarity
        #     # sort similarity and print out
        #     centroidResult = sorted(similarities.keys(),key=similarities.__getitem__,reverse=True)
        #     return centroidResult





        # printA()
        # plt.show()
        # getDocumentList(query, 2)