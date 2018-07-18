import sys

def get_stringrules(*rules_files):
    stringrules = []
    for rules_file in rules_files:
        try:
            with open(rules_file, 'r') as rulefile:
                stringrules.extend(rulefile.read().splitlines())
        except FileNotFoundError:
            sys.exit(f'Rule file "{rules_file}" does not exist or is not accessible.')

    return stringrules
            
get_stringrules('_rules')
