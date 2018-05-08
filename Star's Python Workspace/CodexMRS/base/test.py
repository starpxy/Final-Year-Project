from CodexMRS.base.network import Client
from CodexMRS.base.communicator import CommunicationClient
if __name__ == '__main__':
    msg = ''
    for i in range(10000):
        msg+='as'
    client = Client("127.0.0.1", "127.0.0.1", 9609, {"hello": msg})
    client.send_message()
    # client = CommunicationClient()
    # client.send_message('test',{"test":"test"})