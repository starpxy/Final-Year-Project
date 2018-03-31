# coding=utf-8
"""
Created on 07/03/2018
Author: Ciarán
"""

import paramiko

from LogWriter import LogWriter


class Connection:

    def __init__(self):
        self.log_writer = LogWriter()
        self.ssh_client = paramiko.SSHClient()
        self.sftp = None

    def open_file(self, file):
        return self.sftp.open(file)

    def copy_file_to_server(self, local_path, remote_path):
        self.sftp.put(local_path, remote_path)

    def isdir(self, file):
        try:
            self.listdir(file)
            return True
        except FileNotFoundError:
            return False

    def listdir(self, path):
        return self.sftp.listdir(path)

    def exec_command(self, command):
        self.ssh_client.exec_command(command)

    def close_connection(self):
        self.ssh_client.close()