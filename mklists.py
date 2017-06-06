import re

def md2html(text_string):
    URL_REGEX = re.compile(r'''((?:mailto:|ftp://|http://)[^ <>'"{}|\\^`[\]]*)''')
    return URL_REGEX.sub(r'<a href="\1">\1</a>', text_string)


