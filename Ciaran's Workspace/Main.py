# coding=utf-8
"""
Created on 07/03/2018
Author: Ciarán

Runs all the code
"""

from Cleanup.ProjectCleanUp import ProjectCleanUp
from FCI.FileDetailsToJson import FileDetailsToJson
from Server.LinuxConnection import LinuxConnection


def main():
    connection = LinuxConnection()
    cleanup = ProjectCleanUp(connection)
    tojson = FileDetailsToJson(connection)

    cleanup.run()
    tojson.run()

    connection.close_connection()


if __name__ == '__main__':
    main()
