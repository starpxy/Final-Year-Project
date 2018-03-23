# coding=utf=8
# @author : star
import socket
import threading
import json
import hashlib
from LogWriter import LogWriter
from DF.core import Main_Client


class MainServer:
    __port = 0
    __sk_server = ''
    __max_client_num = 0
    __ip_address = ''
    __thread = ''

    # initialize synchronize server
    def __init__(self, port=9609, max_client_num=3, ip_address='localhost'):
        self.__port = port
        self.__max_client_num = max_client_num
        self.__ip_address = ip_address
        self.__sk_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.__sk_server.bind((self.__ip_address, port))
            self.__sk_server.listen(max_client_num)
        except OSError:
            LogWriter().write_error_log("Port {} is already in use!".format(self.__port))
            exit()
        LogWriter().write_info_log(
            'Main Server will serve at {}:{}, max server number is {}'.format(self.__ip_address, self.__port,
                                                                              self.__max_client_num))

    def __task__(self, connection):
        LogWriter().write_info_log('Running task')
        h = connection.recv(1024)
        h = bytes.decode(h)
        h = h.split('\n')
        header = json.loads(h[0])
        size = header['message_size']
        fingerprint = header['fingerprint']
        p1 = h[1].encode('utf-8')
        size -= len(p1)
        result = p1
        while size > 0:
            temp = connection.recv(1024)
            result += temp
            size -= 1024
        result += connection.recv(1024)

        #   Check Integrity
        m = hashlib.md5()
        m.update(result)
        digest = m.hexdigest()
        if digest == fingerprint:
            print("yes")

    # listen at the port and run tasks
    def start_listen(self):
        while True:
            connection, address = self.__sk_server.accept()
            LogWriter().write_info_log('Server accepted access.')
            connection.settimeout(30)
            self.__thread = threading.Thread(target=self.__task__(connection))
            try:
                self.__thread.start()
            except self.__sk_server.timeout:
                LogWriter().write_warning_log("Time out. Thread automatically closed.")


if __name__ == '__main__':
    MainServer().start_listen()
