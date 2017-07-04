import re

def md2html(text_string):
    URL_REGEX = re.compile(r'''((?:mailto:|git://|http://|https://)[^ <>'"{}|\\^`[\]]*)''')
    return URL_REGEX.sub(r'<a href="\1">\1</a>', text_string)

class ListLine():

    def __init__(self, line_of_list):
        self.line = line_of_list

    def linkify(self):
        """
        Given:
        * 'URL_REGEX': a compiled regex that matches URL strings
        * 'self': an instance of ListLine, a list of lines
        * 'self.line': one line of the list 'self'

        Return:
        * 'self', where 'self.line' has been modified to wrap URL strings in anchor tags
        """
        URL_REGEX = re.compile(r'''((?:mailto:|git://|http://|https://)[^ <>'"{}|\\^`[\]]*)''')
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

