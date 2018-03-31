# coding=utf-8
"""
Created on 07/03/2018
Author: Ciarán
"""

import paramiko

def main():
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname="123.206.77.77", username="ubuntu", password="Star==960906")
        unzip_delete_command = "unzip /home/ubuntu/test_files/unclean/Final-Year-Project-Test.zip" \
                               " -d /home/ubuntu/test_files/clean " \
                               "&& rm /home/ubuntu/test_files/unclean/Final-Year-Project-Test.zip"
        stdin, stdout, stderr = ssh_client.exec_command(unzip_delete_command)
        print(stdin)
        print(stdout)
        print(stderr)
    except Exception as e:
        print(str(e))


if __name__ == '__main__':
    main()
