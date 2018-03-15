# coding=utf-8
"""
Created on 13/03/2018
Author: Ciarán
"""

import nltk
from nltk.book import *


def main():
    sentence = "At eight o'clock on Thursday morning"
    tokens = nltk.word_tokenize(sentence)
    print(tokens)
    tagged = nltk.pos_tag(tokens)
    print(tagged[0:6])
    print(text1)


if __name__ == '__main__':
    main()
