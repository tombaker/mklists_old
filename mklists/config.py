"""@@@Docstring"""

from dataclasses import dataclass, field
from textwrap import dedent
import datetime
from attr import attrs, attrib

# Note: variables set only at command line:
#     cli:  [config]
#     init: [config] with_examples [directory - add this]
#     run:  [config] dryrun here_only


@attrs()
class Constants:
    """Holds variables 'hard-coded' into mklists -
    variables not intended to be changed.

    Could add validation methods here, then re-allow
    R0903 in pylintrc."""

    config_yamlfile_name = attrib(default="mklists.yml")
    rule_yamlfile_name = attrib(default=".rules")
    backupdir_name = attrib(default=".backups")
    htmldir_name = attrib(default=".html")
    url_pattern_regex = attrib(
        default=r"""((?:git://|http://|https://)[^ <>'"{}(),|\\^`[\]]*)"""
    )
    timestamp_str = datetime.datetime.now().strftime("%Y-%m-%d_%H%M_%S%f")


@dataclass(frozen=True)
class Config:
    """Holds state and self-validation methods for configuration.
    these are written to mklists.yml."""

    invalid_filename_regexes: list = field(
        default_factory=lambda: [r"\.swp$", r"\.tmp$", r"~$", r"^\."]
    )
    valid_filename_characters_regex: str = r"[\-_=.,@:A-Za-z0-9]+$"

    # Flags
    verbose: bool = True
    htmlify: bool = True

    # Other
    backup_depth_int: int = 3
    files2dirs_dict: dict = field(default_factory=lambda: {})


@dataclass
class ConfigExamples:
    """Holds state and self-validation methods for examples."""

    datadira_name: str = "a"
    datadirb_name: str = "b"

    rootdir_rules_yamlfile_str: str = dedent(
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

    minimal_datadira_rules_yamlfile_str: str = dedent(
        r"""# Rules for Folder A.
        - [0, '.',          alines,    etc.txt,  0]
        - [1, 'TODO',       etc.txt,   todo.txt, 1]
        """
    )

    example_datadira_rules_yamlfile_str: str = dedent(
        r"""
        - [0, '.',       alines,     todo.txt,   1]
        - [1, 'NOW',     todo.txt,   now.txt,    1]
        - [1, 'LATER',   todo.txt,   later.txt,  0]
        """
    )

    example_datadirb_rules_yamlfile_str: str = dedent(
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


fixed = Constants()
settable = Config()
example = ConfigExamples()
