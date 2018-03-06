# coding=utf-8
"""
Created on 04/03/2018
Author: Ciarán
"""

from process.ProjectCleanUp import *
# from paramiko import sftp_client, SSHClient
import paramiko
import zipfile


class Main:

    def __init__(self):
        pass

    if __name__ == "__main__":
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print("Connecting . . .")
        ssh_client.connect(hostname="123.206.77.77", username="ubuntu", password="Star==960906")
        ftp = ssh_client.open_sftp()
        print("Connected!")
        dirs = ftp.listdir()
        print(dirs)
        ftp.chdir('/home/ubuntu/test_files')
        print(dirs)
        ssh_client.exec_command("cd /home/ubuntu/test_files;"
                                "unzip /home/ubuntu/test_files/Final-Year-Project.zip")
        # print(stdout.readlines())
        # stdin, stdout, stderr = ssh_client.exec_command("unzip /home/ubuntu/test_files/Final-Year-Project.zip")

        # Go to test_files folder
        # run command 'unzip /home/ubuntu/test_files/Final-Year-Project.zip'
        # zip will be in test_files

        '''
        print(ssh_client.exec_command("ls"))
        print(ssh_client.exec_command("cd test_files"))
        print(ssh_client.exec_command("ls"))
        print(ftp.listdir())

        for file_name in ftp.listdir("/home/ubuntu/test_files"):
            print(file_name)
            project_file = zipfile.ZipFile(file_name)
            project_file.extractall(file_name[:-4])
            project_file.close()
        '''

        pcu = ProjectCleanUp('C:\\Users\\CeXGalway\\Downloads\\Final-Year-Project.zip')
        pcu.clean_up()

        ssh_client.close()
