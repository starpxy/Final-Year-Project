# coding=utf-8
"""
Created on 06/03/2018
Author: Ciarán

Gets all the info from the files in a project and stores them in a json file
"""

import os

from FCI.FormattedCodeInterface import FormattedCodeInterface
from LogWriter import LogWriter
import FCI.FCIConverter


class GetProjectInfo:

    def __init__(self):
        self.files_in_project = []
        self.logwriter = LogWriter()

    def save_file_details(self, file_path, file_name):
        fci = FormattedCodeInterface()

        fci.set_file_name(file_name)
        fci.set_save_path(file_path)  # How to save files? One directory with all files or in original path?
        fci.set_content(self.get_file_content(file_path))

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
        self.logwriter.write_info_log(file_name + " documented.")

    def get_file_content(self, file_path):
        file = open(file_path)
        content = ''
        print(file)

        for line in file.readlines():
            content += line

        return content

    def find_all_files(self, parent_directory):
        for file_name in os.listdir(parent_directory):
            file_path = parent_directory + '/' + file_name
            if os.path.isdir(file_path):
                self.find_all_files(file_path)
            else:
                self.save_file_details(file_path, file_name)

    def print_list_details(self):
        for file in self.files_in_project:
            print(file.get_file_name() + " " + str(file))

    def save_to_json_file(self):
        for fci_object in self.files_in_project:
            FCI.FCIConverter.to_json_file("../../Hester'sWorkSpace/files", fci_object)

    def run(self):
        self.find_all_files(os.curdir + "/Final-Year-Project")
        self.print_list_details()
        self.save_to_json_file()


def main():
    GetProjectInfo().run()


if __name__ == '__main__':
    main()
