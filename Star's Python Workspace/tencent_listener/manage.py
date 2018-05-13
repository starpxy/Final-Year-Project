# coding=utf8
# author:Star
# time:11/05/2018

from tencent_listener.vendor.network import Server
from tencent_listener.vendor.communicator import CommunicationClient


def task(message, shared):
    result = message['result']
    timestamp = message['timestamp']
    client = CommunicationClient()
    client.send_message(str(timestamp), {'result': result})


server = Server(task, '10.141.131.14', max_node_num=200)
server.start_listening()
