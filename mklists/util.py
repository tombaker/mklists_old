__all__ = ['is_utf8', 'ls_files', 'abs_pathname', 'linkify']

import os
from mklists.exceptions import NotUTF8Error

def is_utf8(file):
    try:
        open(file).read(512)
    except UnicodeDecodeError as e:
        raise NotUTF8Error(f'File {file} not UTF-8: convert or delete, then retry.') from e

def ls_files(filenames=os.listdir(), config_file='mklists.yaml'):
    """
    Arguments:
    * filenames - default: os.listdir()
    * config_file - default: 'mklists.yaml'

    Checks 
    * first, for filenames matching showstopping patterns (swap filenames, backup filenames...)
    * then, filters out filenames 

    Returns: 
    * list of passing filenames, only for files

    FACTOR OUT ls_files_only??  
    * [f for f in passing_filenames if os.path.isfile(f)]
    * mustbetext?
    """
    #     with open(config_file) as mkl:
    #         config = yaml.load(mkl)
    #         
    #     no_showstoppers = []
    #     for filename in filenames:
    #         for regex_string in config['showstopping_filenames']:
    #             if re.search(regex_string, os.path.split(filename)[1]):
    #                 raise SystemExit("Show-stopper: filename {} matches blacklist pattern {}".format(filename, regex_string))
    #         no_showstoppers.append(filename)
    # 
    #     passing_filenames = []
    #     for filename in no_showstoppers:
    #         for regex_string in config['ignored_filenames']:
    #             if not re.search(config['ignored_filenames'][0], filename):
    #                 passing_filenames.append(filename)
    # 
    #     return [f for f in passing_filenames if os.path.isfile(f)]

def abs_pathname(pathname):
    """
    Given: 
    * the relative or absolute pathname of a file or directory

    Returns: 
    * the absolute name, if the file or directory exists
    * None, if the file or directory does not exit

    >>> abs_pathname('./mklists.py')
    '/Users/tbaker/github/tombaker/mklists/mklists/mklists.py'
    >>> abs_pathname('/Users/tbaker/github/tombaker/mklists/mklists/mklists.py')
    '/Users/tbaker/github/tombaker/mklists/mklists/mklists.py'
    >>> abs_pathname('~/github/tombaker/mklists')
    '/Users/tbaker/github/tombaker/mklists'
    >>> abs_pathname('../../../../github/tombaker/mklists')
    '/Users/tbaker/github/tombaker/mklists'
    >>> abs_pathname('../github/tombaker/mklists')
    """
    absolute_pathname = os.path.abspath(os.path.expanduser(pathname))
    if os.path.exists(absolute_pathname):
        return absolute_pathname
    else:
        return None

def linkify(string):
    """
    2017-07-18 Puts HTML links around URLs found in a string.
    """
    URL_REGEX = re.compile(r"""((?:mailto:|git://|http://|https://)[^ <>'"{},|\\^`[\]]*)""")
    if '<a href=' in string:
        return string
    return URL_REGEX.sub(r'<a href="\1">\1</a>', string)

if __name__ == "__main__":
    import doctest
    doctest.testmod()

