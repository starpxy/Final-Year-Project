from scipy.linalg import *
from scipy.sparse.linalg import svds
from scipy import spatial
from scipy.sparse import dok_matrix
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer,CountVectorizer
import numpy as np
titles = [
    "The Neatest Little Guide to Stock Market Investing",
    "Investing For Dummies, 4th Edition",
    "The Little Book of Common Sense Investing: The Only Way to Guarantee Your Fair Share of Stock Market Returns",
    "The Little Book of Value Investing",
    "Value Investing: From Graham to Buffett and Beyond",
    "Rich Dad's Guide to Investing: What the Rich Invest in, That the Poor and the Middle Class Do Not!",
    "Investing in Real Estate, 5th Edition",
    "Stock Investing For Dummies",
    "Rich Dad's Advisors: The ABC's of Real Estate Investing: The Secrets of Finding Hidden Profits Most Investors Miss",
    "The Neatest Little Guide to Stock Market Investing",
    "Investing in Real Estate, 5th Edition"
]


def MatrixSearching(query):
    tfidf = TfidfVectorizer()
    vectorizer = CountVectorizer()
    re = tfidf.fit_transform(titles).toarray().T
    idf = tfidf.idf_
    word = tfidf.vocabulary_
    word = sorted(word, key=word.get)
    # print(re)
    # scipy svd
    re = dok_matrix(re)
    u, s, d = svds(re, k=4, return_singular_vectors='u')
    # print(u)
    print(s)
    sDiagno = np.diag(np.array(s))
    print(sDiagno)
    sInv = np.linalg.inv(sDiagno)
    print(sInv)
    qFreq = vectorizer.fit_transform([query]).toarray().T  # make the vectorizer fit the query
    qWord = vectorizer.get_feature_names()  # the unique terms after preprocessing
    qArr = np.zeros([1, len(word)])
    print(qArr.shape)
    j = 0
    for w in qWord:
        i=qWord.index(w)
        if w in word:
            j = word.index(w)
            qArr[0][j] = qFreq[i] * idf[j]
    print(qArr)
    sDiagno = np.diag(np.array(s))
    print(sDiagno)
    sInv = np.linalg.inv(sDiagno)
    Dq = np.dot(qArr, u)
    Dq = np.dot(Dq, sInv)
    d = d.T
    print(d)
    # print(Dq)
    # similarities from Dq=X.T * T * S-1.
    similarities = {}
    for i in range(len(d)):
        # similarities[titles[i]] = round((np.dot(Dq, d[i]) / (np.linalg.norm(Dq) * (np.linalg.norm(d[i]))))[0], 8)
        # similarity = round(spatial.distance.cosine(Dq, d[i]), 8)
        similarity=((np.dot(Dq, d[i])) / ((np.linalg.norm(Dq)) * (np.linalg.norm(d[i]))))[0]
        if similarity > 0:
            similarities[titles[i]] = similarity
    print(Dq)
    # matrixSimilarity=sorted(similarities.items(),key=lambda item:item[1],reverse=True)
    keys = sorted(similarities, key=similarities.get, reverse=True)[0: 50]
    # machingLines=self.highlighting(ocurrence,qWord,keys)
    i = 0
    for k in keys:
        print(k)
        print(similarities[k])
        # print(machingLines[i](1))
        i += 1
    # turn the id list into sorted document list

MatrixSearching('Value')