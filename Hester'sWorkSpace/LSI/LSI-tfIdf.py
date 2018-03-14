import numpy as np
from scipy.linalg import *
from scipy import spatial
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from Interfaces import FCIConverter as conv
from Interfaces import LogWriter as lg
import os
import math
import redis
from LSI import Results
import pickle

class LSI_TFIDF:
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)  # host是redis主机，需要redis服务端和客户端都启动 redis默认端口是6379
    lw = lg.LogWriter()
    # get files
    path = "../files"  # path name
    files = []
    documents = {}
    sortedDocuments = []
    contents = []
    wholeContent = ""
    X = ''
    re = []
    word = ''
    vectorizer = ''
    tfidf = ''
    pageNum = 3

    def __init__(self):
        self.lw.write_info_log("reading files...")
        self.files = os.listdir(self.path)  # get all the file names
        for file in self.files: #go through the folder
            if not os.path.isdir(file): #judge if it is a folder
                if not file=='.DS_Store':
                    print(file)
                    self.documents[file]=conv.to_dic(self.path+"/"+file)
                    self.contents.append(self.documents[file]['code'])
                    self.wholeContent+=self.documents[file]['code']
        self.lw.write_info_log("get "+str(len(self.documents))+" documents")
        self.lw.write_info_log("indexing...")
        self.stopwords = ['and', 'edition', 'for', 'in', 'little', 'of', 'the', 'to','print']
        self.vectorizer = CountVectorizer()
        self.tfidf = TfidfVectorizer()

    #indexing
    def indexing(self):
        self.X = self.vectorizer.fit_transform([self.wholeContent]).toarray().T
        self.transformer=TfidfTransformer()
        self.re = self.tfidf.fit_transform(self.contents).toarray().T #tf-idf values
        self.word=self.vectorizer.get_feature_names()#the unique terms after preprocessing
        #store the index into the pickle
        with open('CodexIndex.pik', 'wb')as f:  # use pickle module to save data into file 'CodexIndex.pik'
            pickle.dump(self.re, f, True)
            pickle.dump(self.X, f, True)
            pickle.dump(self.word, f, True)
            pickle.dump(self.transformer, f, True)


    def getDocumentList(self,query,page):
        # use pickle module to read data into our program if CodexIndex.pik exists, load the data directly
        if os.path.exists("CodexIndex.pik"):
            rfile = open('CodexIndex.pik', 'rb')
            self.re = pickle.load(rfile)
            self.X=pickle.load(rfile)
            self.word=pickle.load(rfile)
            self.transformer=pickle.load(rfile)

        sortedDocuments=[]
        #check if the result of this query already exist in the redis
        if not self.r.exists(query):#if the result is not in the redis
            #store the result of the query into redis
            l=self.MatrixSearching(query)
            if l is None:
                return None
            self.lw.write_info_log("storing results into redis in form of list")
            for j in range(len(l)):
                self.r.rpush(query, l[j])
                if (page-1)*self.pageNum<j and j<page*self.pageNum:
                    sortedDocuments.append(self.documents[l[j]])
            results=Results(len(l),sortedDocuments)
        #get the result list of this query from redis
        # catch 10 documents at a time
        else:
            self.lw.write_info_log("geting results from redis")
            i=(page-1)*self.pageNum
            while i<page*self.pageNum:
                fileName=self.r.lindex(query,i)
                sortedDocuments.append(self.documents[fileName])
                i+=1
            length=self.r.llen(query)
            results=Results(length,sortedDocuments)
        self.r.expire(query, 30)#expire after 30s

        return results#return results


    # print(r.get('sortedDocuments'))  # 取出键name对应的值

#throw away the low-frequency terms (terms appears only once)
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


    def MatrixSearching(self,query):
        #svd decomposition
        print('re\n')
        print(self.re)
        u, s, vt = svd(self.re, full_matrices=False)
        print("""\r""")
        print('u\n')
        print(u)
        print("""\r""")
        print('s\n')
        print(s)
        print("""\r""")
        print('vt\n')
        print(vt)
        print("""\r""")
        d = vt.T

        # work out the Xq.T
        # get the term frequency
        qFreq = self.vectorizer.fit_transform([query]).toarray().T  # make the vectorizer fit the query
        qWord = self.vectorizer.get_feature_names()  # the unique terms after preprocessing
        qArr = np.zeros([1, len(self.word)])
        # fill in the term frequency into the empty Xq matrix
        ifEmpty=True
        for w in qWord:
            i = qWord.index(w)
            if w in self.word:
                ifEmpty=False
                j = self.word.index(w)
                idf=len(np.nonzero(self.re[j])[0])
                idf=(1+len(self.files))/(idf+1)
                idf=math.log2(idf)+1
                qArr[0][j] = qFreq[i]*idf
        #give the warning and stop searching if no terms found
        if ifEmpty:
            self.lw.write_warning_log("Nothing found!")
            return None

        # print(qArr)
        sDiagno = np.diag(np.array(s))
        sInv = np.linalg.inv(sDiagno)
        # print("sDiago inverse")
        # print(sInv)
        # print('u')
        # print(u)
        Dq = np.dot(qArr, u)
        Dq = np.dot(Dq, sInv)
        # print(Dq)
        # similarities from Dq=X.T * T * S-1.
        similarities={}
        for i in range(len(d)):
            # similarity[i]=spatial.distance.cosine(Dq, d[i])
            similarities[self.files[i]]=np.dot(Dq, d[i])/ (np.linalg.norm(Dq) * (np.linalg.norm(d[i])))
        # matrixSimilarity=sorted(similarities.items(),key=lambda item:item[1],reverse=True)
        matrixSimilarity=sorted(similarities.keys(),key=similarities.__getitem__,reverse=True)
        print(matrixSimilarity)
        #turn the id list into sorted document list
        return matrixSimilarity


# printA()
# plt.show()
# getDocumentList(query, 2)