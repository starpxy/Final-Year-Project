# coding=utf-8
"""
Created on 07/03/2018
Author: Ciarán
"""

import paramiko

from src.Server import Connection


class WindowsConnection(Connection):

    def __init__(self):
        self.windows_server_details = {'hostname': 'yeats.ucd.ie', 'username': 'xingyu', 'password': 'vKZkv3rt'}
        super().__init__()

    def connect_to_server(self):
        if self.ssh_client.get_transport().is_active():
            return self.sftp
        else:
            self.open_windows_connection()
            return self.sftp

    def open_windows_connection(self):

        hostname = self.windows_server_details.get('hostname')
        username = self.windows_server_details.get('username')
        password = self.windows_server_details.get('password')

        ssh_client = self.ssh_client
        # Let's the machine know that you trust the server
        # Paramiko rejects all new remote machines by default but AutoAddPolicy() changes it to allow any host
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        self.logwriter.write_info_log("Connecting to server " + hostname)

        try:
            ssh_client.connect(hostname=hostname, username=username, password=password)
            self.sftp = self.ssh_client.open_sftp()  # Open an SFTP session on the SSH server.
            self.logwriter.write_info_log("Connected!")
        except Exception as connection_error:
            self.logwriter.write_error_log("Could not connect to server: " + str(connection_error))
