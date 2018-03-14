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


global r

r = redis.Redis(host='localhost', port=6379, decode_responses=True)   # host是redis主机，需要redis服务端和客户端都启动 redis默认端口是6379
lw=lg.LogWriter()
#get files
lw.write_info_log("reading files...")
path = "../files" #path name
files= os.listdir(path) #get all the file names
files.remove('.DS_Store')
documents = {}
sortedDocuments=[]
contents=[]
wholeContent=""
for file in files: #go through the folder
    if not os.path.isdir(file): #judge if it is a folder
        if not file=='.DS_Store':
            documents[file]=conv.to_dic(path+"/"+file)
            contents.append(documents[file]['code'])
            wholeContent+=documents[file]['code']

lw.write_info_log("get "+str(len(documents))+" documents")

#indexing
lw.write_info_log("indexing...")
stopwords = ['and', 'edition', 'for', 'in', 'little', 'of', 'the', 'to','print']
pageNum=3
vectorizer = CountVectorizer()
tfidf = TfidfVectorizer()
X = vectorizer.fit_transform([wholeContent]).toarray().T
transformer=TfidfTransformer()
re = tfidf.fit_transform(contents).toarray().T #tf-idf values
word=vectorizer.get_feature_names()#the unique terms after preprocessing
#get query
query = input("Please enter your query: ")

def getDocumentList(query,page):
    sortedDocuments=[]
    #check if the result of this query already exist in the redis
    if not r.exists(query):#if the result is not in the redis
        #store the result of the query into redis
        l=MatrixSearching(query)
        if l is None:
            return None
        lw.write_info_log("storing results into redis in form of list")
        for j in range(len(l)):
            r.rpush(query, l[j])
            if (page-1)*pageNum<j and j<page*pageNum:
                sortedDocuments.append(documents[l[j]])
    #get the result list of this query from redis
    # catch 10 documents at a time
    else:
        lw.write_info_log("geting results from redis")
        i=(page-1)*pageNum
        while i<page*pageNum:
            fileName=r.lindex(query,i)
            print(fileName)
            sortedDocuments.append(documents[fileName])
            i+=1
    r.expire(query, 30)#expire after 30s

    return sortedDocuments#return 10 results


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


def printA(query):
    print('re\n')
    print(re)
    u, s, vt = svd(re, full_matrices=False)
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

    plt.title("LSI Subspace with TF-IDF weight")
    plt.xlabel(u'dimention2')
    plt.ylabel(u'dimention3')

    ut = u.T  # Transaction
    demention2 = ut[1]
    demention3 = ut[2]
    # draw terms
    for i in range(len(demention2)):
        plt.text(demention2[i], demention3[i], word[i])
        plt.plot(demention2[i], demention3[i], '*')  # draw points

    vdemention2 = vt[1]  # we choose the 2nd and 3rd dimensions because the first dimension has little meaning
    vdemention3 = vt[2]
    # get query coordinates
    # get the term frequency
    qFreq = vectorizer.fit_transform([query]).toarray().T  # make the vectorizer fit the query
    qWord = vectorizer.get_feature_names()  # the unique terms after preprocessing
    qArr = np.zeros([1, len(word)])
    # fill in the term frequency into the empty Xq matrix
    for w in qWord:
        i = qWord.index(w)
        if w in word:
            j = word.index(w)
            idf = len(np.nonzero(re[j])[0])
            idf = (1 + len(files)) / (idf + 1)
            idf = math.log2(idf) + 1
            qArr[0][j] = qFreq[i] * idf

    dX = np.dot(np.array(demention2), np.array(qArr))/len(qArr)
    dY = np.dot(np.array(demention3), np.array(qArr))/len(qArr)
    # draw query point
    plt.text(dX, dY, 'QUERY')
    plt.plot(dX, dY, 'ro')
    similarities={}
    for j in range(len(vdemention2)):
        plt.text(vdemention2[j], vdemention3[j], 'T' + str(j))
        plt.plot(vdemention2[j], vdemention3[j], '.')
        # calculate the eclidean distance similarity
        similarity=math.sqrt(math.pow((vdemention2[j]-dX),2)+math.pow((vdemention3[j]-dY),2))
        similarities[files[j]]=similarity
    # sort similarity and print out
    centroidResult = sorted(similarities.keys(),key=similarities.__getitem__,reverse=True)
    return centroidResult


def MatrixSearching(query):
    #svd decomposition
    print('re\n')
    print(re)
    u, s, vt = svd(re, full_matrices=False)
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
    qFreq = vectorizer.fit_transform([query]).toarray().T  # make the vectorizer fit the query
    qWord = vectorizer.get_feature_names()  # the unique terms after preprocessing
    qArr = np.zeros([1, len(word)])
    # fill in the term frequency into the empty Xq matrix
    ifEmpty=True
    for w in qWord:
        i = qWord.index(w)
        if w in word:
            ifEmpty=False
            j = word.index(w)
            idf=len(np.nonzero(re[j])[0])
            idf=(1+len(files))/(idf+1)
            idf=math.log2(idf)+1
            qArr[0][j] = qFreq[i]*idf
    #give the warning and stop searching if no terms found
    if ifEmpty:
        lw.write_warning_log("Nothing found!")
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
        similarities[files[i]]=np.dot(Dq, d[i])/ (np.linalg.norm(Dq) * (np.linalg.norm(d[i])))
    # matrixSimilarity=sorted(similarities.items(),key=lambda item:item[1],reverse=True)
    matrixSimilarity=sorted(similarities.keys(),key=similarities.__getitem__,reverse=True)
    print(matrixSimilarity)
    #turn the id list into sorted document list
    return matrixSimilarity


# printA()
# plt.show()
getDocumentList(query, 2)