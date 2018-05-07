# coding=utf-8
"""
Created on 09/03/2018
Author: Ciarán
"""

import re
import nltk


def test_error_files():
    file = open("Error Files/core.py")
    #file = open("Error Files/registration.py")

    content = ''
    comments_list = []
    comments = ''
    python_comments = ['\"\"\"((.|\n)*)\"\"\"', '\'\'\'((.|\n)*)\'\'\'', '(?<!(\"|\'))#.*(?=\n)']

    # Content
    for line in file.readlines():
        content += line

    #content = "\"\"\"The main OpenAI Gym class. It encapsulates an environment with\narbitrary behind-the-scenes dynamics. An environment can be\npartially or fully observed.\n\"\"\"\ndef reset(self):\n\"\"\"Resets the state of the environment and returns an initial observation.\nReturns: observation (object): the initial observation of the\nspace.\n\"\"\"\nraise NotImplementedError"

    # Code
    code = content
    for comment_pattern in python_comments:
        for match in re.finditer(comment_pattern, code):
            formatted_comment = format_comments(match.group(0))
            comments_list.append(formatted_comment)
            try:
                code = re.sub(match.group(0), '', code)
            except Exception as e:
                print(e)

    # Comments
    comments = ' '.join(comments_list)


def format_comments(comment):
    formatted_comment = ''
    alnum_pattern = r'[^(a-zA-Z0-9)]'
    stopwords = set(nltk.corpus.stopwords.words('english'))

    comment = re.sub(alnum_pattern, ' ', comment)

    for word in comment.split(' '):
        if word.lower() not in stopwords:
            formatted_comment += str(word.lower()) + ' '

    return formatted_comment


def main():
    test_error_files()


if __name__ == '__main__':
    main()
