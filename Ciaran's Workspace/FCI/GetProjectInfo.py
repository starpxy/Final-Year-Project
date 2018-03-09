# coding=utf-8
"""
Created on 06/03/2018
Author: Ciarán

Gets all the info from the files in a project and stores them in a json file
"""

import os
import re

from FCI.FormattedCodeInterface import FormattedCodeInterface
from LogWriter import LogWriter
import FCI.FCIConverter
from Server.LinuxConnection import LinuxConnection


class GetProjectInfo:

    def __init__(self, connection):
        self.local_path = "../../Hester'sWorkSpace/files"
        self.remote_path = "/home/ubuntu/test_files/json_files"
        self.clean_projects_path = "/home/ubuntu/test_files/clean"
        self.files_in_project = []
        self.log_writer = LogWriter()
        self.connection = connection

    def save_file_details_to_fci_object(self, file_path, file_name):
        fci = FormattedCodeInterface()

        fci.set_file_name(file_name)
        fci.set_save_path(file_path)  # How to save files? One directory with all files or in original path?
        self.set_code_and_comments(file_path, fci)

        '''
        fci.set_author()
        fci.set_description()
        fci.set_language()
        fci.set_project_name()
        fci.set_quality()
        fci.set_save_time()
        fci.set_update_at()
        '''

        self.files_in_project.append(fci)
        self.log_writer.write_info_log(file_path + " documented.")

    def set_code_and_comments(self, file_path, fci):
        file = self.connection.open_file(file_path)
        code = ''
        comments_list = []
        comments = ''
        python_comments = ['\"\"\"((.|\n)*)\"\"\"', '\'\'\'((.|\n)*)\'\'\'', '#.*']

        for line in file.readlines():
            code += line

        for comment_pattern in python_comments:
            comments_list += re.findall(comment_pattern, code)
            code = re.sub(comment_pattern, '', code)

        for recorded_comment in comments_list:
            if type(recorded_comment) is tuple:
                for comment in recorded_comment:
                    comments += comment + '\n'
            else:
                comments += recorded_comment + '\n'

        fci.set_code(code)
        fci.set_comments(comments)

    def find_and_save_files(self, parent_directory):
        try:
            for file_name in self.connection.listdir(parent_directory):
                file_path = parent_directory + '/' + file_name
                if file_name.endswith(".py"):
                    self.save_file_details_to_fci_object(file_path, file_name)
                else:
                    self.find_and_save_files(file_path)
        except Exception as e:
            self.log_writer.write_error_log(str(e))

    def save_to_json_file(self):
        self.log_writer.write_info_log("Saving Json files")
        self.save_to_local_directory()
        self.save_to_remote_directory()

    def save_to_local_directory(self):
        for fci_object in self.files_in_project:
            FCI.FCIConverter.to_json_file(self.local_path, fci_object)

        self.log_writer.write_info_log("Saved to local machine at " + self.local_path)

    def save_to_remote_directory(self):
        for file in os.listdir(self.local_path):
            local_path = self.local_path + "/" + file
            remote_path = self.remote_path + "/" + file
            self.connection.copy_file_to_server(local_path, remote_path)

        self.log_writer.write_info_log("Saved to remote machine at " + self.remote_path)

    def run(self):
            self.find_and_save_files(self.clean_projects_path)
            self.save_to_json_file()


def main():
    GetProjectInfo().run()


if __name__ == '__main__':
    main()
