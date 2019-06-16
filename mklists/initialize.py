"""Write initial configuration and rule files."""

import io
import os

# @@TODO: distinguish between YAML string constants and
# initial configuration values, which can directly be expressed
# as a Python object

CONFIG_YAMLFILE_NAME = "mklists.yml"
RULE_YAMLFILE_NAME = ".rules"
INITIAL_CONFIG_YAMLFILE_STR = r"""\
backups: 3
html: false
invalid_filename_patterns: [\.swp$, \.tmp$, ~$, ^\.]
verbose: false
files2dirs: {
    move_to_logs.txt: logs,
    move_to_a.txt: a,
}
"""
INITIAL_GLOBALRULE_YAMLFILE_STR = """\
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


def write_initial_config_yamlfile():
    """Write initial YAML config file (/mklists.yml)."""
    config_path = os.path.join(os.getcwd())
    config_file = os.path.join(config_path, CONFIG_YAMLFILE_NAME)
    io.open(config_file, "w", encoding="utf-8").write(INITIAL_CONFIG_YAMLFILE_STR)


def write_initial_rule_yamlfiles():
    """Write initial YAML rule files:
    * global rule file (/.rules)
    * folder rule file (/a/.rules)"""
    config_path = os.path.join(os.getcwd())
    grule_file = os.path.join(config_path, RULE_YAMLFILE_NAME)
    os.makedirs(os.path.join(config_path, "a"))
    os.makedirs(os.path.join(config_path, "b"))
    rulea_file = os.path.join(config_path, "a", RULE_YAMLFILE_NAME)
    ruleb_file = os.path.join(config_path, "b", RULE_YAMLFILE_NAME)
    io.open(grule_file, "w", encoding="utf-8").write(INITIAL_GLOBALRULE_YAMLFILE_STR)
    io.open(rulea_file, "w", encoding="utf-8").write(INITIAL_EXAMPLE_RULEA_YAMLFILE_STR)
    io.open(ruleb_file, "w", encoding="utf-8").write(INITIAL_EXAMPLE_RULEB_YAMLFILE_STR)
