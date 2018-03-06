# coding=utf-8
"""
Created on 04/03/2018
Author: Ciarán
"""

import zipfile
import os


class ProjectCleanUp:

    def __init__(self, project_file_name):
        self.project_file_name = project_file_name

    def unzip(self):
        project_file = zipfile.ZipFile(self.project_file_name)
        project_file.extractall(self.project_file_name[:-4])
        project_file.close()

    def delete_files(self, parent_directory):
        for file_name in os.listdir(parent_directory):
            #print(file_name)
            file_path = parent_directory + '//' + file_name
            if os.path.isdir(file_path):
                self.delete_files(file_path)
            elif os.path.isfile(file_path) and not file_name.endswith('.py'):
                os.remove(file_path)
            else:
                continue

    def clean_up(self):
        self.unzip()
        self.delete_files(self.project_file_name[:-4])
