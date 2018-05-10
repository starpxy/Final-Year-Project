# coding=utf-8
"""
Created on 31/03/2018
Author: Ciarán
"""

import unittest
import os
import json

from src.FCI.CreateJsonFiles import CreateJsonFiles


class CreateJsonFilesTest(unittest.TestCase):

    def setUp(self):
        self.cjf = CreateJsonFiles()
        self.cjf.file_paths = "file_paths.json"

        self.cjf.clean_projects_path = None
        self.cjf.unclean_projects_path = None
        self.cjf.so_questions = None
        self.cjf.python_json_path = None
        self.cjf.java_json_path = None
        self.cjf.so_json_path = None

        self.cjf.json_data = None
        self.cjf.project_info = {}

        self.cjf.load_file_paths()

    def test_load_file_paths(self):
        self.assertEqual(self.cjf.clean_projects_path, "test_files/clean")
        self.assertEqual(self.cjf.unclean_projects_path, "test_files/unclean")
        self.assertEqual(self.cjf.so_questions, "test_files/so_questions")
        self.assertEqual(self.cjf.python_json_path, "test_files/json_files/python")
        self.assertEqual(self.cjf.java_json_path, "test_files/json_files/java")
        self.assertEqual(self.cjf.so_json_path, "test_files/so_json_files")

    def test_get_info_from_so_files(self):
        self.cjf.get_info_from_so_files()

        json_files_created = len([name for name in os.listdir(self.cjf.so_json_path) if name.endswith(".json")])
        self.assertEqual(json_files_created, 3)

    def test_find_all_json_files(self):
        self.cjf.find_all_json_files()

        self.assertEqual(len(self.cjf.project_info), 1)

        actual_project_info = self.cjf.project_info["/github_projects/example_github_project"]
        example_json = open("test_files/unclean/github_projects/example_github_project.json")
        expected_project_info = json.load(example_json)
        self.assertEqual(actual_project_info, expected_project_info)
        example_json.close()

    def test_find_all_source_files(self):
        self.cjf.find_all_json_files()
        self.cjf.json_data = self.cjf.project_info["/github_projects/example_github_project"]
        self.cjf.find_all_source_files("test_files/clean")

        json_files_created = len([name for name in os.listdir("test_files/json_files/python") if name.endswith(".json")])
        self.assertEqual(json_files_created, 3)

