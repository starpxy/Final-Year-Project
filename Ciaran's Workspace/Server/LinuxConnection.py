# coding=utf-8
"""
Created on 07/03/2018
Author: Ciarán
"""

import paramiko

from LogWriter import LogWriter


class LinuxConnection:

    def __init__(self):
        # Parent
        self.log_writer = LogWriter()
        self.ssh_client = paramiko.SSHClient()
        self.sftp = None

        self.linux_server_details = {'hostname': '123.206.77.77', 'username': 'ubuntu', 'password': 'Star==960906'}
        #self.connect_to_server()
        self.open_linux_connection()
        super().__init__()

    ### Parent ###
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

    def mkdir(self, dir_path):
        self.sftp.mkdir(dir_path)

    def listdir(self, path):
        return self.sftp.listdir(path)

    def exec_command(self, command):
        self.ssh_client.exec_command(command)

    def close_connection(self):
        self.ssh_client.close()
    ### Parent ###

    def connect_to_server(self):
        try:
            self.ssh_client.get_transport().is_active()
            return self.sftp
        except ConnectionError:
            self.open_linux_connection()
            return self.sftp

    def open_linux_connection(self):

        hostname = self.linux_server_details.get('hostname')
        username = self.linux_server_details.get('username')
        password = self.linux_server_details.get('password')

        ssh_client = self.ssh_client
        # Let's the machine know that you trust the server
        # Paramiko rejects all new remote machines by default but AutoAddPolicy() changes it to allow any host
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        self.log_writer.write_info_log("Connecting to server " + hostname)

        try:
            ssh_client.connect(hostname=hostname, username=username, password=password)
            self.sftp = self.ssh_client.open_sftp()  # Open an SFTP session on the SSH server.
        except Exception as connection_error:
            self.log_writer.write_error_log("Could not connect to server: " + str(connection_error))
