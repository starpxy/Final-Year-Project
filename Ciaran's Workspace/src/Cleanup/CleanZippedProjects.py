# coding=utf-8
"""
Created on 25/03/2018
Author: Ciarán
"""

import json
import os

from src.LogWriter import LogWriter


class CleanZippedProjects:

    def __init__(self):
        self.log_writer = LogWriter()
        self.unclean_projects_path = None
        self.clean_projects_path = None

    def load_file_paths(self):
        file_paths_config_file = open("file_paths.json")
        file_paths = json.load(file_paths_config_file)

        self.clean_projects_path = file_paths["Linux"]["clean_dir"]
        self.unclean_projects_path = file_paths["Linux"]["unclean_dir"]

    # Unzips all zipped folders in the directories in unclean to corresponding directories in clean
    def unzip(self):

        self.log_writer.write_info_log("Unzipping files")

        try:
            for directory in os.listdir(self.unclean_projects_path):
                if os.path.isdir(self.unclean_projects_path + "/" + directory):
                    for file in os.listdir(self.unclean_projects_path + "/" + directory):
                        file_path = self.unclean_projects_path + "/" + directory + "/" + file
                        if file.endswith(".zip"):
                            unzip_path = self.clean_projects_path + "/" + directory + "/" + file[:-4]

                            if not os.path.isdir(unzip_path):
                                os.makedirs(unzip_path)
                            else:
                                continue

                            unzip_command = "unzip " + file_path + " -d " + unzip_path
                            os.system(unzip_command)
                            self.log_writer.write_info_log(directory + "/" + file + " unzipped")

            self.log_writer.write_info_log("Files unzipped")
        except Exception as command_error:
            self.log_writer.write_error_log("Could not unzip files: " + str(command_error))

    def compare_projects(self):
        unclean_projects = []
        clean_projects = []

        for directory in os.listdir(self.unclean_projects_path):
            for project in os.listdir(self.unclean_projects_path + "/" + directory):
                if project.endswith(".zip"):
                    unclean_projects.append(project[:-4])

        for directory in os.listdir(self.clean_projects_path):
            if os.path.isdir(self.clean_projects_path + "/" + directory):
                for project in os.listdir(self.clean_projects_path + "/" + directory):
                    if os.path.isdir(self.clean_projects_path + "/" + directory + "/" + project):
                        clean_projects.append(project)

        for not_unzipped in set(unclean_projects).difference(clean_projects):
            self.log_writer.write_error_log("Could not unzip: " + not_unzipped)

    # Uses the delete_files_script to delete all files in a folder
    # who's extensions aren't in the language configuration file
    def delete_files(self):

        self.log_writer.write_info_log("Deleting unwanted files")

        try:
            os.system("cd /home/ubuntu/test_files/clean; python3 delete_unwanted_files.py")
            self.log_writer.write_info_log("Unwanted files deleted")
        except Exception as command_error:
            self.log_writer.write_error_log("Could not delete files: " + str(command_error))

    def run(self):
        self.load_file_paths()
        self.unzip()
        # Unzip and then delete files in one operation?
        # self.compare_projects()
        # self.delete_files()
