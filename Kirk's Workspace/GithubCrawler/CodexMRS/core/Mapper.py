# encoding=utf8
# author:Star


class Mapper:
    # status:0  available
    # status:1  working
    # status:2  work done (Only when all the nodes done their work, all the status will be changed to 0)
    __status = 0
    __port = 9609
    __alias = None
    __client = None
    __server = None

    def __init__(self):
        pass