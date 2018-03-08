# coding=utf-8
"""
Created on 08/03/2018
Author: Ciarán
"""

import paramiko


class Test1:

    def open_linux_connection(self):
        try:
            linux_server_details = {'hostname': '123.206.77.77', 'username': 'ubuntu', 'password': 'Star==960906'}
            hostname = linux_server_details.get('hostname')
            username = linux_server_details.get('username')
            password = linux_server_details.get('password')

            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(hostname=hostname, username=username, password=password)
            sftp = ssh_client.open_sftp()

            file = sftp.open("/home/ubuntu/test_files/clean/Final-Year-Project/Code/src/com/codex/main.py")
            for line in file.readlines():
                print(line)



        except Exception as connection_error:
            print("Could not connect to server: " + str(connection_error))


class Test2:

    def __init__(self):
        self.ssh_client = paramiko.SSHClient()
        self.sftp = None
        self.linux_server_details = {'hostname': '123.206.77.77', 'username': 'ubuntu', 'password': 'Star==960906'}
        self.open_linux_connection()

    def open_file(self, file):
        return self.sftp.open(file)

    def listdir(self, path):
        return self.sftp.listdir(path)

    def open_linux_connection(self):

        hostname = self.linux_server_details.get('hostname')
        username = self.linux_server_details.get('username')
        password = self.linux_server_details.get('password')

        ssh_client = self.ssh_client
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            ssh_client.connect(hostname=hostname, username=username, password=password)
            self.sftp = self.ssh_client.open_sftp()
        except Exception as connection_error:
            print("Could not connect to server: " + str(connection_error))


def main():
    test1 = Test1()
    test2 = Test2()

    test2.open_file("/home/ubuntu/test_files/clean/Final-Year-Project/Code/src/com/codex/main.py")
    test1.open_linux_connection()



if __name__ == '__main__':
    main()