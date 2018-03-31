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
        try:
            self.listdir(file)
            return True
        except:
            return False

    def listdir(self, path):
        return self.sftp.listdir(path)

    def exec_command(self, command):
        return self.ssh_client.exec_command(command)

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
        except Exception as connection_error:
            print("Could not connect to server: " + str(connection_error))


def main():
    connection = TestLinuxServer()
    print(connection.listdir("/home/ubuntu/test_files/clean"))

    if connection.isdir("/home/ubuntu/test_files/unclean"):
        print("isdir")
    else:
        print("notdir")

    if connection.isdir("/home/ubuntu/test_files/clean/Final-Year-Project/Code/src/com/codex/main.py"):
        print("isdir")
    else:
        print("notdir")

    file = connection.open_file("/home/ubuntu/test_files/clean/Final-Year-Project/Code/src/com/codex/main.py")
    dir = connection.open_file("/home/ubuntu/test_files/clean/Final-Year-Project/Code/src/com/codex")
    content = ''
    print(file)
    print(dir)

    #print(connection.listdir("/home/ubuntu/test_files/clean/Final-Year-Project/Code/src/com/codex"))
    #print(connection.listdir("/home/ubuntu/test_files/clean/Final-Year-Project/Code/src/com/codex/main.py"))

    #print(connection.listdir(dir))
    #print(connection.listdir(file))

    for line in file.readlines():
        content += line

    print(content)

    stdin, stdout, stderr = connection.exec_command("-d /home/ubuntu/test_files/clean/Final-Year-Project/Code/src/com/codex/main.py")
    print(stdout.channel.recv_exit_status())
    print(connection.exec_command("-d /home/ubuntu/test_files/clean"))


if __name__ == '__main__':
    main()
