# coding=utf-8
"""
Created on 13/03/2018
Author: Ciarán
"""

import nltk
#from nltk.book import *
from nltk.corpus import stopwords


def test():
    '''sentence = "At eight o'clock on Thursday morning"
    tokens = nltk.word_tokenize(sentence)
    print(tokens)
    tagged = nltk.pos_tag(tokens)
    print(tagged[0:6])
    print(text1)'''


def stopwords_test():

    description = "youtube-dl is a command-line program to download videos from YouTube.com and a few more sites. " \
                  "It requires the Python interpreter, version 2.6, 2.7, or 3.2+, and it is not platform specific. " \
                  "It should work on your Unix box, on Windows or on macOS. It is released to the public domain, " \
                  "which means you can modify it, redistribute it or use it however you like."
    print(description).
    tokenised_description = nltk.word_tokenize(description.lower())
    stopwords = set(nltk.corpus.stopwords.words('english'))
    #description_no_stopwords = [w for w in description if w.lower() not in stopwords]
    #print(description_no_stopwords)
    #tokens = nltk.word_tokenize(description_no_stopwords)

    filtered_text = []
    for word in tokenised_description:
        if (word not in stopwords) and (len(word) > 2):
            filtered_text.append(word)

    print(filtered_text)

    new_description = ' '.join(filtered_text)
    print(new_description)

    #tagged = nltk.pos_tag(tokens)
    #print(tagged[:])
    #print(sorted(stopwords.words('english')))


def main():
    #test()
    stopwords_test()


if __name__ == '__main__':
    main()
