import yaml
rulefiles = ['.rulesy', '.rulesy2']

def parse_yaml(rulefiles):
    for rulefile in rulefiles:
        rules_raw = []
        for rulefile in rulefiles:
            try:
                with open(rulefile) as rf:
                    rules_raw.extend(yaml.load(rf))
            except FileNotFoundError:
                raise Exception(f"{repr(rulefile)} not found.")

    return rules_raw
