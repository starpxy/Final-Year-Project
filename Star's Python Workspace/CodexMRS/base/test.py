# import threading
#
# class test:
#     def __init__(self):
#         global h
#         h = {}
#     def hello(self,i):
#         global h
#         print(h)
#         h[i] = i
# if __name__ == '__main__':
#     t = test()
#     for i in range(100):
#         threading.Thread(target=t.hello(i))

from CodexMRS.base.network import Server


def test(message, share):
    print(message)
    print(share)
    share[message['test']] = 10


Server(test, "localhost").start_listening()
