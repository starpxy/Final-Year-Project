# coding=utf8
# author:Star
# time: 06/05/2018
import threading
class Singleton:
    __list = []
    def __init__(self):
        print("init...")
__instance = None
def get_instance():
    if __instance == None:
        __instance = Singleton()
    return self.__instance

def test():
    Singleton.get_instance()
if __name__ == '__main__':
    thread = threading.Thread(target=test())