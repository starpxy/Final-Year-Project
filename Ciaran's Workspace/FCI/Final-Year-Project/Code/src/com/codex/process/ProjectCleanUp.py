# coding=utf-8
"""
Created on 04/03/2018
Author: Ciarán
"""

import zipfile


class ProjectCleanUp:

    def __init__(self, project_file_name):
        self.project_file_name = project_file_name

    def fixBadZipfile(self, zipFile):
        f = open(zipFile, 'r+b')
        data = f.read()
        pos = data.find('\x50\x4b\x05\x06')  # End of central directory signature
        if (pos > 0):
            f.seek(pos + 22)  # size of 'ZIP end of central directory record'
            f.truncate()
            f.close()

    def unzip(self):
        print self.project_file_name
        #self.fixBadZipfile(self.project_file_name)
        #project_file = zipfile.ZipFile(self.project_file_name)
        print zipfile.is_zipfile("C:\\Users\\CeXGalway\\Downloads\\BBS-master.zip")
        project_file = zipfile.ZipFile("C:\\Users\\CeXGalway\\Downloads\\BBS-master.zip")
        project_file.extractall(self.project_file_name[:-4])
        project_file.close()