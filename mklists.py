import re

def md2html(text_string):
    URL_REGEX = re.compile(r'''((?:mailto:|ftp://|http://|https://)[^ <>'"{}|\\^`[\]]*)''')
    return URL_REGEX.sub(r'<a href="\1">\1</a>', text_string)

class ListLine():

    def __init__(self, line_of_list):
        self.line = line_of_list

    def urlify(self):
        URL_REGEX = re.compile(r'''((?:mailto:|ftp://|http://|https://)[^ <>'"{}|\\^`[\]]*)''')
        return URL_REGEX.sub(r'<a href="\1">\1</a>', self.line)


