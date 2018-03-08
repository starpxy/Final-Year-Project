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
wholeContent=""
i=0
for file in files: #go through the folder
     if not os.path.isdir(file): #judge if it is a folder
        documents[i]=conv.to_dic(path+"/"+file)
        contents.append(documents[i]['content'])
        wholeContent+=documents[i]['content']
        i+=1

stopwords = ['and', 'edition', 'for', 'in', 'little', 'of', 'the', 'to','print']
ignorechars =":!,"
vectorizer = CountVectorizer()
tfidf = TfidfVectorizer()
X = vectorizer.fit_transform([wholeContent]).toarray().T
transformer=TfidfTransformer()
re = tfidf.fit_transform(contents).toarray().T #tf-idf values
word=vectorizer.get_feature_names()#the unique terms after preprocessing
print(re.shape)
i=0
#throw away the low-frequency terms (terms appears only once)
while True:
    if i>=len(word):
        break
    if X[i]<2:
        word.pop(i)
        X=np.delete(X,i,0)
        re=np.delete(re,i,0)
    else:
        i+=1

print(re.shape)

class LSA(object):
    def __init__(self, stopwords, ignorechars):
        self.stopwords = stopwords

    def printA(self):
        print('re\n')
        print (re)
        u,s,vt = svd(re,full_matrices=False)
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

        ut = u.T  # Transaction
        demention2 = ut[1]
        demention3 = ut[2]
        # draw terms
        for i in range(len(demention2)):
            plt.text(demention2[i], demention3[i], word[i])
            plt.plot(demention2[i], demention3[i], '*')  # draw points

        vdemention2 = vt[1]#we choose the 2nd and 3rd dimensions because the first dimension has little meaning
        vdemention3 = vt[2]
        #get query coordinates
        qArr=self.getQuery(u,s,d)
        dX=np.dot(demention2,qArr)
        dY=np.dot(demention3,qArr)
        #draw query point
        plt.text(dX, dY, 'QUERY')
        plt.plot(dX, dY,  'ro')
        euclideanSimilarity={}
        for j in range(len(vdemention2)):
            plt.text(vdemention2[j],vdemention3[j],'T'+str(j))
            plt.plot(vdemention2, vdemention3, '.')
            #calculate the eclidean distance similarity
            euclideanSimilarity[j]=np.linalg.norm(np.array([vdemention2[j],vdemention3[j]])-np.array([dX,dY]))

        #sort similarity and print out
        euclidianSimilarity = sorted(euclideanSimilarity.items(), key=lambda item: item[1])
        for i in range(len(euclidianSimilarity)):
            index = euclidianSimilarity[i][0]
            print(str(euclidianSimilarity[i]) + ':    ' + files[index])



    def getQuery(self,u,s,d):
        query=input("Please enter your query: ")
        #work out the Xq.T
        #get the term frequency
        qFreq = vectorizer.fit_transform([query]).toarray().T#make the vectorizer fit the query
        qWord=vectorizer.get_feature_names()#the unique terms after preprocessing
        qArr=np.zeros([1, len(word)])
        #fill in the term frequency into the empty Xq matrix
        for w in qWord:
            i=qWord.index(w)
            if w in word:
                j=word.index(w)
                qArr[0][j]=qFreq[i]

        print(qArr)
        sDiagno=np.diag(np.array(s))
        sInv=np.linalg.inv(sDiagno)
        print("sDiago inverse")
        print(sInv)
        print('u')
        print(u)
        print('qArr  ',np.shape(qArr),'  u  ', np.shape(u),' sInv  ',np.shape(sInv))
        Dq=np.dot(qArr,u)
        Dq=np.dot(Dq,sInv)
        print(Dq)
        #similarities from Dq=X.T * T * S-1.
        # similarity={}
        # for i in range(len(d)):
        #     similarity[i]=spatial.distance.cosine(Dq, d[i])
        # similarity=sorted(similarity.items(),key=lambda item:item[1])
        # for i in range(len(similarity)):
        #     index=similarity[i][0]
        #     print(str(similarity[i])+':    '+files[index])
        return qArr.T

mylsa = LSA(stopwords, ignorechars)
mylsa.printA()
plt.show()