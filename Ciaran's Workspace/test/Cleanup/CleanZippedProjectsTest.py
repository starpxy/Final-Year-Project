# coding=utf-8
"""
Created on 31/03/2018
Author: Ciarán
"""

import unittest
import os

from src.Cleanup.CleanZippedProjects import CleanZippedProjects


class CleanZippedProjectsTest(unittest.TestCase):

    def setUp(self):
        self.czp = CleanZippedProjects()

        self.czp.file_paths = "file_paths.json"
        self.czp.unclean_projects_path = None
        self.czp.clean_projects_path = None

        self.czp.load_file_paths()

    def test_load_file_paths(self):
        self.assertEqual(self.czp.unclean_projects_path, "test_files/unclean")
        self.assertEqual(self.czp.clean_projects_path, "test_files/clean")

    # I can't actually test if the file is unzipped because the command to do so is for linux
    def test_unzip(self):
        self.czp.unzip()

        self.assertTrue(os.path.isdir("test_files/clean/python/example_python_project"))
