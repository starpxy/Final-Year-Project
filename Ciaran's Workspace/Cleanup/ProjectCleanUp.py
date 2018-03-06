# coding=utf-8
"""
Created on 04/03/2018
Author: Ciarán
"""

import paramiko

from LogWriter import LogWriter


class ProjectCleanUp:

    def __init__(self):
        self.logwriter = LogWriter()
        self.hostname = "123.206.77.7"
        self.username = "ubuntu"
        self.password = "Star==960906"
        self.ssh_client = paramiko.SSHClient()
        self.sftp = None

    def connect_to_server(self):

        self.logwriter.write_info_log("Connecting to server " + self.hostname)
        ssh_client = self.ssh_client

        # Try three times?
        try:
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(hostname=self.hostname, username=self.username, password=self.password)
            self.sftp = self.ssh_client.open_sftp()
            self.logwriter.write_info_log("Connected!")
        except Exception as connection_error:
            self.logwriter.write_error_log("Could not connect to server: " + str(connection_error))

    def unzip(self):

        self.logwriter.write_info_log("Unzipping files")

        try:
            for file in self.sftp.listdir("/home/ubuntu/test_files/unclean"):
                print(file)
                command = "unzip /home/ubuntu/test_files/unclean/" + file + " -d /home/ubuntu/test_files/clean"
                print(command)
                self.ssh_client.exec_command(command)
            self.logwriter.write_info_log("Files unzipped")
        except Exception as command_error:
            self.logwriter.write_error_log("Could not unzip files: " + str(command_error))

    def delete_files(self):

        self.logwriter.write_info_log("Deleting unwanted files")

        try:
            self.ssh_client.exec_command("cd /home/ubuntu/test_files/clean;"
                                         "python3 delete_unwanted_files.py")
            self.logwriter.write_info_log("Unwanted files deleted")
        except Exception as command_error:
            self.logwriter.write_error_log("Could not delete files: " + str(command_error))

    def clean_up(self):
        self.connect_to_server()
        self.unzip()
        self.delete_files()

        self.ssh_client.close()


def main():
    ProjectCleanUp().clean_up()


if __name__ == "__main__":
    main()
