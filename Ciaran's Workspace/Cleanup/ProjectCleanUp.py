# coding=utf-8
"""
Created on 04/03/2018
Author: Ciarán

Unzips all zip folders in the unclean directory on the server,
stores them in the clean folder and then runs delete_files_script.py
"""

from LogWriter import LogWriter
from Server.LinuxConnection import LinuxConnection


class ProjectCleanUp:

    def __init__(self):
        self.log_writer = LogWriter()
        self.connection = LinuxConnection()

    def unzip(self):

        self.log_writer.write_info_log("Unzipping files")

        # Keep unzipped folders but put in separate directory
        # Delete unzipped directories containing source code files
        try:
            for file in self.connection.listdir("/home/ubuntu/test_files/unclean"):
                unzip_command = "unzip /home/ubuntu/test_files/unclean/" + file + \
                                " -d /home/ubuntu/test_files/clean/" + file[:-4]
                self.connection.exec_command(unzip_command)
                self.log_writer.write_info_log(file + " unzipped")
            self.log_writer.write_info_log("Files unzipped")
        except Exception as command_error:
            self.log_writer.write_error_log("Could not unzip files: " + str(command_error))

    def delete_files(self):

        self.log_writer.write_info_log("Deleting unwanted files")

        try:
            self.connection.exec_command("cd /home/ubuntu/test_files/clean;"
                                         "python3 delete_unwanted_files.py")
            self.log_writer.write_info_log("Unwanted files deleted")
        except Exception as command_error:
            self.log_writer.write_error_log("Could not delete files: " + str(command_error))

    def run(self):
        self.unzip()
        self.delete_files()


def main():
    ProjectCleanUp().run()


if __name__ == "__main__":
    main()
