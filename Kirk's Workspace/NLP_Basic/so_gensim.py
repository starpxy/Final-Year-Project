
import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')

from gensim import corpora, models, similarities

import os
import pickle
import time
import operator
import json
import FCIConverter
from LogWriter import LogWriter
from NLTK.NLTKFormatter import NLTKFormatter

# from nltk.stem.lancaster import LancasterStemmer

from six import iteritems

lw = LogWriter()

# Start Time
startTime = time.time()

# import io
# import sys
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')

# Read all files from the root path
def ReadFilesDeep(rootDir):
	filePath = []
	fileName = []
	list_dirs = os.walk(rootDir) 
	for root, dirs, files in list_dirs:       
		for f in files:
			if not 'Thumbs' or not '.db' in f:
				filePath.append(os.path.join(root, f))
				fileName.append(f.split(".")[0])
				# fileName.append(f)

	return filePath

# File path for JSON folder
path_json = "C:\\Users\\soapk\\Desktop\\so_all_cleaned"
path_so_pix = "C:\\Users\\soapk\\Desktop\\so_all_cleaned.pik"

# Get all SO JSONs
files = ReadFilesDeep(path_json)

if not os.path.exists(path_so_pix):
	# Preprocessed so question titles, which without stopwords
	so_dict = {}
	so_titles = []

	i = 0
	for i in range(len(files)):
		dict_json = FCIConverter.to_dic(files[i])

		# print(dict_json['project_name'].lower().split())

		# print(dict_json['content'].lower().split())

		# print("")
		temp_dict = {}
		temp_dict["id"] = dict_json["id"]
		# Just for now
		temp_dict["project_name"] = dict_json["project_name"]

		so_dict[i] = temp_dict

		so_titles.append(dict_json['content'].lower().split())

		lw.write_info_log("No. " + str(i) + " reading file: " + temp_dict["id"])

		# print(i)

	# store the index into the pickle
	print('start dumping')
	with open(path_so_pix, 'wb')as f:
		pickle.dump(so_dict, f, True)
		pickle.dump(so_titles, f, True)
		print('finish')
else:
	rfile = open(path_so_pix, 'rb')
	so_dict = pickle.load(rfile)
	so_titles = pickle.load(rfile)




# print(so_dict)
# print(so_titles)

# Preprocessing

# punctuation issue?
#english_punctuations=[',', '.', ':', '?', '(', ')', '[', ']', '&', '!', '*', '@', '#', '$', '%']
# "!\"#$%&()*+,./:;<=>?@[\]^_`{|}~"
#texts_filted=[[word for word in document if word not in english_punctuations]  
			 #  for document in texts_filtered_stopwords] 

#  Stemming?
# st = LancasterStemmer()  
# texts_stemmed = [[st.stem(word) for word in document]  
# 				for document in so_titles]

# print(texts_stemmed)

saved_filename = "so_all_cleaned"

if os.path.exists(os.path.join('C:\\Users\\soapk\\Desktop', saved_filename + ".dict")):
	dictionary = corpora.Dictionary.load(os.path.join('C:\\Users\\soapk\\Desktop', saved_filename + ".dict"))
	
	# with open("C:\\Users\\soapk\\Desktop\\so_dict.txt", 'w', encoding = 'utf-8')as f:
	# 	f.write(str(dictionary.token2id))
	# 	f.write("\n\n")

	# 	for word in dictionary.token2id:
	# 		f.write(word + "\n")
	# 		f.write("tokenid " + str(dictionary.token2id[word]) + "\n")
	# 		f.write("freq " + str(dictionary.dfs[dictionary.token2id[word]]) + "\n")
	# 		f.write("\n")

			

	# # Dict {word : freq}
	# freqDict = {}
	# for word in dictionary.token2id:
	# 	freqDict[word] = dictionary.dfs[dictionary.token2id[word]]
	# 	# print(word)
	# 	# print(dictionary.token2id[word])
	# 	# print(dictionary.dfs[dictionary.token2id[word]])

	# sorted_freqDict = sorted(freqDict.items(), key=operator.itemgetter(1))

	# with open("C:\\Users\\soapk\\Desktop\\so_dict_sorted.txt", 'w', encoding = 'utf-8')as f:
	# 	f.write(json.dumps(sorted_freqDict))

