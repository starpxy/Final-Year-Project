# encoding=utf8
# author:Star
# time: 21/04/2018
import os
from CodexMRS.base.network import Server


class Master:
    """
    Master server to assign tasks (in our version, master will also do some calculation)
    """
    __block_size = 100
    __max_block_num = 5
    __blocks = {}
    __mappers = []
    __reducers = []
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

    def __task(self, message):
        """
        Task to execute on the server.
        :param message: the dictionary received from server
        :return: None
        """
        # operation 1 is to allocate blocks and
        operate_type = message['operate_type']
        if operate_type == 1:

            print('1')
        # operation 2 is to
        elif operate_type == 2:
            print('2')

    def start_master(self):
        """
        start up the master server
        :return: None
        """
        self.init_blocks()
        server = Server(self.__task, "localhost")
        server.start_listening()


if __name__ == '__main__':
    Master("/Users/quanyewu/Desktop/files").init_blocks()
