# coding=utf-8
# author:star

class configuration:
    __VERSION = '1.0.0'
    __IS_MAIN = False
    __SERVER_LIST = []

    @property
    def VERSION(self):
        return self.__VERSION

    @property
    def IS_MAIN(self):
        return self.IS_MAIN

    @IS_MAIN.setter
    def IS_MAIN(self, value):
        if isinstance(value, bool):
            self.__IS_MAIN = value

    @property
    def SERVER_LIST(self):
        return self.__SERVER_LIST

    @SERVER_LIST.setter
    def SERVER_LIST(self, value):
        if isinstance(value, list):
            self.__SERVER_LIST = value


if __name__ == '__main__':
    configuration.SERVER_LIST = ['asdf']
    print(configuration.SERVER_LIST)
