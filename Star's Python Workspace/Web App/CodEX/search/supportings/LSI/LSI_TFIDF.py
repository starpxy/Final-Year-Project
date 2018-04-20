import numpy as np
from scipy.linalg import *
from scipy import spatial
# import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from search.supportings import FCIConverter as conv
from search.supportings import LogWriter as lg
import os
import math
import redis
import search.supportings.LSI.Results as Results
import pickle
import CodEX.config as config

class LSI_TFIDF:
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)  # host是redis主机，需要redis服务端和客户端都启动 redis默认端口是6379
    lw = lg.LogWriter()
    # get files
    path = config.configs['paths']['FCI_path']  # path name
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
    pageNum = config.configs['others']['page_num']
    indexing_path = config.configs["paths"]["LSI_indexing_path"]

    def __init__(self):
        self.lw.write_info_log("reading files...")
        self.files = os.listdir(self.path)  # get all the file names
        # self.files.remove('.DS_Store')
        for file in self.files:  # go through the folder
            if not os.path.isdir(file):  # judge if it is a folder
                self.documents[file] = conv.to_dic(self.path + "/" + file)
                self.contents.append(self.documents[file]['content'])
                self.wholeContent += self.documents[file]['content']
        self.lw.write_info_log("get " + str(len(self.documents)) + " documents")
        # indexing
        self.lw.write_info_log("indexing...")
        self.stopwords = ['and', 'edition', 'for', 'in', 'little', 'of', 'the', 'to', 'print']
        self.vectorizer = CountVectorizer()
        self.tfidf = TfidfVectorizer()
        self.X = ''

        # indexing

    def indexing(self):
        self.transformer = TfidfTransformer()
        self.re = self.tfidf.fit_transform(self.contents).toarray().T  # tf-idf values
        self.vectorizer.fit_transform([self.wholeContent])
        self.word = self.vectorizer.get_feature_names()  # the unique terms after preprocessing
        self.X = self.vectorizer.fit_transform(self.contents).toarray().T
        # store the index into the pickle
        with open(self.indexing_path, 'wb')as f:  # use pickle module to save data into file 'CodexIndex.pik'
            pickle.dump(self.re, f, True)
            pickle.dump(self.X, f, True)
            pickle.dump(self.word, f, True)
            pickle.dump(self.transformer, f, True)

    def getDocumentList(self, query, page):
        # use pickle module to read data into our program if CodexIndex.pik exists, load the data directly
        if os.path.exists(self.indexing_path):
            rfile = open(self.indexing_path, 'rb')
            self.re = pickle.load(rfile)
            self.X = pickle.load(rfile)
            self.word = pickle.load(rfile)
            self.transformer = pickle.load(rfile)
        sortedDocuments = []
        # check if the result of this query already exist in the redis
        if not self.r.exists(query):  # if the result is not in the redis
            # store the result of the query into redis
            l = self.MatrixSearching(query)
            if l is None:
                return Results.Results(0, [])
            self.lw.write_info_log("storing results into redis in form of list")
            for j in range(len(l)):
                self.r.rpush(query, l[j])
                if (page - 1) * self.pageNum <= j and j < page * self.pageNum:
                    sortedDocuments.append(l[j])
            results = Results.Results(len(l), sortedDocuments)
        # get the result list of this query from redis
        # catch 10 documents at a time
        else:
            self.lw.write_info_log("geting results from redis")
            i = (page - 1) * self.pageNum
            length = self.r.llen(query)
            while i < page * self.pageNum and i < length:
                sortedDocuments.append(tuple(eval(self.r.lindex(query, i))))
                i += 1
            results = Results.Results(length, sortedDocuments)
        self.r.expire(query, 30)  # expire after 30s

        return results  # return results



    def MatrixSearching(self, query):
        # svd decomposition
        u, s, vt = svd(self.re, full_matrices=False)
        d = vt.T

        # work out the Xq.T
        # get the term frequency
        qFreq = self.vectorizer.fit_transform([query]).toarray().T  # make the vectorizer fit the query
        qWord = self.vectorizer.get_feature_names()  # the unique terms after preprocessing
        qArr = np.zeros([1, len(self.word)])
        ocurrence = np.zeros([1, len(self.word)])
        # fill in the term frequency into the empty Xq matrix
        ifEmpty = True
        for w in qWord:
            i = qWord.index(w)
            if w in self.word:
                ifEmpty = False
                j = self.word.index(w)
                ocurrence[0][j] += 1
                idf = len(np.nonzero(self.re[j])[0])
                idf = (1 + len(self.files)) / (idf + 1)
                idf = math.log2(idf) + 1
                qArr[0][j] = qFreq[i] * idf
        # give the warning and stop searching if no terms found
        if ifEmpty:
            self.lw.write_warning_log("Nothing found!")
            return None
        sDiagno = np.diag(np.array(s))
        sInv = np.linalg.inv(sDiagno)
        Dq = np.dot(qArr, u)
        Dq = np.dot(Dq, sInv)
        # similarities from Dq=X.T * T * S-1.
        similarities = {}
        for i in range(len(d)):
            # similarity[i]=spatial.distance.cosine(Dq, d[i])
            similarities[self.files[i]] = np.dot(Dq, d[i]) / (np.linalg.norm(Dq) * (np.linalg.norm(d[i])))
        # matrixSimilarity=sorted(similarities.items(),key=lambda item:item[1],reverse=True)
        similarities = sorted(similarities, key=similarities.get, reverse=True)
        machingLines = self.highlighting(ocurrence, qWord, similarities)
        # turn the id list into sorted document list
        return machingLines

    # highlight the matching lines
    def highlighting(self, ocurrence, qWord, similarities):
        if similarities is None:
            return None
        rT = self.X.T
        # construct matching lines
        machingLines = []
        for doc in similarities:
            i = self.files.index(doc)
            if np.dot(rT[i], ocurrence[0]) > 0:
                lines = []
                lineNo = 0
                for line in self.contents[i].split('\n'):
                    if line.strip() is '':
                        lineNo+=1
                        continue
                    try:
                        self.vectorizer.fit_transform([line])
                    except ValueError:
                        lineNo+=1
                        continue
                    else:
                        w = self.vectorizer.get_feature_names()
                        if len(list(set(w).intersection(set(qWord)))) > 0:
                            lines.append(lineNo)
                    lineNo += 1
                machingLines.append((doc, lines))
            else:
                machingLines.append((doc, []))

        return machingLines

        # printA()
        # plt.show()
        # getDocumentList(query, 2)