from search.supportings.FormattedCodeInterface import FormattedCodeInterface

class FrontEndInterface:
    __fci_obj = FormattedCodeInterface()
    __match_lines = ''

    def __init__(self,fci_obj,match_lines):
        self.__fci_obj = fci_obj
        self.__match_lines = match_lines

    def set_fci_obj(self,fci_obj):
        self.__fci_obj = fci_obj

    def get_fci_obj(self):
        return self.__fci_obj

    def set_match_lines(self,match_lines):
        self.__match_lines = match_lines

    def get_match_lines(self):
        return self.__match_lines