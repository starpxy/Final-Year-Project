# coding=utf-8
from CodexMRS.base.network import Server
from CodexMRS.vendor.as_algorithms.AST.ASTSearching import ASTSearching
from CodexMRS.vendor.as_algorithms.java_ast.java_AST import JavaAST


def task(message, ):
    print()

server = Server(task, public_ip_address="137.43.92.9", port=9609, max_node_num=100)