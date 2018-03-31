# coding=utf-8
"""
Created on 08/03/2018
Author: Ciarán
"""

import json

from FCI.FormattedCodeInterface import FormattedCodeInterface
import FCI.FCIConverter


def set_json_data(json_file):
    fci = FormattedCodeInterface()
    data = json.load(open(json_file))

    fci.set_author(data["items"][0]["owner"]["login"])
    fci.set_description(data["items"][0]["description"])
    fci.set_language(data["items"][0]["language"])
    fci.set_project_name(data["items"][0]["name"])
    #fci.set_quality(data["items"][0]["owner"])
    fci.set_save_time(data["items"][0]["owner"])
    fci.set_update_at(data["items"][0]["updated_at"])

    FCI.FCIConverter.to_json_file("json_files", fci)

    '''
    fci.set_author()
    fci.set_description()
    fci.set_language()
    fci.set_project_name()
    fci.set_quality()
    fci.set_save_time()
    fci.set_update_at()
    '''


def main():
    set_json_data('python_repo_page_100_1.json')


if __name__ == '__main__':
    main()