else:
	dictionary = corpora.Dictionary(so_titles)

	print(dictionary)

	once_ids = [tokenid for tokenid, docfreq in iteritems(dictionary.dfs) if docfreq == 1]

	# remove stop words and words that appear only once
	dictionary.filter_tokens(once_ids)

	# remove gaps in id sequence after words that were removed
	dictionary.compactify()
	print(dictionary)

	dictionary.save(os.path.join('C:\\Users\\soapk\\Desktop', saved_filename + ".dict"))


# print(len(dictionary))

if os.path.exists(os.path.join('C:\\Users\\soapk\\Desktop', saved_filename + ".mm")):
	corpus = corpora.MmCorpus(os.path.join('C:\\Users\\soapk\\Desktop', saved_filename + ".mm"))
else:
	corpus = [dictionary.doc2bow(title) for title in so_titles]
	corpora.MmCorpus.serialize(os.path.join('C:\\Users\\soapk\\Desktop', saved_filename + ".mm"), corpus)

tfidf = models.TfidfModel(corpus)

if os.path.exists(os.path.join('C:\\Users\\soapk\\Desktop', saved_filename + ".index")):
	index = similarities.SparseMatrixSimilarity.load(os.path.join('C:\\Users\\soapk\\Desktop', saved_filename + ".index"))
else:	
	corpus_tfidf = tfidf[corpus]

	index = similarities.SparseMatrixSimilarity(corpus_tfidf, num_features = len(dictionary))
	index.save(os.path.join('C:\\Users\\soapk\\Desktop', saved_filename + ".index"))


nltk_formatter = NLTKFormatter()

query = "return error"

print(nltk_formatter.format_sentence(query).split())
print(query.lower().split())

# Ciaran NLTK approach
bow_query = dictionary.doc2bow(nltk_formatter.format_sentence(query).split())

print(bow_query)

# Basic gensim approach
bow_query_basic = dictionary.doc2bow(query.lower().split())
print(bow_query_basic)

# Query
sims = index[tfidf[bow_query]]
# print(sims)
sims = sorted(enumerate(sims), key=lambda item: -item[1])

endTime = time.time()
print(endTime - startTime)

# print("!")
# print(sims)

# lw.write_info_log("Sims Result\n" + str(sims)

with open("C:\\Users\\soapk\\Desktop\\result-" + query + ".txt", 'w', encoding = 'utf-8')as f:
	for i in range(len(sims)):
		so_id = sims[i][0]
		so_sim_score = sims[i][1]
		# print(so_dict[so_id])
		# print(so_dict[so_id]['content'])
		if not so_sim_score == 0:
			# f.write("Search Ranked Result: " + so_dict[so_id]['id'] + "\n")
			f.write("Search Ranked Result: " + so_dict[so_id]['project_name'] + "\n")

		# lw.write_info_log("Search Ranked Result: " + so_dict[so_id]['project_name'])
		# print(so_dict[so_id]['project_name'])

# class SOCorpus(object):
# 	"""docstring for ClassName"""
# 	def __init__(self):
# 		# Log Writter
# 		self.lw = LogWriter()

# 		# File path for JSON folder
# 		self.path_json = "C:\\Users\\soapk\\Desktop\\so"

# 		# Json files list 
# 		# Get all SO JSONs
# 		self.files = ReadFilesDeep(self.path_json)
		

# 	def __iter__(self):
# 		for json in self.files:
# 			dict_json = FCIConverter.to_dic(json)

# 			# assume there's one document per line, tokens separated by whitespace
# 			# TO DO: Stopwords? \ Stemming?
# 			print(dict_json['project_name'])
# 			print(dict_json['project_name'].lower().split())
# 			yield corpora.Dictionary.doc2bow(dict_json['project_name'].lower().split())

# def main():
# 	nlp_corpus = SOCorpus()

# 	for doc in nlp_corpus:
# 		print(doc)

# if __name__ == '__main__':
# 	main()