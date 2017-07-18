import re

URL_REGEX = re.compile(r"""((?:mailto:|git://|http://|https://)[^ <>'"{},|\\^`[\]]*)""")

def md2html(text_string):
    URL_REGEX = re.compile(r'''((?:mailto:|git://|http://|https://)[^ <>'"{}|\\^`[\]]*)''')
    return URL_REGEX.sub(r'<a href="\1">\1</a>', text_string)

class ListLine():

    def __init__(self, line_of_list):
        self.line = line_of_list

    def linkified_line(self):
        """
        """
        FILE_REGEX = re.compile(r"""((/Users/tbaker|/home/tbaker)[^ <>'"{},|\\^`[\]]*)""")
        if '<a href=' in self.line:
            return self.line
        return URL_REGEX.sub(r'<a href="\1">\1</a>', self.line)