# from mkl import ListLine
# 
# def test_linkified_line_already_linkified():
#     x = ListLine('A line with <a href="http://example.org">http://example.org</a>.\n')
#     output_line = """A line with <a href="http://example.org">http://example.org</a>.\n"""
#     assert x.linkified_line() == output_line
# 
# def test_linkified_line():
#     x = ListLine('http://example.org')
#     output_line = """<a href="http://example.org">http://example.org</a>"""
#     assert x.linkified_line() == output_line
# 
# def test_linkified_line_non_url():
#     """Shows that function does not test for non-sensical URLs."""
#     x = ListLine('http://...')
#     output_line = """<a href="http://...">http://...</a>"""
#     assert x.linkified_line() == output_line
# 
# def test_linkified_line_url_with_question_mark():
#     x = ListLine('http://192.168.2.1/html/login/status.html?lang=en')
#     output_line = """<a href="http://192.168.2.1/html/login/status.html?lang=en">http://192.168.2.1/html/login/status.html?lang=en</a>"""
#     assert x.linkified_line() == output_line
# 
# def test_linkified_line_url_with_ip_address():
#     x = ListLine('http://192.168.56.100:8888/')
#     output_line = """<a href="http://192.168.56.100:8888/">http://192.168.56.100:8888/</a>"""
#     assert x.linkified_line() == output_line
# 
# def test_linkified_line_url_with_3D():
#     x = ListLine('http://carnegieeurope.eu/strategiceurope/?fa=3D64063=')
#     output_line = """<a href="http://carnegieeurope.eu/strategiceurope/?fa=3D64063=">http://carnegieeurope.eu/strategiceurope/?fa=3D64063=</a>"""
#     assert x.linkified_line() == output_line
# 
# def test_linkified_line_url_with_hashsign():
#     x = ListLine('http://ctrlpvim.github.io/ctrlp.vim/#installation')
#     output_line = """<a href="http://ctrlpvim.github.io/ctrlp.vim/#installation">http://ctrlpvim.github.io/ctrlp.vim/#installation</a>"""
#     assert x.linkified_line() == output_line
# 
# def test_linkified_line_url_with_colon():
#     x = ListLine('http://en.wikipedia.org/wiki/Talk:Dublin_Core')
#     output_line = """<a href="http://en.wikipedia.org/wiki/Talk:Dublin_Core">http://en.wikipedia.org/wiki/Talk:Dublin_Core</a>"""
#     assert x.linkified_line() == output_line
# 
# def test_linkified_line_url_with_escaped_characters():
#     x = ListLine('http://en.wikipedia.org/wiki/USS_Rizzi_%28DE-537%29')
#     output_line = """<a href="http://en.wikipedia.org/wiki/USS_Rizzi_%28DE-537%29">http://en.wikipedia.org/wiki/USS_Rizzi_%28DE-537%29</a>"""
#     assert x.linkified_line() == output_line
# 
# def test_linkified_line_url_with_colon2():
#     x = ListLine('http://explore.dublincore.net/rdf/lrmi/#/resource')
#     output_line = """<a href="http://explore.dublincore.net/rdf/lrmi/#/resource">http://explore.dublincore.net/rdf/lrmi/#/resource</a>"""
#     assert x.linkified_line() == output_line
# 
# def test_linkified_line_url_with_bang():
#     x = ListLine('http://twitter.com/#!/search/%23dcmi11')
#     output_line = """<a href="http://twitter.com/#!/search/%23dcmi11">http://twitter.com/#!/search/%23dcmi11</a>"""
#     assert x.linkified_line() == output_line
# 
# def test_linkified_line_url_with_comma():
#     """This application will not accept commas as valid URL characters."""
#     x = ListLine('http://standorte.deutschepost.de,')
#     output_line = """<a href="http://standorte.deutschepost.de">http://standorte.deutschepost.de</a>,"""
#     assert x.linkified_line() == output_line
# 
# def test_linkified_line_url_with_https():
#     x = ListLine('https://www.w3.org/2013/data/CG/wiki')
#     output_line = """<a href="https://www.w3.org/2013/data/CG/wiki">https://www.w3.org/2013/data/CG/wiki</a>"""
#     assert x.linkified_line() == output_line
# 
# def test_linkified_line_surrounded_by_brackets():
#     x = ListLine('see info (https://www.w3.org/2013/data/CG/wiki)')
#     output_line = """see info (<a href="https://www.w3.org/2013/data/CG/wiki">https://www.w3.org/2013/data/CG/wiki</a>)')"""
# 
# def test_linkified_line_with_two_urls():
#     x = ListLine('see info (https://example1.org), http://example2.org')
#     output_line = """see info (<a href="https://example1.org">https://example1.org</a>), <a href="http://example2.org">http://example2.org</a>)"""

