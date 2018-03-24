# coding=utf=8
# @author : star
import socket
import threading
import hashlib
import json
from LogWriter import LogWriter
from DF.core.Task import Task


class Server:
    __port = 0
    __sk_server = ''
    __max_client_num = 0
    __ip_address = ''
    __thread = ''
    __other_server = []

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
            print("Port {} is already in use!".format(self.__port))
            exit()
        LogWriter().write_info_log(
            'Server will serve at {}:{}, max server number is {}'.format(self.__ip_address, self.__port,
                                                                         self.__max_client_num))
        print('Server will serve at {}:{}, max server number is {}'.format(self.__ip_address, self.__port,
                                                                           self.__max_client_num))

    def __execute__(self, connection, address):
        LogWriter().write_info_log('Running task')
        try:
            l = threading.Lock()
            l.acquire()
            if address not in self.__other_server:
                self.__other_server.append(address)
            l.release()
            h = connection.recv(1024)
            h = bytes.decode(h)
            header = json.loads(h)
            size = int(header['message_size'])
            fingerprint = header['fingerprint']
            result = ''.encode("utf-8")
            while size > 0:
                temp = connection.recv(1024)
                result += temp
                size -= 1024
            result += connection.recv(1024)
            #   Check Integrity
            m = hashlib.md5()
            m.update(result)
            digest = m.hexdigest()

            #   Run task if message hasn't been changed
            if digest == fingerprint:
                LogWriter().write_info_log("Message received correctly!")
                print("Message received correctly!")
                r = result.decode("utf-8")
                data = json.loads(r)
                Task(data).run()
            else:
                LogWriter().write_error_log("Message has been changed!")
                print("Message has been changed!")
        except:
            LogWriter().write_error_log('Error occurs during information transforming.')
            print('Error occurs during information transforming.')

    # listen at the port and run tasks
    def start_listen(self):
        while True:
            try:
                connection, address = self.__sk_server.accept()
                LogWriter().write_info_log('Server accepted access.')
                print('Server accepted access.')
                connection.settimeout(30)
                self.__thread = threading.Thread(target=self.__execute__(connection, address))
                self.__thread.start()
            except TimeoutError:
                LogWriter().write_warning_log("Time out. Thread automatically closed.")
                print("Time out. Thread automatically closed.")
            except :
                LogWriter().write_error_log("Server stopped.")
                print("Server stopped.")
                exit()


if __name__ == '__main__':
    Server().start_listen()
