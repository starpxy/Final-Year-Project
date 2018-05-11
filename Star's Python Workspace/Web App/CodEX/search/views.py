# coding:utf-8
# @author: Star
# @time: 10-03-2018
import json
import time
import search.supportings.FCIConverter as fci
from search.supportings.network import Server
from search.supportings.communicator import CommunicationServer
from search.supportings.network import Client
from django.shortcuts import render
from django.http import HttpResponse
from search.supportings.LSI.LSI_TFIDF import LSI_TFIDF
import CodEX.config as config
from search.supportings.FrontEndInterface import FrontEndInterface
from search.supportings.AST.ASTSearching import ASTSearching


def index(request):
    return render(request, 'index-sub.html')


def task(message, shared):
    print(message)


def search(request):
    q = request.GET['q']
    p = int(request.GET['p'])
    timestamp = time.time()
    client = Client("yeats.ucd.ie", "10.141.131.14", 9609,
                    {'operate_type': 1, 'query': q, 'page': p, 'timestamp': timestamp})
    client.send_message()
    # server = Server(task, '10.141.131.14')
    # message = server.listen_once().get_message_body()
    # message = json.loads(message)
    server = CommunicationServer()
    message = server.receive_message(socket_name=str(timestamp))
    result = message['result']
    pages = []
    f = result[1]
    total_p = (result[0] / 10) + 1
    t_p = int(total_p)
    p_p = max(p - 5, 1)
    n_p = min(p + 5, total_p)
    while total_p > 0:
        pages.append(0)
        total_p -= 1
    files = []
    for f_f in f:
        f_name = f_f[0][0]
        temp = fci.to_fciObject(config.configs['paths']['FCI_path'] + "/" + f_name)
        m_l = ''
        for t_f_f in f_f[0][1]:
            m_l += str(t_f_f + 1)
            m_l += ','
        m_l = m_l[0:len(m_l) - 1]
        fei = FrontEndInterface(temp, m_l)
        files.append(fei)
    return render(request, 'search-result-sub.html',
                  {'results': files, 'q': q, 'p': p, 'pages': pages, 'p_p': p_p, 'n_p': n_p, 'pre': p - 1,
                   'next': p + 1, 't_p': t_p})


def init(request):
    return HttpResponse("init successfully")


def plagiarize(request):
    return render(request, 'snippet.html', {})


def nlsindex(request):
    return render(request, 'nls.html', {})


def plagiarizeResult(request):
    snippet = request.GET['snippet']
    page = int(request.GET['p'])
    operate_type = request.GET['l']
    operate_type = int(operate_type)
    timestamp = time.time()
    client = Client("yeats.ucd.ie", "10.141.131.14", 9609,
                    {'operate_type': operate_type, 'query': snippet, 'page': page, 'timestamp': timestamp})
    client.send_message()
    server = CommunicationServer()
    message = server.receive_message(socket_name=str(timestamp))
    result = message['result']
    is_global = False
    plagiarize_list = []
    document_list = []
    component_document = []
    global_similarity = 0
    if result != None:
        total_num = result['numOfResults']
        total_page = (total_num / config.configs['others']['page_num']) + 1
        matching_blocks = result['matchingBlocks']
        global_similarity = result['globalSimilarity']
        if global_similarity != None and global_similarity > 0:
            is_global = True
            cd = result['componentDocuments']
            component_document = []
            for c in cd:
                ml = str(matching_blocks[c][0]) + '-' + str(matching_blocks[c][1])
                fobj = fci.to_fciObject(config.configs['paths']['FCI_path'] + "/" + c)
                component_document.append(FrontEndInterface(fobj, ml))
        matching_lines = result['matchingLines']

        for t in result['plagiarismList']:
            ml = ''
            for mls in matching_lines[t]:
                ml += str(mls[0]) + '-' + str(mls[1]) + ','
            fobj = fci.to_fciObject(config.configs['paths']['FCI_path'] + "/" + t)
            plagiarize_list.append(FrontEndInterface(fobj, ml))
        for t in result['documentList']:
            ml = ''
            for mls in matching_lines[t]:
                ml += str(mls[0]) + '-' + str(mls[1]) + ','
            fobj = fci.to_fciObject(config.configs['paths']['FCI_path'] + "/" + t)
            document_list.append(FrontEndInterface(fobj, ml))
    return render(request, 'snippet-result.html',
                  {'snippet': snippet, "is_global": is_global, 'component_documents': component_document,
                   "global_similarity": global_similarity, "plagiarize_list": plagiarize_list,
                   "document_list": document_list})


def detail(request):
    id = request.GET['id']
    ml = request.GET['ml']
    m_l = ml
    fci_obj = fci.to_fciObject(config.configs['paths']['FCI_path'] + "/" + id + '.json')
    return render(request, 'detail-sub.html', {'detail': fci_obj, 'match_lines': m_l})
