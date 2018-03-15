# coding:utf-8
# @author: Star
# @time: 10-03-2018
import search.supportings.FCIConverter
from django.shortcuts import render
from django.http import HttpResponse
from search.supportings.LogWriter import LogWriter
from search.supportings.FormattedCodeInterface import FormattedCodeInterface
from search.supportings.LSI.LSI_TFIDF import LSI_TFIDF
from search.supportings.LSI.Results import Results
import math

def index(request):
    return render(request, 'index.html')


def search(request):
    q = request.GET['q']
    p = int(request.GET['p'])
    pages = []
    lsi = LSI_TFIDF()
    result = lsi.getDocumentList(query=q,page=p)
    f = result.getDocumentList()
    total_p = result.getNumOfResults()/10;
    t_p = total_p
    p_p = max(p - 5, 1)
    n_p = min(p + 5, total_p)
    while total_p > 0:
        pages.append(0)
        total_p -= 1
    files = []
    for f_f in f:
        temp = FormattedCodeInterface().from_dictionary(f_f)
        cont = temp.get_content()
        if len(cont)>=400:
            cont = cont[0:399]
            cont+="..."
        temp.set_content(cont)
        files.append(temp)
    return render(request, 'search-result.html', {'results': files, 'q': q, 'p': p, 'pages': pages, 'p_p': p_p, 'n_p': n_p,'pre':p-1,'next':p+1,'t_p':t_p})

def init(request):
    LSI_TFIDF().indexing()
    return HttpResponse("init successfully")
def detail(request):
    return render(request, 'detail.html')
