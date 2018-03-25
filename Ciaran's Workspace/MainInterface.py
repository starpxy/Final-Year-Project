# coding=utf-8
"""
Created on 25/03/2018
Author: Ciarán
"""

from Server.LinuxConnection import LinuxConnection


def main():
    connection = LinuxConnection()
    path_to_file = "/home/ubuntu/Final-Year-Project/Ciaran's Workspace/Main.py"
    command = "pyhton3.5 " + path_to_file
    connection.exec_command(command)
    connection.close_connection()


if __name__ == '__main__':
    main()
