"""@@@Docstring"""

import os
import datetime
from dataclasses import dataclass, field
from textwrap import dedent
import attr

# Note: variables set only at command line:
#     cli:  [config]
#     init: [config] with_examples [directory - add this]
#     run:  [config] dryrun here_only


class Defaults:
    """Holds variables 'hard-coded' into mklists -
    variables not intended to be changed.
    Could add validation methods here, then re-allow
    R0903 in pylintrc."""

    # pylint: disable=too-many-instance-attributes
    # pylint: disable=too-few-public-methods
    # Not unreasonable to use a class instance as a namespace.
    # pylint: disable=no-self-use
    # Perfectly fine to take function out of module namespace and encapsulate in class.

    def __init__(self):
        self.config_yamlfile_name = "mklists.yml"
        self.rule_csvfile_name = ".rules"
        self.backupdir_name = "backups"
        self.htmldir_name = "html"
        self.url_pattern_regex = (
            r"""((?:git://|http://|https://)[^ <>'"{}(),|\\^`[\]]*)"""
        )
        self.datadir_pathname = os.getcwd()
        self.timestamp_str = datetime.datetime.now().strftime("%Y-%m-%d_%H%M_%S%f")
        self.valid_filename_characters_regex = r"[\-_=.,@:A-Za-z0-9]+$"
        self.rootdir_pathname = self.return_rootdir_pathname(
            datadir_pathname=self.datadir_pathname
        )
        self.backupdir_shortname = self.return_backupdir_shortname(
            datadir_pathname=self.datadir_pathname,
            rootdir_pathname=self.rootdir_pathname,
        )
        self.backupdir_pathname = os.path.join(
            self.rootdir_pathname,
            self.backupdir_name,
            self.backupdir_shortname,
            self.timestamp_str,
        )

    def return_rootdir_pathname(self, datadir_pathname=None):
        """Return repo root pathname when executed anywhere within repo."""
        if not datadir_pathname:
            datadir_pathname = os.getcwd()
        starting_pathname = datadir_pathname
        while "mklists.yml" not in os.listdir():
            cwd_before_changing = os.getcwd()
            os.chdir(os.pardir)
            if os.getcwd() == cwd_before_changing:
                os.chdir(starting_pathname)
                return None
        rootdir_pathname = os.getcwd()
        os.chdir(starting_pathname)
        return rootdir_pathname

    def return_backupdir_shortname(self, datadir_pathname=None, rootdir_pathname=None):
        """@@@Docstring"""
        if datadir_pathname == rootdir_pathname:
            return "rootdir"
        # pylint: disable=bad-continuation
        # But this makes it more readable!
        return (
            self.datadir_pathname[len(self.rootdir_pathname) :]
            .strip("/")
            .replace("/", "_")
        )


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
