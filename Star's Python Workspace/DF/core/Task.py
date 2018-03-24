# coding=utf-8
# author:star
from LogWriter import LogWriter


class Task:
    __data = {}

    def __init__(self, data):
        self.__data = data

    #   TODO: Insert your task content here...
    def run(self):
        LogWriter().write_info_log("Running server task...")