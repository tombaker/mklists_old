"""Return list of rule objects from chain of rule files."""

import csv
import os
from pathlib import Path
from .ruleclass import Rule
from .constants import ROOTDIR_RULEFILE_NAME, DATADIR_RULEFILE_NAME, CONFIGFILE_NAME
from .decorators import preserve_cwd
from .exceptions import (
    BadRuleError,
    MissingArgumentError,
    MissingValueError,
    NoRulefileError,
    NoRulesError,
)

# pylint: disable=bad-continuation
# Black disagrees.


def get_rules(startdir=None):
    """Return list of Rule objects from one or more rule files."""
    if not startdir:
        startdir = Path.cwd()
    rulefile_chain = _return_rulefile_chain(startdir)
    listrules_lists_aggregated = []
    for rulefile in rulefile_chain:
        listrules_list = _return_listrules_from_rulefile_chain(rulefile)
        listrules_lists_aggregated.extend(listrules_list)
    return _return_ruleobj_list_from_listrules(listrules_lists_aggregated)


@preserve_cwd
def _return_rulefile_chain(
    startdir=None,
    rootdir_rulefile=ROOTDIR_RULEFILE_NAME,
    datadir_rulefile=DATADIR_RULEFILE_NAME,
    configfile=CONFIGFILE_NAME,
):
    """Return list of rule files from root to specified data directory."""
    if not startdir:
        startdir = Path.cwd()
    os.chdir(startdir)
    rulefile_chain = []
    while datadir_rulefile in os.listdir():
        rulefile_chain.insert(0, Path.cwd().joinpath(datadir_rulefile))
        os.chdir(os.pardir)
    if configfile in os.listdir():
        if rootdir_rulefile in os.listdir():
            rulefile_chain.insert(0, Path.cwd().joinpath(rootdir_rulefile))
    return rulefile_chain


def _return_listrules_from_rulefile_chain(csvfile=None):
    """Return lists of lists, string items stripped, from pipe-delimited CSV file."""
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
    if not pyobj:
        raise MissingArgumentError("Expecting list of lists of rule components.")
    ruleobj_list = []
    for item in pyobj:
        try:
            if Rule(*item).is_valid():
                ruleobj_list.append(Rule(*item).coerce_types())
        except MissingValueError:
            print(f"Skipping badly formed rule: {item}")
        except ValueError:
            print(f"Value error.")
        except TypeError:
            raise BadRuleError(f"Rule {repr(item)} is badly formed.")
    if not ruleobj_list:
        raise NoRulesError(f"No rules found.")
    return ruleobj_list
