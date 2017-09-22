class ListLine(object):
    """@@@"""

    def __init__(self, line_of_list):
        self.line = line_of_list

    def linkified_line(self):
        """
        """
        URL_REGEX = re.compile(r"""((?:mailto:|git://|http://|https://)[^ <>'"{},|\\^`[\]]*)""")
        if '<a href=' in self.line:
            return self.line
        return URL_REGEX.sub(r'<a href="\1">\1</a>', self.line)

