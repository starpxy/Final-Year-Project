# coding=utf-8
"""
Created on 08/05/2018
Author: Ciarán
"""

import nltk
from nltk.corpus import wordnet


class NLTKFormatter:

    def __init__(self):
        self.stopwords = set(nltk.corpus.stopwords.words('english'))

    def format_sentence(self, sentence):
        tokenised_sentence = nltk.word_tokenize(sentence.lower())

        sentence_no_stopwords = []
        for word in tokenised_sentence:
            if (word not in self.stopwords) and (len(word) > 2):
                sentence_no_stopwords.append(word)

        sentence_no_stopwords = ' '.join(sentence_no_stopwords)

        return sentence_no_stopwords

        '''
        sentences = nltk.sent_tokenize(sentence)
        sentences = [nltk.word_tokenize(sent) for sent in sentences]
        sentences = [nltk.pos_tag(sent) for sent in sentences]

        synonyms = []
        synonym_list = ()
        for word in tokenised_sentence:
            for synonym in wordnet.synsets(word):
                synonym_list += synonym

        synonyms.append(synonym_list)
        '''


def main():
    nltk_formatter = NLTKFormatter()
    formatted_sentence = nltk_formatter.format_sentence("Is it possible to do mathematics inside CSS?")
    print(formatted_sentence)


if __name__ == '__main__':
    main()