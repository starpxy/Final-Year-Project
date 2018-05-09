# coding=utf-8
"""
Created on 23/03/2018
Author: Ciarán
"""

import re
import json
import os
import nltk
import sys
import socket
import csv

from FCI.FormattedCodeInterface import FormattedCodeInterface
from LogWriter import LogWriter
import FCI.FCIConverter as FCIConverter
from Server.LinuxConnection import LinuxConnection
from NLTK.NLTKFormatter import NLTKFormatter


class CreateJsonFiles:

    def __init__(self):
        self.file_paths = "file_paths.json"

        self.clean_projects_path = None
        self.unclean_projects_path = None
        self.so_questions = None
        # self.master_json_path = None
        self.python_json_path = None
        self.java_json_path = None
        self.so_json_path = None
        # self.so_python_json_path = None
        # self.so_java_json_path = None

        self.json_data = None
        # Dictionary with project names and containing directory as keys and their corresponding json data as values
        self.project_info = {}

        self.connection = None

        self.log_writer = LogWriter()

    # For each json file from Kirk find the corresponding clean project
    # For each file within that project crete an fci object with the details of that file
    def run(self):
        self.open_connection()
        self.load_file_paths()
        self.find_all_json_files()
        self.get_info_from_so_files()

        for project_name in self.project_info:
            # If project_name is not in clean:
            # if self.not_cleaned(self.clean_projects_path, project_name):
            self.json_data = self.project_info[project_name]
            self.find_all_source_files(self.clean_projects_path + project_name)

        self.log_writer.write_info_log("All json files created.")
        self.close_connection()

    # Open a connection to the master server if on a slave server
    def open_connection(self):
        if socket.gethostname() != "VM-131-14-ubuntu":
            self.connection = LinuxConnection()

    def close_connection(self):
        if self.connection is not None:
            self.connection.close_connection()

    def load_file_paths(self):
        file_paths_config_file = open(self.file_paths)
        file_paths = json.load(file_paths_config_file)

        self.clean_projects_path = file_paths["Linux"]["clean_dir"]
        self.unclean_projects_path = file_paths["Linux"]["unclean_dir"]
        self.so_questions = file_paths["Linux"]["so_questions"]
        # self.master_json_path = file_paths["Linux"]["master_json_dir"]
        self.python_json_path = file_paths["Linux"]["python_json_dir"]
        self.java_json_path = file_paths["Linux"]["java_json_dir"]
        self.so_json_path = file_paths["Linux"]["so_json_dir"]
        # self.so_python_json_path = file_paths["Linux"]["so_python_json_dir"]
        # self.so_java_json_path = file_paths["Linux"]["so_java_json_dir"]

        file_paths_config_file.close()

        # if self.connection is not None:
            # self.master_json_path = file_paths["Linux"]["master_json_files"]

    def not_cleaned(self, clean_project, project_name):
        for directory in self.connection.listdir(clean_project):
            if directory == project_name:
                return False
            else:
                self.not_cleaned(clean_project + "/" + directory, project_name)

    # Goes through each line in the StackOverflow text files
    # Saves each question and corresponding answer to an FCI object
    def get_info_from_so_files(self):
        nltk_formatter = NLTKFormatter()

        for file_name in os.listdir(self.so_questions):
            file_path = self.so_questions + "/" + file_name
            self.log_writer.write_info_log("Reading StackOverflow questions from " + file_name)

            '''
            json_file_path = ""
            if file_name == "python_title_answer.txt":
                json_file_path = self.so_python_json_path
            else:
                json_file_path = self.so_java_json_path
            '''

            with open(file_path, 'r', encoding='UTF-8') as tsv:
                for line in csv.reader(tsv, dialect="excel-tab"):
                    try:
                        fci_object = FormattedCodeInterface()
                        fci_object.set_content(nltk_formatter.format_sentence(line[2]))
                        fci_object.set_code(line[3])
                        self.save_fci_object_to_json_files(fci_object, self.so_json_path)
                        self.log_writer.write_info_log("Reading StackOverflow question " + line[0])
                    except Exception as e:
                        self.log_writer.write_error_log(e)

    # Goes through each unclean folder and searches for all json files from Kirk
    # When a file is found it saves it to a directory with the folder and file name as a key
    # and the json data as the element
    def find_all_json_files(self):
        for directory in os.listdir(self.unclean_projects_path):
            projects = self.unclean_projects_path + "/" + directory
            if os.path.isdir(projects):
                self.log_writer.write_info_log("Reading jsons from " + directory)
                for file in os.listdir(projects):
                    if file.endswith(".json"):
                        json_path = "/" + directory + "/" + file
                        json_file = open(self.unclean_projects_path + json_path)
                        # Save the json_path without '.json' at the end to get the name of the unzipped project
                        self.project_info[json_path[:-5]] = json.load(json_file)
                        json_file.close()

    # Goes through all files in a cleaned project and creates an fci object for each
    # Initially the path to a project is passed and the function recursively goes through all files in the project
    def find_all_source_files(self, parent_directory):
        curr_file_path = ''
        try:
            for file_name in os.listdir(parent_directory):
                file_path = parent_directory + '/' + file_name
                curr_file_path = file_path
                if (file_name.endswith(".py") and file_name != "__init__.py") or file_name.endswith(".java"):
                    self.save_file_details_to_fci_object(file_path, file_name)
                elif os.path.isdir(file_path):
                    self.find_all_source_files(file_path)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            self.log_writer.write_error_log("At line %d: %s in %s" % (exc_tb.tb_lineno, str(e), curr_file_path))

    # Saves the details of an individual file to an fci object
    def save_file_details_to_fci_object(self, file_path, file_name):
        fci_object = FormattedCodeInterface()

        fci_object.set_file_name(file_name)
        fci_object.set_save_path(file_path)
        # self.set_content(file_path, fci_object)

        # Content
        file = open(file_path, encoding='UTF-8')
        content = ''
        for line in file.readlines():
            content += line
        fci_object.set_content(content)

        self.set_project_details(fci_object)

        if file_path.endswith(".py"):
            self.save_fci_object_to_json_files(fci_object, self.python_json_path, file_name)
        else:
            self.save_fci_object_to_json_files(fci_object, self.java_json_path, file_name)

        self.log_writer.write_info_log(file_name + " saved to server at " + file_path)

    # Save the content, code, and comments of an individual file to an fci object
    def set_content(self, file_path, fci_object):
        file = open(file_path)
        content = ''
        comments_list = []
        comment_patterns = []

        if file_path.endswith(".py"):
            comment_patterns = ['\"\"\"((.|\n)*)\"\"\"', '\'\'\'((.|\n)*)\'\'\'', '(?<!(\"|\'))#.*(?=\n)']
        else:
            comment_patterns = ['//.*|(\"(?:\\\\[^\"]|\\\\\"|.)*?\")|(?s)/\\*.*?\\*/']
            # (?:/\\*(?:[^*]|(?:\\*+[^*/]))*\\*+/)|(?://.*)

        # Content
        for line in file.readlines():
            content += line
        fci_object.set_content(content)

        # Code
        code = content
        for comment_pattern in comment_patterns:
            for match in re.finditer(comment_pattern, code):
                comments_list.append(self.format_comments(match.group(0)))
                code = re.sub(match.group(0), '', code)
        fci_object.set_code(code)

        # Comments
        comments = ' '.join(comments_list)
        fci_object.set_comments(comments)

    def format_comments(self, comment):
        formatted_comment = ''
        alnum_pattern = r'[^(a-zA-Z0-9)]'
        stopwords = set(nltk.corpus.stopwords.words('english'))

        comment = re.sub(alnum_pattern, ' ', comment)

        for word in comment.split(' '):
            if word not in stopwords:
                formatted_comment += str(word) + ' '

        return formatted_comment.lower()

    # Saves the details of the current project to an fci object
    def set_project_details(self, fci_object):
        fci_object.set_author(self.json_data["owner_name"])
        fci_object.set_description(self.json_data["description"])
        fci_object.set_language(self.json_data["language"])
        fci_object.set_project_name(self.json_data["name"])
        # fci.set_quality(data["items"][0]["owner"])
        # fci.set_save_time()
        fci_object.set_update_at(self.json_data["updated_at"])
        fci_object.set_url(self.json_data["html_url"])
        fci_object.set_wiki(self.json_data["has_wiki"])

    # Converts fci object to json file and saves it to the server
    # Also saves the json files to the master server if on a slave
    def save_fci_object_to_json_files(self, fci_object, json_file_path, file_name = "StackOverflow question"):
        FCIConverter.to_local_json_file(json_file_path, fci_object)

        if self.connection is not None:
            # FCIConverter.to_master_json_file(self.master_json_path, fci_object, self.connection)
            FCIConverter.to_master_json_file(json_file_path, fci_object, self.connection)
            self.log_writer.write_info_log(file_name + " saved to master server")
