from numpy import zeros
import numpy as np
from scipy.linalg import *
from scipy import spatial
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
import math

titles = [
    "The Neatest Little Guide to Stock Market Investing",
    "Investing For Dummies, 4th Edition",
    "The Little Book of Common Sense Investing: The Only Way to Guarantee Your Fair Share of Stock Market Returns",
    "The Little Book of Value Investing",
    "Value Investing: From Graham to Buffett and Beyond",
    "Rich Dad's Guide to Investing: What the Rich Invest in, That the Poor and the Middle Class Do Not!",
    "Investing in Real Estate, 5th Edition",
    "Stock Investing For Dummies",
    "Rich Dad's Advisors: The ABC's of Real Estate Investing: The Secrets of Finding Hidden Profits Most Investors Miss"
]
stopwords = ['and', 'edition', 'for', 'in', 'little', 'of', 'the', 'to']
ignorechars =":!,"
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(titles)
word=vectorizer.get_feature_names()
tfidf = TfidfVectorizer()
re = tfidf.fit_transform(titles).toarray().T
dic={}
tranIgnore = str.maketrans("", "", ignorechars)
for i in range(len(word)):
    w=word[i]
    if w not in stopwords:
        dic[w]=re[i]
print('dic\n')
print(dic)
dickeys=[]

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
        for word in words:
            #print self.dcount
            w = word.lower().replace("'s", '').translate(tranIgnore)
            if w in self.stopwords:
                continue
            elif w in self.wdict:
                self.wdict[w].append(self.dcount)
                self.dic1[w]=dic[w]#copy the words appearing in more than one document
            else:
                self.wdict[w] = [self.dcount]
        self.dcount += 1

    def build(self):
        # self.keys = [k for k in self.wdict.keys() if len(self.wdict[k]) > 1]
        # self.keys.sort()
        # self.A = zeros([len(self.keys), self.dcount])
        # for i, k in enumerate(self.keys):
        #     for d in self.wdict[k]:
        #         self.A[i,d] += 1
        # dic1.keys = [k for k in self.wdict.keys() if len(self.wdict[k]) > 1]
        self.dickeys=sorted(self.dic1.keys())
        print('--------------------------')
        print(self.dickeys)
        self.A = zeros([len(self.dickeys), self.dcount])
        index=0
        for i in self.dickeys:
            self.A[index] = self.dic1[i]
            index+=1
        return self.A

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

        self.getQuery(u,s,d)

        plt.title("LSI Subspace with TF-IDF weight")
        plt.xlabel(u'dimention2')
        plt.ylabel(u'dimention3')

        titles = ['T1','T2','T3','T4','T5','T6','T7','T8','T9']
        vdemention2 = vt[1]
        vdemention3 = vt[2]
        for j in range(len(vdemention2)):
            plt.text(vdemention2[j],vdemention3[j],titles[j])
            plt.plot(vdemention2, vdemention3, '.')

        ut = u.T #Transaction
        demention2 = ut[1]
        demention3 = ut[2]
        for i in range(len(demention2)):
            plt.text(demention2[i],demention3[i],self.dickeys[i])
            plt.plot(demention2[i], demention3[i], '*')#draw points
            #get query, draw the query point

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
        i=0
        for i in range(len(d)):
            similarity[i]=spatial.distance.cosine(Dq, d[i])
        similarity=sorted(similarity.items(),key=lambda item:item[1])
        print(similarity)
        # for key in similarity.keys():
        #     print('doc '+str(key)+': '+str(similarity[key]))

mylsa = LSA(stopwords, ignorechars)
for t in titles:
    mylsa.parse(t)
mylsa.build()
mylsa.printA()
plt.show()