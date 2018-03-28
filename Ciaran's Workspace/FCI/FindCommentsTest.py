# coding=utf-8
"""
Created on 09/03/2018
Author: Ciarán
"""

import re


def test_error():
    code = [" # for If-Modified-Since (because IMS does not otherwise\n",
            "g# TODO: 304 responses SHOULD return the same etag that a full\n",
            "\"# response would.  We currently do for If-None-Match, but not\"\n",
            " #!/usr/bin/env python\n",
            "# require us to read the file from disk)\n"]
    code1 = ''

    for code_piece in code:
        code1 += code_piece

    p = r'(?<!(\"|\'))#.*(?=\n)'
    matches = re.finditer(p, code1)
    results1 = [match.group(0)
               for match in matches]
    print(results1)

    for comment in results1:
        code = re.sub(comment, '', code1)


def set_content():
    comments_list = []
    python_comments = ['\"\"\"((.|\n)*)\"\"\"', '\'\'\'((.|\n)*)\'\'\'', '(?<!(\"|\'))#.*']
    python_ignore_comments = ['[^\"]\"(([^\"]|\n)+)\"[^\"]', '[^\']\'(([^\']|\n)+)\'[^\']']

    # Code
    code = [" # for If-Modified-Since (because IMS does not otherwise\n",
            "g# TODO: 304 responses SHOULD return the same etag that a full\n",
            "\"# response would.  We currently do for If-None-Match, but not\"\n",
            " #!/usr/bin/env python\n",
            "# require us to read the file from disk)\n"]
    code1 = ''

    for code_piece in code:
        code1 += code_piece

    print(code1)

    p1 = r'(?<!(\"|\'))#.*(?=\n)'
    p2 = r'[^(\"|\')]#.*(?=\n)'
    matches1 = re.finditer(p1, code1)
    matches3 = re.finditer(p2, code1)
    matches2 = re.findall(p1, code1)
    matches4 = re.findall(p2, code1)
    for match in matches1:
        print(match.group(0))
    results1 = [match.group(2)
               for match in matches1]
    #results2 = [match.group(1)
               #for match in matches3]
    print(results1)
    #print(results2)
    print(matches2)
    print(matches4)

    #for i in results:
       # print(i.start(1), i.end(1))


    '''pattern = re.compile(p)
    clist1 = pattern.search(code1)
    #clist2 = re.findall(p, code1, overlapped=True)
    #clist2 = re.findall(comment_pattern, code1)
    #clist2 = pattern.findall(code1)
    print(clist1)
    print(clist2)

    for comment_pattern in python_comments:
        pattern = re.compile(comment_pattern)
        clist1 = pattern.search(code1)
        #clist2 = re.findall(comment_pattern, code1)
        clist2 = pattern.findall(code1)
        print(clist1)
        print(clist2)'''

    '''for comment_pattern in python_comments:
        for comment in re.findall(comment_pattern, code):
            print(comment)
            for ignore_comment_pattern in python_ignore_comments:
                if re.match(ignore_comment_pattern, comment) is None:
                    comments_list += comment
                    code = re.sub(comment, '', code)'''


def old_test():
    file = open("C:/Users/CeXGalway/PycharmProjects/Final-Year-Project/Ciaran's Workspace/FCI/FormattedCodeInterface.py")

    content = ''
    comments_list = []
    comments = ''
    python_comments = ['\"\"\"((.|\n)*)\"\"\"', '\'\'\'((.|\n)*)\'\'\'', '(?<!(\"|\'))#.*']

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


def main():
    test_error()


if __name__ == '__main__':
    main()
