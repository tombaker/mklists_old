import os
import yaml
from mklists import (
    GLOBAL_RULEFILE_NAME,
    GLOBAL_RULEFILE_STARTER_YAMLSTR,
    LOCAL_RULEFILE_NAME,
    LOCAL_RULEFILE_STARTER_YAMLSTR,
    BadYamlRuleError,
    InitError,
)
from mklists.rules import Rule


def get_rules(local_rulefile_name=None, global_rulefile_name=None):
    aggregated_rules_list = []
    for rulefile_name in global_rulefile_name, local_rulefile_name:
        if rulefile_name:
            rules_list = read_yamlfile_return_pyobject(rulefile_name)
            aggregated_rules_list = aggregated_rules_list + rules_list
    ruleobj_list = []
    for item in aggregated_rules_list:
        try:
            Rule(*item).is_valid
        except TypeError:
            raise BadYamlRuleError(f"Rule {repr(item)} is badly formed.")
        ruleobj_list.append(Rule(*item))

    return ruleobj_list


def get_rules2(lrules=LOCAL_RULEFILE_NAME, grules=GLOBAL_RULEFILE_NAME):
    rules_list = []
    try:
        rules_to_add = read_yamlfile_return_pyobject(grules)
        rules_list.append(rules_to_add)
    except FileNotFoundError:
        print("File was not found")
    except TypeError:
        print("NoneType")
    return rules_list

    # for rulefile_name in grules, lrules:
    #     if rulefile_name:
    #         rules_list = rules_list + rules_list
    # ruleobj_list = []
    # for item in rules_list:
    #     try:
    #         Rule(*item).is_valid
    #     except TypeError:
    #         raise BadYamlRuleError(f"Rule {repr(item)} is badly formed.")
    #     ruleobj_list.append(Rule(*item))

    # return ruleobj_list


def write_initial_configfile(settings_dict=None, verbose=False):
    """Writes initial configuration file to disk (or just says it will).
    * If configfile already exists, exits suggesting to first delete.
    * If configfile not found, creates new file using current settings.
    """
    if os.path.exists(configfile_name):
        raise InitError(
            f"To re-initialize, first delete {repr(configfile_name)}."
        )
    else:
        print(
            f"Creating default {repr(configfile_name)}. "
            f"Customize as needed."
        )
        with open(configfile_name, "w") as fout:
            fout.write(yaml.safe_dump(settings_dict, default_flow_style=False))


def write_initial_rulefiles(
    global_rulefile_name=GLOBAL_RULEFILE_NAME,
    local_rulefile_name=LOCAL_RULEFILE_NAME,
    globalrules_content=GLOBAL_RULEFILE_STARTER_YAMLSTR,
    localrules_content=LOCAL_RULEFILE_STARTER_YAMLSTR,
    verbose=False,
):
    """Generate default rule (and global rule) configuration files.

        Checks whether current settings name non-default rule files.
        If either rule file already exists, leaves untouched.
        Creates rule files with default contents.
    """
    for file, content in [
        (global_rulefile_name, globalrules_content),
        (local_rulefile_name, localrules_content),
    ]:
        if file:
            if os.path.exists(file):
                print(f"Found existing {repr(file)} - leaving untouched.")
            else:
                print(
                    f"Creating starter rule file {repr(file)} "
                    "from built-in settings - can be customized."
                )
                with open(file, "w") as fout:
                    fout.write(content)
