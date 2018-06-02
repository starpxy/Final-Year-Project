# encoding=utf8
# author:Star
# time: 21/04/2018

import json
import socket
import hashlib
import threading
from search.supportings.LogWriter import LogWriter


class Server:
    """
    A class to supporting Master and Workers in CodexMRS.core package
    """
    __port = 9609
    __max_node_num = 4
    __server_socket = None
    __public_ip_address = ''
    __connected_ip = []
    __task = None

    def __init__(self, task, public_ip_address, port=9609, max_node_num=4):
        """
        Initialize the basic configuration of server socket.
        :param task: A function to run after the server receive information.
        :param public_ip_address: The public network address of your server (if your system run on a LAN, then use inner address)
        :param port: An available port number to run your server on.
        :param max_node_num: max number of nodes in the parallel system.
        """
        self.__port = port
        self.__max_client_num = max_node_num
        self.__public_ip_address = public_ip_address
        self.__task = task
        global __shared_variable
        __shared_variable = {}

    def listen_once(self):
        self.__server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__server_socket.bind((self.__public_ip_address, self.__port))
        self.__server_socket.listen(self.__max_client_num)
        connection, address = self.__server_socket.accept()
        connection.settimeout(30)
        if address not in self.__connected_ip:
            self.__connected_ip.append(address)
        msg = b''
        while True:
            buff = connection.recv(1024)
            if not buff:
                break
            msg += buff
        msg = bytes.decode(msg)
        message = MessageDumper.dump_s(msg)
        self.__server_socket.close()
        if message.get_is_modified():
            LogWriter().write_error_log('Message has been modified!')
        else:
            return message

    def start_listening(self):
        """
        Listen to the specific port, and start a new thread after it accept any client.
        :return: None
        """
        self.__server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__server_socket.bind((self.__public_ip_address, self.__port))
        self.__server_socket.listen(self.__max_client_num)
        self.__listen()

    def __listen(self):
        """
        A private function that only will be called by start_listening()
        :return: None
        """
        while True:
            connection, address = self.__server_socket.accept()
            connection.settimeout(30)
            LogWriter().write_info_log("{} connect to the server...".format(address[0]))
            LogWriter().write_error_log("{} connect to the server...".format(address[0]))
            thread = threading.Thread(target=self.__execute(connection, address[0]))
            thread.start()

    def __execute(self, connection, address):
        """
        A function to run receive information from client and run tasks
        :param connection: the socket connection
        :param address: ip address of the client who connected with the server
        :return: None
        """
        global __shared_variable
        if address not in self.__connected_ip:
            self.__connected_ip.append(address)
        msg = b''
        while True:
            buff = connection.recv(1024)
            if not buff:
                break
            msg += buff
        msg = bytes.decode(msg)
        message = MessageDumper.dump_s(msg)
        if message.get_is_modified():
            LogWriter().write_error_log('Message has been modified!')
        else:
            self.__task(json.loads(message.get_message_body()), __shared_variable)

    def get_connected_ip(self):
        """
        Getter for connected ip address
        :return: a list of connected ip address.
        """
        return self.__connected_ip

    def get_public_ip_add(self):
        """
        Getter for public ip address
        :return: a string of public ip address
        """
        return self.__public_ip_address


class Client:
    """
    a socket client to send message to server
    """
    __des_ip = ''
    __source_ip = ''
    __target_port = 9609
    __message = {}

    def __init__(self, des_ip, source_ip, target_port, message):
        self.__des_ip = des_ip
        self.__source_ip = source_ip
        self.__target_port = target_port
        self.__message = message

    def send_message(self):
        """
        send message to destination server
        :return: None
        """
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((self.__des_ip, self.__target_port))
        LogWriter().write_info_log(
            "Connected to server {}:{}".format(self.__des_ip, self.__target_port))
        message = json.dumps(self.__message)
        to_send = MessageDumper.encode_s(self.__source_ip, self.__des_ip, message)
        to_send = to_send.encode()
        while len(to_send) > 1024:
            trunk = to_send[0:1024]
            to_send = to_send[1024:]
            client.send(trunk)
        if len(to_send) > 0:
            client.send(to_send)
        client.close()
        LogWriter().write_error_log('Message sent successfully.')


