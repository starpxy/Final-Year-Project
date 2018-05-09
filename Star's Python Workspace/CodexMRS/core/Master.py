# encoding=utf8
# author:Star
# time: 21/04/2018
"""
This one is yeats.ucd.ie
"""
import redis
from CodexMRS.vendor.Results import Results
from CodexMRS.base.configs import config
from CodexMRS.base.network import Server
from CodexMRS.base.network import Client


class Master:
    """
    Master server to assign tasks (in our version, master will also do some calculation)
    """
    # __block_size = 100
    # __max_block_num = 5
    __workers = {
        'csiserver.ucd.ie': ('137.43.92.165', 9609),  # another UCD server
        'yeats.ucd.ie': ('127.0.0.1', 9610),  # this one is master it self
    }
    # __blocks = {}
    __name = 'yeats.ucd.ie'
    __server = None

    # __block_dir = ''
    # def init_blocks(self):
    #     """
    #     Initialize the file blocks into
    #     :return: None
    #     """
    #     for temp in os.walk(self.__block_dir):
    #         file_names = temp[2]
    #         total_num = len(file_names)
    #         for i in range(0, int(total_num / self.__block_size), 1):
    #             self.__blocks[i] = file_names[i:min((total_num - i * self.__block_size), self.__block_size)]

    def __task(self, message,__status):
        """
        Task to execute on the server.
        :param message: the dictionary received from server
        :return: None
        """
        # operation 1 is for task assignment for LSI
        operate_type = message['operate_type']
        timestamp = message['timestamp']
        print('{}========={}'.format(timestamp, operate_type))
        if operate_type == 1:
            query = message['query']
            page = message['page']
            # we do not have enough server to complete mapper and reducer. So just assign Mapper task first.
            # if want to increase reducer, please rewrite the for loop below.
            __status[timestamp] = {'page': page, 'workers': {}}
            for worker in self.__workers.keys():
                print(worker)
                __status[timestamp]['workers'] = {worker: {'status': 1}}
                client = Client(self.__workers[worker][0], '127.0.0.1', self.__workers[worker][1],
                                {'operate_type': 1, 'query': query, 'timestamp': timestamp})
                client.send_message()
        # operation 2 LSI merge
        elif operate_type == 2:
            result = message['result']
            result = Results.from_dict(result)
            name = message['name']
            print(name)
            __status[timestamp]['workers'][name]['status'] = 2
            __status[timestamp]['workers'][name]['result'] = result
            is_complete = True
            print(__status[timestamp]['workers'])
            for slave in __status[timestamp]['workers'].keys():
                if __status[timestamp]['workers'][slave]['status'] == 1:
                    is_complete = False
            if is_complete:
                print("complete")
                results = []
                for worker in __status[timestamp]['workers'].keys():
                    results.append(__status[timestamp]['workers'][worker]['result'])
                page = __status[timestamp]['page']
                result_list = self.LSI_merge(results)
                to_return = self.get_result_at_page(page, config['page_num'], result_list)
                client = Client(config['recall_ip'], self.__name, config['recall_port'], {'result': to_return})
                client.send_message()
        # operation 3 NLP search
        elif operate_type == 3:
            pass
        # operation 4 NLP merge
        elif operate_type == 4:
            pass

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
        fullHitLines = {}
        hitDocs = {}
        matchingLines = {}
        fullHitLineskeys = []
        hitDocskeys = []
        matchingLineskeys = []
        numOfResults = 0
        for result in results:
            fullHitLines.update(result.getFullHitLines())
            hitDocs.update(result.getHitDocs())
            matchingLines.update(result.getMatchingLines())
            numOfResults += result.getNumOfResults()
            fullHitLineskeys = list(fullHitLines.keys())
            hitDocskeys = list(hitDocs.keys())
            matchingLineskeys = list(matchingLines.keys())
            fullHitLineskeys.sort(reverse=True)
            hitDocskeys.sort(reverse=True)
            matchingLineskeys.sort(reverse=True)

        # sort the docs into a single list
        displayList = []
        for k in fullHitLineskeys:
            displayList.append(fullHitLines[k])
        for k in hitDocskeys:
            displayList.append(hitDocs[k])
        for k in matchingLineskeys:
            displayList.append(matchingLines[k])

        return displayList

    def get_result_at_page(self, page, num, displayList):
        # compose the displayList
        currentDisplay = displayList[(page - 1) * num: page * num]
        length = len(displayList)
        return (length, currentDisplay)

    def start_master(self):
        """
        start up the master server
        :return: None
        """
        # self.init_blocks()
        self.__server = Server(self.__task, "137.43.92.45", 9609, max_node_num=200)
        self.__server.start_listening()


if __name__ == '__main__':
    Master().start_master()
