"""@@@Docstring"""

import os
import datetime
from dataclasses import dataclass, field
from textwrap import dedent
from .decorators import preserve_cwd

# "Constants": hard-coded variables, not intended to be changed


@preserve_cwd
def _return_rootdir_pathname():
    """Return root pathname of mklists repo wherever executed in repo."""
    while "mklists.yml" not in os.listdir():
        cwd_before_changing = os.getcwd()
        os.chdir(os.pardir)
        if os.getcwd() == cwd_before_changing:
            return None
    return os.getcwd()


CONFIG_YAMLFILE_NAME = "mklists.yml"
RULES_CSVFILE_NAME = ".rules"
BACKUPDIR_NAME = "backups"
HTMLDIR_NAME = "html"
URL_PATTERN_REGEX = r"""((?:git://|http://|https://)[^ <>'"{}(),|\\^`[\]]*)"""
TIMESTAMP_STR = datetime.datetime.now().strftime("%Y-%m-%d_%H%M_%S%f")
VALID_FILENAME_CHARACTERS_REGEX = r"[\-_=.,@:A-Za-z0-9]+$"
STARTDIR_PATHNAME = os.getcwd()
ROOTDIR_PATHNAME = _return_rootdir_pathname()


@preserve_cwd
def _return_backupdir_shortname(rootdir_pathname=None, datadir_pathname=None):
    """@@@Docstring"""
    if rootdir_pathname == datadir_pathname:
        return "rootdir"
    return datadir_pathname[len(rootdir_pathname) :].strip("/").replace("/", "_")


# BACKUPDIR_PATHNAME = os.path.join(
#     ROOTDIR_PATHNAME, BACKUPDIR_NAME, BACKUPDIR_SHORTNAME, TIMESTAMP_STR
# )
# BACKUPDIR_SHORTNAME = _return_backupdir_shortname()


class Settings:
    """Holds settable settings."""

    # pylint: disable=too-few-public-methods
    # Not unreasonable to use a class instance as a namespace.

    def __init__(self):
        self.invalid_filename_regexes_list = [r"\.swp$", r"\.tmp$", r"~$", r"^\."]
        self.verbose = True
        self.htmlify = True
        self.backup_depth_int = 3
        self.files2dirs_dict = {}


settings_dict = vars(Settings())


@dataclass
class Samples:
    """Holds state and self-validation methods for examples."""

    datadira_name: str = "a"
    datadirb_name: str = "b"

    rootdir_rules_csvstr: str = dedent(
        r"""\
        # Each rule matches against part of a line of text.
        #
        # Each rule is a list with five components:
        # 1. Section of text line (integer) to be matched against regular expression:
        #    0 = entire line
        #    2 = second column (whitespace-delimited field)
        # 2. Regular expression against which the line will be matched.
        # 3. Filename of text line to be matched (see 1, above).
        # 4. Filename of target file where text line should be moved if it matches.
        # 5. Sort order (integer) of target file.
        #    0 = will sort on entire line
        #    2 = will sort on second column (whitespace-delimited field)
        #
        # Note:
        #   Integer values (1 and 5) must _not_ be quoted ("2"); this turns them into strings.
        #   If regular expressions contain backslashes, these must be escaped (e.g., "\\").
        #   Filenames (3 and 4) must be composed of valid characters.
        #   * In the YAML file, quotes may be omitted around filenames (unless the filenames
        #   * look like numbers).
        #   * By default, pathname slashes ('/'), spaces, and accented characters are illegal.
        #   * Set of valid filename characters can be configured in 'mklists.yml'.

        - [0, '.',       lines.tmp, alines,  0]
        - [0, '201.-..', alines,    blines,  1]
        """
    )

    minimal_datadira_rules_csvstr: str = dedent(
        r"""# Rules for Folder A.
        - [0, '.',          alines,    etc.txt,  0]
        - [1, 'TODO',       etc.txt,   todo.txt, 1]
        """
    )

    example_datadira_rules_csvstr: str = dedent(
        r"""
        - [0, '.',       alines,     todo.txt,   1]
        - [1, 'NOW',     todo.txt,   now.txt,    1]
        - [1, 'LATER',   todo.txt,   later.txt,  0]
        """
    )

    example_datadirb_rules_csvstr: str = dedent(
        r"""# Rules for folder B.
        - [0, '.',       lines,      blines,     0]
        - [1, '^2019',   blines,     2019.txt,   1]
        - [1, '^2020',   blines,     2020.txt,   0]
        """
    )

    example_datadira_textfile_name: str = "example_datalines_README.txt"

    example_datadira_textfile_str: str = dedent(
        r"""\
        TODO Examine config file 'mklists.yml' (in the root directory); tweak if needed.
        TODO Examine '.rules' file (in root directory); tweak if needed.
        TODO Examine 'a/.rules' file under root directory; tweak if needed.
        2019-08-14 Installed mklists <= this line will end up in 'b/log.txt'.
        LATER According to default rules, this line will end up in 'etc.txt'.
        """
    )

    example_datadirb_textfile_str: str = dedent(
        r"""\
        TODO Note how the default rules will move this line to Folder A.
        """
    )
