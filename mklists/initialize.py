"""Write initial configuration and rule files.

$ mklists init --example (or --newbie)
    These would be installed as examples:
    * /mklists.yml
    * /.rules
    * /a/.rules
    * /a/calendar.txt
    * /a/todo.txt
    * /logs/.rules
    * /logs/log.txt
"""

import io
import os
import yaml

# from .utils import make_backup_shortname

# @@TODO: distinguish between YAML string constants and
# initial configuration values, which can directly be expressed
# as a Python object?
# 2019-06-16: No, write initial config file with sensible defaults
# and trust people to edit that file carefully.  If it is then
# edited with bad values (wrong type, out of range, missing)
# the functions that rely on those values should trigger an exit
# with error message.

CONFIG_YAMLFILE_NAME = "mklists.yml"
RULE_YAMLFILE_NAME = ".rules"
INITIAL_CONFIG_YAMLFILE_STR = """\
backups: 3
html: false
invalid_filename_patterns: [\.swp$, \.tmp$, ~$, ^\.]
verbose: false
files2dirs: {
    move_to_logs.txt: logs,
    move_to_a.txt: a,
}
"""
INITIAL_EXAMPLE_GLOBALRULE_YAMLFILE_STR = """\
# This file: Global rules, applied before rules specific to a list folder.
# Put here any rules that apply to multiple list folders.
- [0, '.',          x,         lines,            0]
- [0, '^=',         lines,     move_to_a.txt,    1]
- [0, '^2019|2020', lines,     move_to_logs.txt, 1]
"""
INITIAL_MINIMAL_RULEA_YAMLFILE_STR = """\
- [0, '.',       lines,      consolidated_lines,   0]
"""
INITIAL_EXAMPLE_RULEA_YAMLFILE_STR = """\
# This file: Rules specific to this list folder.
# At runtime, these rules are appended to the global rules.
- [0, '.',       lines,      todo.txt,   0]
- [0, '.',       to_a.txt    todo.txt,   1]
- [1, 'NOW',     todo.txt,   now.txt,    1]
- [1, 'LATER',   todo.txt,   later.txt,  0]
"""
INITIAL_EXAMPLE_RULEB_YAMLFILE_STR = """\
# This file: Rules specific to this list folder.
# At runtime, these rules are appended to the global rules.
- [0, '.',       lines,      b.txt,      0]
- [1, '^2019',   b.txt,      2019.txt,   1]
- [1, '^2020',   b.txt,      2020.txt,   0]
"""


def load_config_yamlfile(mklists_yamlfile=CONFIG_YAMLFILE_NAME):
    """See /Users/tbaker/github/tombaker/mklists/tests/test_init_load_config_yamlfile
    get_pyobj_from_yamlfile(mklists_yamlfile)
    """
    yaml.load(open(mklists_yamlfile).read())


def write_example_datafiles():
    """Write example data."""


def write_example_rule_yamlfiles():
    """Write initial YAML rule files:
    * global rule file (/.rules)
    * folder rule file (/a/.rules)"""
    config_path = os.path.join(os.getcwd())
    grule_file = os.path.join(config_path, RULE_YAMLFILE_NAME)
    os.makedirs(os.path.join(config_path, "a"))
    os.makedirs(os.path.join(config_path, "b"))
    rulea_file = os.path.join(config_path, "a", RULE_YAMLFILE_NAME)
    ruleb_file = os.path.join(config_path, "b", RULE_YAMLFILE_NAME)
    io.open(grule_file, "w", encoding="utf-8").write(
        INITIAL_EXAMPLE_GLOBALRULE_YAMLFILE_STR
    )
    io.open(rulea_file, "w", encoding="utf-8").write(INITIAL_EXAMPLE_RULEA_YAMLFILE_STR)
    io.open(ruleb_file, "w", encoding="utf-8").write(INITIAL_EXAMPLE_RULEB_YAMLFILE_STR)


def write_initial_config_yamlfile(
    file_written_name=CONFIG_YAMLFILE_NAME,
    file_written_string=INITIAL_CONFIG_YAMLFILE_STR,
):
    """See /Users/tbaker/github/tombaker/mklists/tests/test_init_write_initial_config_yamlfile
    Write initial YAML config file ('/mklists.yml')."""
    io.open(file_written_name, "w", encoding="utf-8").write(file_written_string)


def write_initial_rule_yamlfiles():
    """
    See /Users/tbaker/github/tombaker/mklists/tests/test_todo_write_initial_rule_yamlfiles
    """
    pass
