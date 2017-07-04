class RuleLine(object):

    def __init__(self, text_line):
        self.line = text_line

    def strip_comments(self):
        self.line = self.line.partition('#')[0]
        return self


