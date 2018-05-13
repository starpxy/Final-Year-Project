# coding=utf-8
"""
Created on 13/05/2018
Author: Ciarán
"""

import os
import json

from LogWriter import LogWriter


class FilterLargeFiles:

    def __init__(self):
        self.file_paths = "file_paths.json"
        self.json_path = None

        self.log_writer = LogWriter()
        self.load_file_paths()

    def load_file_paths(self):
        file_paths_config_file = open(self.file_paths)
        file_paths = json.load(file_paths_config_file)
        file_paths_config_file.close()

        self.json_path = file_paths["Linux"]["master_json_dir"]

    def filter_files(self):
        for directory in os.listdir(self.json_path):
            if os.path.isdir(self.json_path + "/" + directory):
                for file in os.listdir(self.json_path + "/" + directory):
                    file_path = self.json_path + "/" + directory + "/" + file
                    if os.path.getsize(file_path) > 500000:
                        self.delete_and_record(file_path)

    def delete_and_record(self, file_path):
        self.log_writer.write_info_log("Deleting " + file_path)
        os.remove(file_path)


def main():
    flf = FilterLargeFiles()
    flf.filter_files()


if __name__ == '__main__':
    main()
