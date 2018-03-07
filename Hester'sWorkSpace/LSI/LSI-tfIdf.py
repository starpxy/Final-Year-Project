from numpy import zeros
import numpy as np
from scipy.linalg import *
from scipy import spatial
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from Interfaces import FCIConverter as conv
import os

path = "../files" #path name
files= os.listdir(path) #get all the file names
documents = {}
contents=[]
i=0
for file in files: #遍历文件夹
     if not os.path.isdir(file): #判断是否是文件夹，不是文件夹才打开
        documents[i]=conv.to_dic(path+"/"+file)
        contents.append(documents[i]['content'])
        i+=1

stopwords = ['and', 'edition', 'for', 'in', 'little', 'of', 'the', 'to']
ignorechars =":!,"
vectorizer = CountVectorizer()
tfidf = TfidfVectorizer()
X = vectorizer.fit_transform(contents)
transformer=TfidfTransformer()
re = tfidf.fit_transform(contents).toarray().T #tf-idf values
word=vectorizer.get_feature_names()#the unique terms after preprocessing
dic={}#dictionary{term: tf-idf}
tranIgnore = str.maketrans("", "", ignorechars)#ignore the ignorechars
for i in range(len(word)):
    w=word[i]
    if w not in stopwords:
        dic[w]=re[i]
print('dic\n')
print(dic)
dickeys=[]#keys of dic
print(contents)

class LSA(object):
    def __init__(self, stopwords, ignorechars):
        self.stopwords = stopwords
        self.ignorechars = ignorechars
        self.wdict = {}
        self.dcount = 0
        self.dic1={}
        self.dickeys=[]
    def parse(self, doc):
        words = doc.split()
        for w in words:
            w = w.lower().replace("'s", '').translate(tranIgnore)
            if w in self.stopwords:
                continue
            elif w not in word:
                self.dic1[w]=dic[w]#give the words a tf-idf value if it appears in more than one document(when we detect a term not in the word list, it is the second time to appear)
            else:
                word.remove(w) #delete the term from word when this term is found at the first time
        self.dcount += 1

    def build(self):
        self.dickeys=sorted(self.dic1.keys())
        self.A = zeros([len(self.dickeys), len(contents)])#num(terms)*num(documments)
        #construct the matrix A
        index=0
        for i in self.dickeys:
            self.A[index] = self.dic1[i]
            index+=1

    def printA(self):
        print('A\n')
        print (self.A)
        u,s,vt = svd(self.A,full_matrices=False)
        print ("""\r""")
        print('u\n')
        print (u)
        print ("""\r""")
        print('s\n')
        print (s)
        print ("""\r""")
        print('vt\n')
        print (vt)
        print ("""\r""")
        d=vt.T


        plt.title("LSI Subspace with TF-IDF weight")
        plt.xlabel(u'dimention2')
        plt.ylabel(u'dimention3')

        vdemention2 = vt[1]#we choose the 2nd and 3rd dimensions because the first dimension has little meaning
        vdemention3 = vt[2]
        for j in range(len(vdemention2)):
            plt.text(vdemention2[j],vdemention3[j],'T'+str(j))
            plt.plot(vdemention2, vdemention3, '.')

        ut = u.T #Transaction
        demention2 = ut[1]
        demention3 = ut[2]
        #draw terms
        for i in range(len(demention2)):
            plt.text(demention2[i],demention3[i],self.dickeys[i])
            plt.plot(demention2[i], demention3[i], '*')#draw points

        #get query, draw the query point
        qArr=self.getQuery(u,s,d)
        # draw the query point
        dX=np.dot(demention2,qArr)
        dY=np.dot(demention3,qArr)
        plt.text(dX, dY, 'QUERY')
        plt.plot(dX, dY,  'ro')

    def getQuery(self,u,s,d):
        query=input("Please enter your query: ")
        #work out the Xq.T
        qArr=np.zeros([1, 11])
        qWords=query.split()
        for w in qWords:
            if w not in self.stopwords:
                w=w.lower().replace("'s", '').translate(tranIgnore)
                if w in self.dickeys:
                    index=self.dickeys.index(w)
                    qArr[0][index]+=1
        print(qArr)
        sDiagno=np.diag(np.array(s))
        print("sDiago")
        print(sDiagno)
        sInv=np.linalg.inv(sDiagno)
        print("sDiago inverse")
        print(sInv)
        print('u')
        print(u)
        print('qArr  ',np.shape(qArr),'  u  ', np.shape(u),' sInv  ',np.shape(sInv))
        Dq=np.dot(qArr,u)
        Dq=np.dot(Dq,sInv)
        print(Dq)
        similarity={}
        for i in range(len(d)):
            similarity[i]=spatial.distance.cosine(Dq, d[i])
        similarity=sorted(similarity.items(),key=lambda item:item[1])
        for i in range(len(similarity)):
            index=similarity[i][0]
            print(str(similarity[i])+':    '+contents[index])
        return qArr.T

mylsa = LSA(stopwords, ignorechars)
for t in contents:
    mylsa.parse(t)
mylsa.build()
mylsa.printA()
plt.show()