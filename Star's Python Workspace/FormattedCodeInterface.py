'''
@author: Star

@time: 06-03-2018

This is an Interface class for Ciaran to transfer his information to Hester

Every single object represents one file

'''

class FormattedCodeInterface:

    __description = ''
    __author = ''
    __update_at = ''
    __save_time = ''
    __file_name = ''
    __project_name=''
    __save_path = ''
    __language = ''
    __quality = ''
    __content = ''

    def __init__(self,description='',author='',update_at='',save_time='',file_name='',project_name='',save_path='',language='',quality='',content=''):
        self.__description = description
        self.__author = author
        self.__update_at = update_at
        self.__save_time = save_time
        self.__file_name = file_name
        self.__project_name = project_name
        self.__save_path = save_path
        self.__language = language
        self.__quality = quality
        self.__content = content

    def set_description(self,description):
        self.__description = description

    def get_description(self):
        return self.__description

    def set_author(self,author):
        self.__author = author

    def get_author(self):
        return self.__author

    def set_update_at(self,update_at):
        self.__update_at = update_at

    def get_update_at(self):
        return self.__update_at

    def set_save_time(self,save_time):
        self.__save_time = save_time

    def get_save_time(self):
        return self.__save_time

    def set_file_name(self,file_name):
        self.__file_name = file_name

    def get_file_name(self):
        return self.__file_name

    def set_project_name(self,project_name):
        self.__project_name = project_name

    def get_project_name(self):
        return self.__project_name

    def set_save_path(self,save_path):
        self.__save_path = save_path

    def get_save_path(self):
        return self.__save_path

    def set_language(self,language):
        self.__language = language

    def get_language(self):
        return self.__language

    def set_quality(self,quality):
        self.__quality = quality

    def get_quality(self):
        return self.__quality

    def set_content(self,content):
        self.__content = content

    def get_content(self):
        return self.__content

    def to_dictionary(self):
        dic = {}
        dic["description"] = self.__description
        dic["author"] = self.__author
        dic["update_at"] = self.__update_at
        dic["save_time"] = self.__save_time
        dic["file_name"] = self.__file_name
        dic["project_name"] = self.__project_name
        dic["save_path"] = self.__save_path
        dic["language"] = self.__language
        dic["quality"] = self.__quality
        dic["content"] = self.__content
        return dic