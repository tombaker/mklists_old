import re

def md2html(text_string):
    URL_REGEX = re.compile(r'''((?:mailto:|ftp://|http://|https://)[^ <>'"{}|\\^`[\]]*)''')
    return URL_REGEX.sub(r'<a href="\1">\1</a>', text_string)

class ListLine():

    def __init__(self, line_of_list):
        self.line = line_of_list

    def urlify(self):
        URL_REGEX = re.compile(r"""((?:mailto:|ftp://|http://|https://)[^ <>'"{}|\\^`[\]]*)""")
        if '<a href=' in self.line:
            return self
        self.line = URL_REGEX.sub(r'<a href="\1">\1</a>', self.line)
        return self

    def addbr(self):
        BR_REGEX = re.compile(r"""(.*)(\n)""")
        if '<br>' in self.line:
            return self
        self.line = BR_REGEX.sub(r'\1 <br>\2', self.line)
        return self


