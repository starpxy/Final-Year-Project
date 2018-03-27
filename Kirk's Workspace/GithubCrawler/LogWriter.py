'''
@author: Star

@time: 05-03-2018

'''
import logging
import os

class LogWriter:

    # Write error log into logs/error.log
    def write_error_log(self,content):
        if not os.path.exists("logs"):
            os.mkdir("logs")
        logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',filename="logs/error.log", filemode="a", level=logging.ERROR)
        logging.error(content)

    # Write warning log into logs/warning.log
    def write_warning_log(self,content):
        if not os.path.exists("logs"):
            os.mkdir("logs")
        logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',filename="logs/warning.log", filemode="a", level=logging.DEBUG)
        logging.warning(content)

    # Write info log into logs/info.log
    def write_info_log(self,content):
        if not os.path.exists("logs"):
            os.mkdir("logs")
        logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',filename="logs/info.log", filemode="a", level=logging.INFO)
        logging.info(content)