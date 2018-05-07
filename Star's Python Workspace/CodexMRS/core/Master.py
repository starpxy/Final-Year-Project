# encoding=utf8
# author:Star
# time: 21/04/2018
import os
from CodexMRS.base.configs import config
from CodexMRS.base.network import Server
from CodexMRS.base.network import Client
from CodexMRS.base.communicator import CommunicationClient
from CodexMRS.vendor.LogWriter import LogWriter


class Master:
    """
    Master server to assign tasks (in our version, master will also do some calculation)
    """
    __block_size = 100
    __max_block_num = 5
    __blocks = {}
    __mappers = {}
    __server = None
    __block_dir = ''

    def __init__(self, block_dir):
        self.__block_dir = block_dir

    def init_blocks(self):
        """
        Initialize the file blocks into
        :param file_dir: the folder that store your source files
        :return: None
        """
        for temp in os.walk(self.__block_dir):
            file_names = temp[2]
            total_num = len(file_names)
            for i in range(0, int(total_num / self.__block_size), 1):
                self.__blocks[i] = file_names[i:min((total_num - i * self.__block_size), self.__block_size)]

    def __task(self, message, ip_add):
        """
        Task to execute on the server.
        :param message: the dictionary received from server
        :return: None
        """
        # operation 1 is for task assignment for LSI
        operate_type = message['operate_type']
        timestamp = message['timestamp']
        if operate_type == 1:
            LogWriter().write_info_log("execute operation 1: LSI task assignment")
            print("execute operation 1: LSI task assignment")
            query = message['query']
            ip_adds = self.__server.get_connected_ip()
            counter = 0
            # we do not have enough server to complete mapper and reducer. So just assign Mapper task first.
            # if want to increase reducer, please rewrite the for loop below.
            self.__mappers[timestamp] = {}
            for ip_add in ip_adds:
                availability = self.__check_ip_availability(ip_add)
                if availability:
                    self.__mappers[timestamp][ip_add] = {"status": 1}
            for mapper in self.__mappers[timestamp].keys():
                client = Client(mapper, self.__server.get_public_ip_add(), 9609,
                                {'operate_type': 1, 'query': query, 'timestamp': timestamp})
                client.send_message()
        # operation 2 is for result merging
        elif operate_type == 2:
            LogWriter().write_info_log("execute operation 2: result merging")
            print("execute operation 2: result merging")
            result = message['result']
            self.__mappers[timestamp][ip_add]['status'] = 2
            self.__mappers[timestamp][ip_add]['result'] = result
            is_complete = True
            for ip in self.__mappers[timestamp].keys():
                if self.__mappers[timestamp][ip]['status'] == 1:
                    is_complete = False
            if is_complete:
                results = []
                for ip in self.__mappers[timestamp].keys():
                    results.append(self.__mappers[timestamp][ip]['result'])
                to_return = self.LSI_merge(results)
                client = CommunicationClient()
                client.send_message(config['socket_path'] + '/' + timestamp, {'results': to_return})

    def __check_ip_availability(self, ip_add):
        """
        Check if a ip address still on line.
        :param ip_add: the ip address that we want to check
        :return: True->available  False->unavailable
        """
        try:
            client = Client(ip_add, self.__server.get_public_ip_add(), 9609, {"operate_type": 3})
            client.send_message()
        except:
            return False
        return True

    def LSI_merge(self, results):
        """
        Merge of LSI
        :return: A LSI Result
        """

        return None

    def start_master(self):
        """
        start up the master server
        :return: None
        """
        self.init_blocks()
        self.__server = Server(self.__task, "localhost")
        self.__server.start_listening()


if __name__ == '__main__':
    Master("/Users/quanyewu/Desktop/files").start_master()
