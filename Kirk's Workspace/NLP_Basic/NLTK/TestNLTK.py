# coding=utf-8
"""
Created on 13/03/2018
Author: Ciarán
"""

import nltk
from nltk.corpus import wordnet
from nltk.corpus import ieer
#from nltk.book import *
from nltk.corpus import stopwords


def test():
    '''sentence = "At eight o'clock on Thursday morning"
    tokens = nltk.word_tokenize(sentence)
    print(tokens)
    tagged = nltk.pos_tag(tokens)
    print(tagged[0:6])
    print(text1)'''


def extraction_test():
    document = "The fourth Wells account moving to another agency is the packaged paper-products division of " \
               "Georgia-Pacific Corp., which arrived at Wells only last fall. Like Hertz and the History Channel, " \
               "it is also leaving for an Omnicom-owned agency, the BBDO South unit of BBDO Worldwide. BBDO South " \
               "in Atlanta, which handles corporate advertising for Georgia-Pacific, will assume additional duties " \
               "for brands like Angel Soft toilet tissue and Sparkle paper towels, said Ken Haldin, a spokesman for " \
               "Georgia-Pacific in Atlanta."
    so_questions = ["Remove ✅, 🔥, ✈ , ♛ and other such emojis/images/signs from Java string", "Is final ill-defined?",
                    "For loop inside its own curly braces", "Does 'finally' always execute in Python?",
                    "Is it possible to \"hack\" python's print function?"]
    so_filtered_questions =[]

    stopwords = set(nltk.corpus.stopwords.words('english'))
    for question in so_questions:
        tokenised_description = nltk.word_tokenize(question.lower())

        question_no_stopwords = []
        for word in tokenised_description:
            if (word not in stopwords) and (len(word) > 2):
                question_no_stopwords.append(word)

        question_no_stopwords = ' '.join(question_no_stopwords)
        so_filtered_questions.append(question_no_stopwords)

    for question in so_filtered_questions:
        print(question)
        sentences = nltk.sent_tokenize(question)
        sentences = [nltk.word_tokenize(sent) for sent in sentences]
        sentences = [nltk.pos_tag(sent) for sent in sentences]
        print(sentences)

    synonyms = []
    for question in so_filtered_questions:
        tokenised_description = nltk.word_tokenize(question.lower())
        synonym_list = ()

        for word in tokenised_description:
            for synonym in wordnet.synsets(word):
                print(synonym)
                synonym_list += synonym

        synonyms.append(synonym_list)

    for list in synonyms:
        print(list)



def stopwords_test():

    description = "youtube-dl is a command-line program to download videos from YouTube.com and a few more sites. " \
                  "It requires the Python interpreter, version 2.6, 2.7, or 3.2+, and it is not platform specific. " \
                  "It should work on your Unix box, on Windows or on macOS. It is released to the public domain, " \
                  "which means you can modify it, redistribute it or use it however you like."
    #print(description).
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
    #stopwords_test()
    extraction_test()


if __name__ == '__main__':
    main()
