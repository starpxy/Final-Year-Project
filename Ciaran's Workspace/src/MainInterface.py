# coding=utf-8
"""
Created on 25/03/2018
Author: Ciarán
"""

from Server.LinuxConnection import LinuxConnection


def main():
    connection = LinuxConnection()
    file = "Main.py"
    #path_to_file = "/home/ubuntu/Final-Year-Project/Ciaran's Workspace/src/"
    '''path_to_file = "Final-Year-Project/Ciaran\\'s\ Workspace/src/"
    change_directory = "cd " + path_to_file
    run_file = "pyhton3.5 " + file
    command = change_directory + "; " + run_file'''
    command = "cd /home/ubuntu/Final-Year-Project/Ciaran\\'s\ Workspace/src/; python3.5 Main.py"
    connection.exec_command(command)
    '''print(command)
    si, so, se = connection.exec_command(command)
    print(se.read())
    print(so.read())'''
    connection.close_connection()


if __name__ == '__main__':
    main()
