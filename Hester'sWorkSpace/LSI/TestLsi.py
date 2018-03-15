from LSI import LSI_TFIDF as LSI
lsi=LSI.LSI_TFIDF()
# lsi.indexing()
dList=lsi.getDocumentList("common", 1)
print(dList)