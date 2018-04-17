# coding=utf8
# author:Star
import socket
import threading
from DF.core.Server import Server
from DF.core.Client import Client


class Master():
    # Every worker will have such a status: 0 represents works, other represents down.
    __mappers = []
    __reducers = []
    __ttl = 5.0
    __master = ''

    def __init__(self, port=9609):
        self.allocate_workers()
        t = threading.Thread(target=self.start(port=port))
        t.start()

    def config_ttl(self, ttl):
        self.__ttl = ttl

    def start(self, port):
        self.__master = Server(ip_address=socket.gethostbyname(socket.gethostname()), port=port)
        self.__master.start_listen()

    def allocate_workers(self):
        if self.__master != '':
            print("allocating...")
            workers = self.__master.get_workers()
            self.__mappers = []
            self.__reducers = []
            i = 0
            for worker in workers:
                client = Client(main_server_ip=worker, main_server_port=9609)
                error_code = client.send_message({})
                if i % 2 == 0:
                    self.__mappers.append({"status": error_code, "ip_address": worker})
                else:
                    self.__reducers.append({"status": error_code, "ip_address": worker})
        thread = threading.Timer(self.__ttl, self.allocate_workers)
        thread.start()


if __name__ == '__main__':
    Master()
