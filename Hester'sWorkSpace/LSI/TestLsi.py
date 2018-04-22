from LSI import LSI_TFIDF as LSI
import time

time_start = time.clock()
lsi=LSI.LSI_TFIDF()
time_end = time.clock()
print("ini: ")
print(time_end-time_start)

# lsi.indexing()

time_start = time.clock()
dList=lsi.getDocumentList("max", 1)
time_end = time.clock()
print("search: ")
print(time_end-time_start)

# time_start = time.clock()
# dList=lsi.getDocumentList("min", 1)
# time_end = time.clock()
# print("search: ")
# print(time_end-time_start)