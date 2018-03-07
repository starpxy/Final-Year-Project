# coding=utf-8
"""
Created on 06/03/2018
Author: Ciarán

Deletes all files in a directory except those specified by 'file_type'
"""

import os

file_type = ".py"

def delete_files(parent_directory):
    for file_name in os.listdir(parent_directory):
        file_path = parent_directory + '//' + file_name
        if os.path.isdir(file_path):
            delete_files(file_path)
        elif os.path.isfile(file_path) and not file_name.endswith(file_type):
            os.remove(file_path)
        else:
            continue


def main():
    delete_files(os.curdir)


if __name__ == '__main__':
    main()
