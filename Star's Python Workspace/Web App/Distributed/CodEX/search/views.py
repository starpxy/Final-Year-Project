# coding:utf-8
# @author: Star
# @time: 10-03-2018
import json
import hashlib
import redis
import time
from CodEX.config import configs
import search.supportings.FCIConverter as fci
from django.views.decorators.csrf import csrf_exempt
from search.supportings.java_ast.java_AST import JavaAST
from django.shortcuts import render
from django.http import HttpResponse
from search.supportings.LSI.LSI_TFIDF import LSI_TFIDF
from search.supportings.LSI.LSI_NLP import LSI_TFIDF as NLP_LSI_TFIDF
import CodEX.config as config
from search.supportings.FrontEndInterface import FrontEndInterface
from search.supportings.AST.ASTSearching import ASTSearching


def index(request):
    return render(request, 'index.html')


def task(message, shared):
    print(message)


def search(request):
    q = request.GET['q']
    p = int(request.GET['p'])
    # timestamp = time.time()
    # client = Client("yeats.ucd.ie", "10.141.131.14", 9609,
    #                 {'operate_type': 1, 'query': q, 'page': p, 'timestamp': timestamp})
    # client.send_message()
    # server = Server(task, '10.141.131.14')
    # message = server.listen_once().get_message_body()
    # message = json.loads(message)
    # server = CommunicationServer()
    # message = server.receive_message(socket_name=str(timestamp))
    # result = message['result']
    tfidf = LSI_TFIDF()
    result = tfidf.getResult(query=q, page=p)
    pages = []
    f = result[1]
    total_p = (result[0] / configs['others']['page_num']) + 1
    t_p = int(total_p)
    p_p = max(p - 5, 1)
    n_p = min(p + 5, total_p)
    while total_p > 0:
        pages.append(0)
        total_p -= 1
    files = []
    for f_f in f:
        f_name = f_f[0]
        temp = fci.to_fciObject(config.configs['paths']['FCI_path'] + "/lsi/" + f_name)
        m_l = ''
        for t_f_f in f_f[1]:
            m_l += str(t_f_f + 1)
            m_l += ','
        m_l = m_l[0:len(m_l) - 1]
        fei = FrontEndInterface(temp, m_l)
        files.append(fei)
    return render(request, 'search-result.html',
                  {'results': files, 'q': q, 'p': p, 'pages': pages, 'p_p': p_p, 'n_p': n_p, 'pre': p - 1,
                   'next': p + 1, 't_p': t_p})


def init(request):
    return HttpResponse("init successfully")


def plagiarize(request):
    return render(request, 'snippet.html', {})


def nlsindex(request):
    return render(request, 'nls.html', {})


def nls_result(request):
    q = request.GET['q']
    p = int(request.GET['p'])
    tfidf = NLP_LSI_TFIDF()
    result = tfidf.getResult(query=q, page=p)
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
        f_name = f_f[0]
        temp = fci.to_fciObject(config.configs['paths']['FCI_path'] + "/so/" + f_name)
        m_l = ''
        for t_f_f in f_f[1]:
            m_l += str(t_f_f + 1)
            m_l += ','
        m_l = m_l[0:len(m_l) - 1]
        fei = FrontEndInterface(temp, m_l)
        files.append(fei)
    return render(request, 'nlp-result.html',
                  {'results': files, 'q': q, 'p': p, 'pages': pages, 'p_p': p_p, 'n_p': n_p, 'pre': p - 1,
                   'next': p + 1, 't_p': t_p})


@csrf_exempt
def plagiarizeResult(request):
    snippet = request.POST['snippet']
    page = int(request.POST['p'])
    operate_type = request.POST['l']
    timestamp = time.time()
    m = hashlib.md5()
    m.update((str(timestamp)+snippet).encode("utf8"))
    ts = m.hexdigest()
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    r.set(ts, snippet, ex=3000)
    operate_type = int(operate_type)
    # timestamp = time.time()
    # client = Client("yeats.ucd.ie", "10.141.131.14", 9609,
    #                 {'operate_type': operate_type, 'query': snippet, 'page': page, 'timestamp': timestamp})
    # client.send_message()
    # server = CommunicationServer()
    # message = server.receive_message(socket_name=str(timestamp))
    # result = message['result']
    ast = None
    language = ''
    if operate_type == 3:
        ast = ASTSearching()
        language = 'python'
    else:
        ast = JavaAST()
        language = 'java'
    result = ast.getResults(snippet, page)
    if result == 0:
        return render(request, 'snippet-result.html',
                      {'snippet': snippet, })
    else:
        result = result.to_dict()
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
        matching_lines = result['matchingLines']
        blockWeights = result['blockWeights']
        if global_similarity != None and global_similarity > 0:
            is_global = True
            cd = result['componentDocuments']
            component_document = []
            for c in cd:
                qml = str(matching_blocks[c][0]) + '-' + str(matching_blocks[c][1])
                ml=''
                for mls in matching_lines[c]:
                    ml += str(mls[2]) + '-' + str(mls[3]) + ','
                print(qml)
                fobj = fci.to_fciObject(config.configs['paths']['FCI_path'] + "/" + language + "/" + c)
                fei = FrontEndInterface(fobj, ml)
                fei.set_query_match_lines(qml)
                print(fei.get_query_match_lines(),'==========')
                component_document.append(fei)
        for t in result['plagiarismList']:
            ml = ''
            qml = ''
            for mls in matching_lines[t]:
                qml += str(mls[0]) + '-' + str(mls[1]) + ','
                ml += str(mls[2]) + '-' + str(mls[3]) + ','
            fobj = fci.to_fciObject(config.configs['paths']['FCI_path'] + "/" + language + "/" + t)
            fei = FrontEndInterface(fobj, ml)
            fei.set_query_match_lines(qml)
            plagiarize_list.append(fei)
        for t in result['documentList']:
            ml = ''
            qml = ''
            for mls in matching_lines[t]:
                qml += str(mls[0]) + '-' + str(mls[1]) + ','
                ml += str(mls[2]) + '-' + str(mls[3]) + ','
            fobj = fci.to_fciObject(config.configs['paths']['FCI_path'] + "/" + language + "/" + t)
            fei = FrontEndInterface(fobj, ml)
            fei.set_query_match_lines(qml)
            document_list.append(fei)
        if global_similarity != None:
            global_similarity *= 100
            global_similarity = '%.2f' % global_similarity
    return render(request, 'snippet-result.html',
                  {'snippet': snippet, "is_global": is_global, 'component_documents': component_document,
                   "global_similarity": global_similarity, "plagiarize_list": plagiarize_list,
                   "document_list": document_list, "l": operate_type, 'ts': ts})


def snippet_detail(request):
    id = request.GET['id']
    ml = request.GET['ml']
    qml = request.GET['qml']
    timestamp = request.GET['ts']
    l = int(request.GET['l'])
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    q = r.get(timestamp)
    language = ''
    print(l)
    if l == 3:
        language = 'python'
    else:
        language = 'java'
    m_l = ml
    fci_obj = fci.to_fciObject(config.configs['paths']['FCI_path'] + "/" + language + "/" + id + '.json')
    return render(request, 'snippet-detail.html',
                  {'detail': fci_obj, 'match_lines': m_l, 'query_match_lines': qml, 'query': q})


def detail(request):
    id = request.GET['id']
    ml = request.GET['ml']
    m_l = ml
    fci_obj = fci.to_fciObject(config.configs['paths']['FCI_path'] + "/lsi/" + id + '.json')
    return render(request, 'detail.html', {'detail': fci_obj, 'match_lines': m_l})
