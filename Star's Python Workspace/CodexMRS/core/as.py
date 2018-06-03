# coding=utf-8
from CodexMRS.base.network import Server
from CodexMRS.base.network import Client
from CodexMRS.base.configs import config
from CodexMRS.vendor.as_algorithms.LSI.LSI_NLP import LSI_TFIDF as NLP
from CodexMRS.vendor.as_algorithms.LSI.LSI_TFIDF import LSI_TFIDF as LSI
from CodexMRS.vendor.as_algorithms.AST.ASTSearching import ASTSearching
from CodexMRS.vendor.as_algorithms.java_ast.java_AST import JavaAST


def task(message, shared):
    operate_type = message['operate_type']
    timestamp = message['timestamp']
    query = message['query']
    page = message['page']
    result = {}
    # operation 1 LSI
    if operate_type == 1:
        lsi = LSI()
        result = lsi.getResult(query,page)
    # operation 2 nlp
    elif operate_type == 2:
        nlp = NLP()
        result = nlp.getResult(query,page)
    # operation 3 Python AST search
    elif operate_type == 3:
        ast = ASTSearching()
        result = ast.getResults(query,page)
    # operation 4 Java AST search
    elif operate_type == 4:
        ast = JavaAST()
        result = ast.getResults(query, page)
    client = Client(config['recall_ip'], 'AS', config['recall_port'],
                    {'result': result, 'timestamp': timestamp})
    client.send_message()



server = Server(task, public_ip_address="137.43.92.9", port=9609, max_node_num=100)
# server = Server(task, public_ip_address="127.0.0.1", port=9610, max_node_num=100)
server.start_listening()