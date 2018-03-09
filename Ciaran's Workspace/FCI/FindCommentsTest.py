# coding=utf-8
"""
Created on 09/03/2018
Author: Ciarán
"""

import re


def main():
    file = open("C:/Users/CeXGalway/PycharmProjects/Final-Year-Project/Ciaran's Workspace/FCI/FormattedCodeInterface.py")

    content = ''
    comments_list = []
    comments = ''
    python_comments = ['\"\"\"((.|\n)*)\"\"\"', '\'\'\'((.|\n)*)\'\'\'', '#.*']

    for line in file.readlines():
        content += line

    for comment_pattern in python_comments:
        comments_list += re.findall(comment_pattern, content)
        content = re.sub(comment_pattern, '', content)

    for recorded_comment in comments_list:
        if type(recorded_comment) is tuple:
            for comment in recorded_comment:
                comments += comment + '\n'
        else:
            comments += recorded_comment + '\n'
    '''

    code = ''
    comments_list = []
    comments = ''
    python_comments = ['\"\"\"((.|\n)*)\"\"\"', '\'\'\'((.|\n)*)\'\'\'', '#.*']

    for line in file.readlines():
        code += line

    for comment_pattern in python_comments:
        comments_list += re.findall(comment_pattern, code)
        code = re.sub(comment_pattern, '', code)

    for recorded_comment in comments_list:
        if type(recorded_comment) is tuple:
            for comment in recorded_comment:
                comments += comment + '\n'
        else:
            comments += recorded_comment + '\n'
    '''

    print(comments_list)
    print(comments)
    #print(content)


if __name__ == '__main__':
    main()
