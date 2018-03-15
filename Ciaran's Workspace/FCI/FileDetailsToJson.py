# coding=utf-8
"""
Created on 06/03/2018
Author: Ciarán

Gets all the info from the files in a project and stores them in a json file
"""

import os
import re
import json

from FCI.FormattedCodeInterface import FormattedCodeInterface
from LogWriter import LogWriter
import FCI.FCIConverter
from Server.LinuxConnection import LinuxConnection


class FileDetailsToJson:

    def __init__(self, connection):
        self.local_path = "../Hester'sWorkSpace/files"
        self.clean_projects_path = None
        self.unclean_projects_path = None
        self.remote_json_path = None

        self.json_data = None
        self.files_in_project = []
        self.project_info = {}  # Dictionary with project names and containing directory as key and corresponding json data as value

        self.log_writer = LogWriter()
        self.connection = connection

    def load_file_paths(self):
        file_paths_config_file = open("../file_paths.json")
        file_paths = json.load(file_paths_config_file)

        self.clean_projects_path = file_paths["Linux"]["clean_dir"]
        self.unclean_projects_path = file_paths["Linux"]["unclean_dir"]
        self.remote_json_path = file_paths["Linux"]["json_dir"]

    # For each json file from Kirk find the corresponding clean project
    # For each file within that project crete an fci object with the details of that file
    def run(self):
        self.load_file_paths()
        self.find_all_json_files()

        for project_name in self.project_info:
            self.json_data = self.project_info[project_name]
            self.create_fci_objects(self.clean_projects_path + project_name)

        self.save_fci_objects_to_json_files()

    # Goes through each unclean folder and searches for all json files from Kirk
    # When a file is found it saves it to a directory with the folder and file name as a key
    # and the json data as the element
    def find_all_json_files(self):
        for directory in self.connection.listdir(self.unclean_projects_path):
            for file in self.connection.listdir(self.unclean_projects_path + "/" + directory):
                if file.endswith(".json"):
                    json_path = "/" + directory + "/" + file
                    json_file = self.connection.open_file(self.unclean_projects_path + json_path)
                    self.project_info[json_path[:-5]] = json.load(json_file)

    # Goes through all files in a cleaned project and creates an fci object for each
    def create_fci_objects(self, parent_directory):
        try:
            for file_name in self.connection.listdir(parent_directory):
                file_path = parent_directory + '/' + file_name
                if file_name.endswith(".py"):
                    self.save_file_details_to_fci_object(file_path, file_name)
                else:
                    if self.connection.isdir(file_path):
                        self.create_fci_objects(file_path)
                    else:  # Just an extra check to make sure no other files are left
                        self.log_writer.write_warning_log(file_path + " not deleted:" + "\n")
        except Exception as e:
            self.log_writer.write_error_log(str(e) + "\n")

    # Saves the details of an individual file to an fci object
    def save_file_details_to_fci_object(self, file_path, file_name):
        fci = FormattedCodeInterface()

        fci.set_file_name(file_name)
        fci.set_save_path(file_path)
        self.set_content(file_path, fci)
        self.set_project_details(fci)

        self.files_in_project.append(fci)
        self.log_writer.write_info_log(file_path + " documented.")

    # Save the content, code, and comments of an individual file to an fci object
    def set_content(self, file_path, fci):
        file = self.connection.open_file(file_path)
        content = ''
        comments_list = []
        comments = ''
        python_comments = ['\"\"\"((.|\n)*)\"\"\"', '\'\'\'((.|\n)*)\'\'\'', '#.*']

        # Content
        for line in file.readlines():
            content += line
        fci.set_content(content)

        # Code
        code = content
        for comment_pattern in python_comments:
            comments_list += re.findall(comment_pattern, code)
            code = re.sub(comment_pattern, '', code)
        fci.set_code(code)

        # Comments
        for recorded_comment in comments_list:
            if type(recorded_comment) is tuple:
                for comment in recorded_comment:
                    comments += comment + '\n'
            else:
                comments += recorded_comment + '\n'
        fci.set_comments(comments)

    # Saves the details of the current project to an fci object
    def set_project_details(self, fci):
        fci.set_author(self.json_data["owner_name"])
        fci.set_description(self.json_data["description"])
        fci.set_language(self.json_data["language"])
        fci.set_project_name(self.json_data["name"])
        # fci.set_quality(data["items"][0]["owner"])
        # fci.set_save_time()
        fci.set_update_at(self.json_data["updated_at"])
        fci.set_url(self.json_data["html_url"])
        fci.set_wiki(self.json_data["has_wiki"])

    # Save fci objects to local and remote json files
    def save_fci_objects_to_json_files(self):
        self.log_writer.write_info_log("Saving Json files")
        self.save_to_local_directory()
        self.save_to_remote_directory()

    # Converts fci objects to json files and saves them locally
    def save_to_local_directory(self):
        for fci_object in self.files_in_project:
            FCI.FCIConverter.to_json_file(self.local_path, fci_object)

        self.log_writer.write_info_log("Saved to local machine at " + os.path.realpath(self.local_path))

    # Save json files from local directory to remote directory
    def save_to_remote_directory(self):
        for file in os.listdir(self.local_path):
            local_path = self.local_path + "/" + file
            remote_path = self.remote_json_path + "/" + file
            self.connection.copy_file_to_server(local_path, remote_path)

        self.log_writer.write_info_log("Saved to remote machine at " + self.remote_json_path)


def main():
    FileDetailsToJson(LinuxConnection()).run()


if __name__ == '__main__':
    main()
