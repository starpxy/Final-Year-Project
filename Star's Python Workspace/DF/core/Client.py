# coding=utf-8
# author:Star
import socket
import json
import hashlib
from DF.LogWriter import LogWriter


class Client:
    __sk_client = ''
    __main_server_ip = ''
    __main_server_port = ''

    def __init__(self, main_server_ip, main_server_port):
        self.__main_server_ip = main_server_ip
        self.__main_server_port = main_server_port

    def send_message(self, message={}):
        try:
            self.__sk_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.__sk_client.connect((self.__main_server_ip, self.__main_server_port))
            print("Connected to server {}:{}".format(self.__main_server_ip, self.__main_server_port))
            LogWriter().write_info_log(
                "Connected to server {}:{}".format(self.__main_server_ip, self.__main_server_port))
        except:
            LogWriter().write_error_log(
                "Cannot connect to server {}:{}!".format(self.__main_server_ip, self.__main_server_port))
            print("Cannot connect to server {}:{}!".format(self.__main_server_ip, self.__main_server_port))
            return
        to_send = json.dumps(message).encode("utf-8")
        m = hashlib.md5()
        m.update(to_send)
        digest = m.hexdigest()
        header = json.dumps({'message_size': str(len(to_send)).zfill(953), 'fingerprint': digest}).encode('utf-8')
        # print(header)
        try:
            self.__sk_client.send(header)
            while len(to_send) > 1024:
                trunk = to_send[0:1024]
                to_send = to_send[1024:]
                self.__sk_client.send(trunk)
            if len(to_send) > 0:
                self.__sk_client.send(to_send)

        except:
            LogWriter().write_error_log("Message {} is not sent to main server!".format(header))
        self.__sk_client.close()
        return


if __name__ == '__main__':
    c = Client("localhost", 9609)
    i = 0
    s = 'a'
    while i < 10:
        s += 'Star '
        i += 1
    msg = {'start': s}
    print(msg)
    c.send_message(msg)
