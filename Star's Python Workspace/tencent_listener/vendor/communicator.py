# coding=utf8
# author:Star
# time: 04/05/2018

import socket
import json
from tencent_listener.vendor.network import MessageDumper
from tencent_listener.core.configs import config


class CommunicationServer:
    __connection_socket = None

    def __config_connection(self, socket_name, listen_number=1):
        """
        A private function to initialize the configuration
        :return: None
        """
        self.__connection_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.__connection_socket.bind(config['socket_path'] + '/' + socket_name)
        self.__connection_socket.listen(listen_number)

    def receive_message(self, socket_name, listen_number=1):
        """
        Start the connection and accept once only.
        :param socket_name: the name of the server (the key of communication)
        :param listen_number: how many server can listen
        :return: None => Message is modified. Message => received successfully.
        """
        self.__config_connection(socket_name, listen_number)
        connection, client_address = self.__connection_socket.accept()
        msg = b''
        while True:
            buff = connection.recv(1024)
            if not buff:
                break
            msg += buff
        msg = bytes.decode(msg)
        message = MessageDumper.dump_s(msg)
        connection.close()
        if message.get_is_modified():
            print('Message has been modified!')
            return None
        else:
            print('Message Received Successfully.')
            return json.loads(message.get_message_body())


class CommunicationClient:
    __connection_socket = None

    def send_message(self, socket_name, message):
        """
        Send message to the communication server.
        :param socket_name: the name of target server socket
        :param message: message to be sent
        :return: None
        """
        self.__connection_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.__connection_socket.connect(socket_name)
        message = json.dumps(message)
        msg = MessageDumper.encode_s('', '', message)
        msg = msg.encode()
        while len(msg) > 1024:
            trunk = msg[0:1024]
            msg = msg[1024:]
            self.__connection_socket.send(trunk)
        if len(msg) > 0:
            self.__connection_socket.send(msg)
        self.__connection_socket.close()

if __name__ == '__main__':
    server = CommunicationServer()
    msg = server.receive_message('test')
    print(msg)