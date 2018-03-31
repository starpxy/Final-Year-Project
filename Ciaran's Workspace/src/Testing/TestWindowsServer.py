# coding=utf-8
"""
Created on 06/03/2018
Author: Ciarán
"""

import paramiko

from src.Server.LinuxConnection import LinuxConnection


def main():
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname="118.89.233.227", username="ubuntu", password="Star==960906")
        print("Connection successful")
    except Exception as e:
        print("Could not connect: " + str(e))

    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname="123.206.68.82", username="ubuntu", password="Star==960906")
        print("Connection successful")
    except Exception as e:
        print("Could not connect: " + str(e))

    try:
        connection = LinuxConnection()
        stdin, stdout, stderr = connection.exec_command("ls")
        print(stdout.readlines())
    except Exception as e:
        print("Could not connect: " + str(e))


if __name__ == "__main__":
    main()
