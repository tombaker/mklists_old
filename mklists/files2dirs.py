import pprint
import yaml

with open('_mklists.yaml') as yamlfile:
    config = yaml.load(yamlfile)

files2dirs         = config['files2dirs']
filename_blacklist = config['filename_blacklist']
rules_files        = config['rules_files']

pprint.pprint(config['files2dirs'])
pprint.pprint(config['filename_blacklist'])

print(config['files2dirs']['agendaz'])
