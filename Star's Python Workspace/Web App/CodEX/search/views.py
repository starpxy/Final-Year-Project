# coding:utf-8
# @author: Star
# @time: 10-03-2018
import search.supportings.FCIConverter
from django.shortcuts import render
from search.supportings.LogWriter import LogWriter
from search.supportings.FormattedCodeInterface import FormattedCodeInterface
from search.supportings.LSI.LSI_TFIDF import LSI_TFIDF
def index(request):
    return render(request, 'index.html')


def search(request):
    q = request.GET['q']
    p = int(request.GET['p'])
    total_p = 20;
    pages = []
    p_p = p - 5
    n_p = p + 5
    while total_p > 0:
        pages.append(0)
        total_p -= 1
    f = [FormattedCodeInterface(project_name="hello", file_name="this.py",
                                content="this is my content,haha And Content balabala"),
         FormattedCodeInterface(project_name="hello", file_name="this.py",
                                content="this is my content,haha And Content balabala"),
         FormattedCodeInterface(project_name="hello", file_name="this.py",
                                content="this is my content,haha And Content balabala"),
         FormattedCodeInterface(project_name="hello", file_name="this.py",
                                content="this is my content,haha And Content balabala"),
         FormattedCodeInterface(project_name="hello", file_name="this.py",
                                content="this is my content,haha And Content balabala")]

    return render(request, 'search-result.html', {'results': f, 'q': q, 'p': p, 'pages': pages, 'p_p': p_p, 'n_p': n_p,'pre':p-1,'next':p+1})


def detail(request):
    return render(request, 'detail.html')
