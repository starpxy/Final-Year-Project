# coding=utf-8
"""
Created on 31/03/2018
Author: Ciarán
"""

import unittest

from src.Server.LinuxConnection import LinuxConnection


class LinuxConnectionTest(unittest.TestCase):

    def setUp(self):
        self.connection = LinuxConnection()
        self.connection.open_linux_connection()

    def test_open_file(self):
        file_path = "/home/ubuntu/LogWriter.py"
        self.connection.open_file(file_path)

    def test_copy_file_to_server(self):
        self.connection.copy_file_to_server("test.txt", "/home/ubuntu/test_files")
        self.connection.open_file("/home/ubuntu/test_files/test.txt")

    def test_isdir_correctly_identifies_directories(self):
        real_dir = "/home/ubuntu/test_files"
        fake_dir = "/home/ubuntu/fake_dir"
        real_file = "/home/ubuntu/LogWriter.py"

        self.assertTrue(self.connection.isdir(real_dir))
        self.assertFalse(self.connection.isdir(fake_dir))
        self.assertFalse(self.connection.isdir(real_file))

    def test_mkdir(self):
        pass

    def test_listdir(self):
        pass

    def test_exec_command(self):
        pass

    def tearDown(self):
        #self.connection.exec_command("rm /home/ubuntu/test_files/test.txt")
        self.connection.close_connection()
