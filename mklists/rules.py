"""Return list of rule objects from chain of rule files."""

import csv
import os
from pathlib import Path
from .ruleclass import Rule
from .constants import ROOTDIR_RULEFILE_NAME, DATADIR_RULEFILE_NAME, CONFIGFILE_NAME
from .decorators import preserve_cwd
from .exceptions import BadRuleError, MissingValueError, NoRulefileError, NoRulesError

# pylint: disable=bad-continuation
# Black disagrees.


def return_ruleobj_list_from_rulefiles(startdir=None):
    """Return list of Rule objects from one or more rule files."""
    # /Users/tbaker/github/tombaker/mklists/tests/rules/test_return_ruleobj_list_from_rulefiles.py
    if not startdir:
        startdir = Path.cwd()
    rulefile_chain = _return_rulefile_chain(startdir)
    listrules_lists_aggregated = []
    for rulefile in rulefile_chain:
        listrules_list = _return_listrules_from_rulefile_list(rulefile)
        listrules_lists_aggregated.extend(listrules_list)
    return _return_ruleobj_list_from_listrules(listrules_lists_aggregated)


def _return_listrules_from_rulefile_list(csvfile=None):
    """Return lists of lists, string items stripped, from pipe-delimited CSV file."""
    # /Users/tbaker/github/tombaker/mklists/tests/rules/test__return_listrules_from_rulefile_list.py
    csv.register_dialect("rules", delimiter="|", quoting=csv.QUOTE_NONE)
    try:
        # encoding 'utf-8-sig' for Excel files with U+FEFF
        # newline '' for MS-Windows '\r\n' line endings
        csvfile_obj = open(csvfile, newline="", encoding="utf-8-sig")
    except FileNotFoundError:
        raise NoRulefileError(f"Rule file not found.")
    except TypeError:
        raise NoRulefileError(f"No rule file specified.")
    rules_parsed_list_raw = list(csv.reader(csvfile_obj, dialect="rules"))
    rules_parsed_list = []
    for single_rule_list in rules_parsed_list_raw:
        single_rule_list_depadded = []
        if len(single_rule_list) > 4:
            for item in single_rule_list:
                single_rule_list_depadded.append(item.strip())
        if single_rule_list_depadded:
            if single_rule_list_depadded[0].isdigit():
                rules_parsed_list.append(single_rule_list_depadded[0:5])
    return rules_parsed_list


def _return_ruleobj_list_from_listrules(pyobj=None):
    """Return list of Rule objects from list of lists of component strings."""
    # /Users/tbaker/github/tombaker/mklists/tests/rules/test__return_ruleobj_list_from_listrules.py
    if not pyobj:
        raise NoRulesError(f"List with rule components as strings must be specified.")
    ruleobj_list = []
    for item in pyobj:
        try:
            if Rule(*item).is_valid():
                ruleobj_list.append(Rule(*item))
        except MissingValueError:
            print(f"Skipping badly formed rule: {item}")
        except ValueError:
            print(f"Value error.")
        except TypeError:
            raise BadRuleError(f"Rule {repr(item)} is badly formed.")
    if not ruleobj_list:
        raise NoRulesError(f"No rules found.")
    return ruleobj_list


@preserve_cwd
def _return_rulefile_chain(
    startdir=None,
    datadir_rulefile=DATADIR_RULEFILE_NAME,
    rootdir_rulefile=ROOTDIR_RULEFILE_NAME,
    configfile=CONFIGFILE_NAME,
):
    """Return list of rule files from root to specified data directory."""
    # /Users/tbaker/github/tombaker/mklists/tests/rules/test__return_rulefile_chain.py
    if not startdir:
        startdir = Path.cwd()
    os.chdir(startdir)
    root2datadir_rulefiles = []
    while datadir_rulefile in os.listdir():
        root2datadir_rulefiles.insert(0, Path.cwd().joinpath(datadir_rulefile))
        os.chdir(os.pardir)
    if configfile in os.listdir():
        if root2datadir_rulefiles:
            if rootdir_rulefile in os.listdir():
                root2datadir_rulefiles.insert(0, Path.cwd().joinpath(rootdir_rulefile))
    return root2datadir_rulefiles
