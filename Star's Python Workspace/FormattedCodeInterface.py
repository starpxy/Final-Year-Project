'''
@author: Star

@time: 06-03-2018

@update_at 06-03-2018 night

This is an Interface class for Ciaran to transfer his information to Hester

Every single object represents one file

'''


class FormattedCodeInterface:
    __description = ''
    __author = ''
    __update_at = ''  # Last commit
    __save_time = ''  # When I create the json file
    __file_name = ''
    __project_name = ''
    __save_path = ''  # On server
    __language = ''
    __quality = ''  # For Later
    __content = ''
    __code = ''  # Content minus comments
    __comments = ''  # Content minus code
    __source = ''
    __url = ''
    __id = ''
    __wiki = False  # Whether the project has a wiki or not

    def __init__(self, description='', author='', update_at='', save_time='', file_name='', project_name='',
                 save_path='',
                 language='', quality='', content='', code='', comments='', source='', url='', wiki=False):
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
        self.__code = code
        self.__comments = comments
        self.__source = source
        self.__url = url
        self.__wiki = wiki

    def set_description(self, description):
        self.__description = description

    def get_description(self):
        return self.__description

    def set_author(self, author):
        self.__author = author

    def get_author(self):
        return self.__author

    def set_update_at(self, update_at):
        self.__update_at = update_at

    def get_update_at(self):
        return self.__update_at

    def set_save_time(self, save_time):
        self.__save_time = save_time

    def get_save_time(self):
        return self.__save_time

    def set_file_name(self, file_name):
        self.__file_name = file_name

    def get_file_name(self):
        return self.__file_name

    def set_project_name(self, project_name):
        self.__project_name = project_name

    def get_project_name(self):
        return self.__project_name

    def set_save_path(self, save_path):
        self.__save_path = save_path

    def get_save_path(self):
        return self.__save_path

    def set_language(self, language):
        self.__language = language

    def get_language(self):
        return self.__language

    def set_quality(self, quality):
        self.__quality = quality

    def get_quality(self):
        return self.__quality

    def set_content(self, content):
        self.__content = content

    def get_content(self):
        return self.__content

    def set_code(self, code):
        self.__code = code

    def get_code(self):
        return self.__code

    def set_comments(self, comments):
        self.__comments = comments

    def get_comments(self):
        return self.__comments

    def set_source(self, source):
        self.__source = source

    def get_source(self):
        return self.__source

    def set_url(self, url):
        self.__url = url

    def get_url(self):
        return self.__url

    def set_wiki(self, wiki):
        self.__wiki = wiki

    def get_wiki(self):
        return self.__wiki

    def get_id(self):
        return self.__id

    def set__id(self, id):
        self.__id = id

    # convert FCI object into dictionary.
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
        dic["code"] = self.__code
        dic["comments"] = self.__comments
        dic["wiki"] = self.__wiki
        dic["url"] = self.__url
        dic["source"] = self.__source
        dic["id"] = self.__id
        return dic

    # convert dictionary into FCI objects.
    def from_dictionary(self, dic):
        fci = FormattedCodeInterface()
        fci.set_author(dic["author"])
        fci.set_content(dic["content"])
        fci.set_description(dic["description"])
        fci.set_file_name(dic["file_name"])
        fci.set_language(dic["language"])
        fci.set_project_name(dic["project_name"])
        fci.set_quality(dic["quality"])
        fci.set_save_path(dic["save_path"])
        fci.set_save_time(dic["save_time"])
        fci.set_update_at(dic["update_at"])
        fci.set_code(dic["code"])
        fci.set_comments(dic["comments"])
        fci.set_wiki(dic["wiki"])
        fci.set_url(dic["url"])
        fci.set_source(dic["source"])
        fci.set__id(dic["id"])
        return fci
