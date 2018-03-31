# coding=utf-8
"""
Created on 06/03/2018
Author: Ciarán

Deletes all files in a directory except those specified by 'file_type'
"""

import os
import json

language_config_file_name = "language_config.json"
language_config_file = open(os.curdir + "/" + language_config_file_name)
language_data = json.load(language_config_file)


# Returns false if the given file ends with a file extension from languages_config
def can_delete_file(file):
    for classes, languages in language_data.items():
        for language, extensions in languages.items():
            for extension in extensions:
                if file.endswith(extension):
                    return False

    return True


# Recursively goes through each file in a directory and deletes those which aren't of a specified type
def delete_files(parent_directory):
    for file_name in os.listdir(parent_directory):
        file_path = parent_directory + '/' + file_name
        if os.path.isdir(file_path):
            delete_files(file_path)
        elif can_delete_file(file_name):
            os.remove(file_path)
        else:
            continue


def main():
    delete_files(os.curdir)


if __name__ == '__main__':
    main()