class Header:
    """
    Our own socket header
    """
    __source_ip = ''
    __des_ip = ''
    __digest = ''
    __total_length = 0

    def get_source_ip(self):
        """
        Getter of source ip
        :return: string contains source ip
        """
        return self.__source_ip

    def get_des_ip(self):
        """
        Getter of destination ip
        :return: string contains destination ip
        """
        return self.__des_ip

    def get_digest(self):
        """
        Getter of digest
        :return: string contains digest of message body
        """
        return self.__digest

    def get_total_length(self):
        """
        Getter of total length
        :return: integer of message body length
        """
        return self.__total_length

    def __init__(self, source_ip, des_ip, total_length, digest):
        """
        :param source_ip: sender ip address
        :param des_ip: destination ip address
        :param total_length: the total length of the message body
        :param digest: digest of the message
        """
        self.__source_ip = source_ip
        self.__des_ip = des_ip
        self.__total_length = total_length
        self.__digest = digest

    def encode_s(self):
        """
        Encode the header into string
        :return: Header String
        """
        result = '|CodEX HEADER=|SOURCE_IP:{}/DES_IP:{}/TOTAL_LENGTH:{}/DIGEST:{}|=CodEX HEADER|'.format(
            self.__source_ip,
            self.__des_ip,
            self.__total_length,
            self.__digest)
        return result


class Message:
    """
    To return by MessageDumper
    """
    __header = None
    __message_body = ''
    __is_modified = True

    def __init__(self, header, message_body):
        self.__header = header
        self.__message_body = message_body
        m = hashlib.md5()
        m.update(message_body.encode('utf-8'))
        digest = m.hexdigest()
        if self.__header.get_digest() == digest:
            self.__is_modified = False
        else:
            self.__is_modified = True

    def get_message_body(self):
        """
        Getter of message body
        :return: string contains message body
        """
        return self.__message_body

    def get_sender(self):
        """
        Getter of sender
        :return: sender's ip address
        """
        return self.__header.get_source_ip()

    def get_is_modified(self):
        """
        Getter of is_modified
        :return: a boolean value of __is_modified
        """
        return self.__is_modified


class MessageDumper:
    """
    This is a class to create and dump socket messages.
    """

    @staticmethod
    def encode_s(source_ip, des_ip, message_body):
        """
        Encode the message into string
        :param source_ip: sender ip address
        :param des_ip: destination ip address
        :param message_body: a string to send
        :return: a String that contains header and origin message
        """
        m = hashlib.md5()
        m.update(message_body.encode('utf-8'))
        digest = m.hexdigest()
        total_length = len(message_body)
        header = Header(source_ip, des_ip, total_length, digest)
        header_str = header.encode_s()
        result = header_str + message_body
        return result

    @staticmethod
    def dump_s(msg=''):
        """
        Dump a String into a message object
        :param msg: a string received by server
        :return: Message object (return None when header isn't integrated)
        """
        start = msg.find('|CodEX HEADER=|')
        end = msg.find('|=CodEX HEADER|')
        if start == -1 or end == -1:
            return None
        header_str = msg[(start + 15):end]
        attributes = header_str.split('/')
        source_ip = ''
        des_ip = ''
        total_length = 0
        digest = ''
        for attr in attributes:
            params = attr.split(':')
            if params[0] == 'SOURCE_IP':
                source_ip = params[1]
            elif params[0] == 'DES_IP':
                des_ip = params[1]
            elif params[0] == 'TOTAL_LENGTH':
                total_length = int(params[1])
            elif params[0] == 'DIGEST':
                digest = params[1]
        header = Header(source_ip, des_ip, total_length, digest)
        msg_body = msg[(end + 15):(total_length + end + 15)]
        message = Message(header, msg_body)
        return message


if __name__ == '__main__':
    # st = MessageDumper.encode_s("localhost", "127.0.0.1", "hello world")
    # msg = MessageDumper.dump_s(st)
    # print(msg.get_message_body())
    # print(msg.get_is_modified())
    # print(msg.get_sender())
    # server = Server(test, "yeats.ucd.ie")
    # server.start_listening()
    client = Client("localhost", "127.0.0.1", 9609, {"test": "kwk"})
    client.send_message()
