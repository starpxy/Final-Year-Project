# coding=utf-8
"""
Created on 07/03/2018
Author: Ciarán

Runs all the code
"""

from Cleanup.ProjectCleanUp import ProjectCleanUp
from FCI.GetProjectInfo import GetProjectInfo
from Server.Connection import Connection

def main():
    cleanup = ProjectCleanUp
    getinfo = GetProjectInfo
    connection = Connection

    cleanup().run()
    getinfo().run()

    connection.close_connection()


if __name__ == '__main__':
    main()
