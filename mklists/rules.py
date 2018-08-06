class BadRuleString(SystemExit): pass

VALID_CHARS = '@:-_=.{}{}'.format(string.ascii_letters, string.digits)

def get_stringrules(*rules_files):
    srules = []
    for rules_file in rules_files:
        try:
            with open(rules_file, 'r') as rulefile:
                srules.extend(rulefile.read().splitlines())
        except FileNotFoundError:
            sys.exit(f'Rule file "{rules_file}" does not exist or is not accessible.')

    return srules
            
def srules_to_lrules(srules):
    return [srule_to_lrule(line) for line in srules if srule_to_lrule(line)]


def check_lrules(lrules):
    lrules_checked = []
    for lrule_to_check in lrules:
        lrules_checked.append(lrule)

    return lrules_checked
