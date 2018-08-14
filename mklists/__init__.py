import string

VALID_FILENAME_CHARS = '@:-_=.{}{}'.format(string.ascii_letters, string.digits)

URL_PATTERN = r"""((?:git://|http://|https://)[^ <>'"{}(),|\\^`[\]]*)"""
__all__ = [
    'URL_PATTERN',
    'VALID_FILENAME_CHARS'
]

