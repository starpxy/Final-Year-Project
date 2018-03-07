# coding=utf-8
"""
Created on 07/03/2018
Author: Ciarán
"""

import paramiko

from LogWriter import LogWriter


class Connection:

    def __init__(self):
        self.logwriter = LogWriter()
        self.ssh_client = paramiko.SSHClient()
        self.sftp = None

    def listdir(self, path):
        self.sftp.listdir(path)

    def exec_command(self, command):
        self.ssh_client.exec_command(command)

    def close_connection(self):
        self.ssh_client.close()
