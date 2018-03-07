# coding=utf-8
"""
Created on 07/03/2018
Author: Ciarán
"""

import stat

import paramiko


class TestLinuxServer:

    def __init__(self):
        self.ssh_client = paramiko.SSHClient()
        self.sftp = None
        self.linux_server_details = {'hostname': '123.206.77.77', 'username': 'ubuntu', 'password': 'Star==960906'}
        self.open_linux_connection()

    def open_file(self, file):
        return self.sftp.open(file)

    def isdir(self, file):
        for attr in self.sftp.listdir_attr(file):
            return stat.S_ISDIR(attr.st_mode)

    def listdir(self, path):
        self.sftp.listdir(path)

    def exec_command(self, command):
        self.ssh_client.exec_command(command)

    def close_connection(self):
        self.ssh_client.close()

    def open_linux_connection(self):

        hostname = self.linux_server_details.get('hostname')
        username = self.linux_server_details.get('username')
        password = self.linux_server_details.get('password')

        ssh_client = self.ssh_client
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            ssh_client.connect(hostname=hostname, username=username, password=password)
            self.sftp = self.ssh_client.open_sftp()
            print(self.sftp.listdir("/home/ubuntu/test_files/clean"))
        except Exception as connection_error:
            print("Could not connect to server: " + str(connection_error))


def main():
    connection = TestLinuxServer()
    print(connection.listdir("/home/ubuntu/test_files/clean"))


if __name__ == '__main__':
    main()
