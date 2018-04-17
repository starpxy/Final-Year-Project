# coding=utf-8
"""
Created on 07/03/2018
Author: Ciarán

Runs all the code
"""

from Cleanup.CleanZippedProjects import CleanZippedProjects
from FCI.CreateJsonFiles import CreateJsonFiles
from Server.LinuxConnection import LinuxConnection


def main():
    connection = LinuxConnection()
    cleanup = CleanZippedProjects()
    create_json_files = CreateJsonFiles()

    cleanup.run()
    create_json_files.run()

    connection.close_connection()


if __name__ == '__main__':
    main()
