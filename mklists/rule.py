class RuleFile(object):
    """ print(rulefilename)
        NoRuleFileError('Rule file does not exist or is unusable.')
    """

class RuleString(object):
    """ Fields 1 and 5 must be digits
            try:
                if field1.isdigit():
                    field1 = int(field1)
                    field5 = int(field5)
            except ValueError as e:
                print(rule_s)
                    print('First rule item (field in source line matched) must be a digit.')
                    print('Fifth rule item (sort order of target file) must be a digit.')
    
        Field 2, a regex
                    print('Second rule item (regex matched to field in source line) must be a digit.')
                    def exit_rule_regex_must_be_escaped(line):
                        print("In rule: %r" % line)
                        print("...in order to match the regex string: %r" % linesplitonorbar[1])
                        print("...the rule component must be escaped as follows: %r" % re.escape(linesplitonorbar[1])
    
        Not five fields long
            print(rulestring)
    
        No source 
            probably because not yet created by target
        Note
            Digit = any of the numerals from 0 to 9, especially when forming part of a number
            Integer = any whole number, including negative numbers
    """

class Rule(object):
    """ Rule = namedtuple('Rule', 'srcmatch_awkf srcmatch_rgx src trg trgsort_awkf')
    """

FTMP /Users/tbaker/github/rdflib/rdflib/rdflib/collection.py
FTMP /Users/tbaker/github/rdflib/rdflib/rdflib/compare.py
FTMP /Users/tbaker/github/rdflib/rdflib/rdflib/compat.py
FTMP /Users/tbaker/github/rdflib/rdflib/rdflib/events.py
FTMP /Users/tbaker/github/rdflib/rdflib/rdflib/exceptions.py
FTMP /Users/tbaker/github/rdflib/rdflib/rdflib/graph.py
FTMP /Users/tbaker/github/rdflib/rdflib/rdflib/namespace.py
FTMP /Users/tbaker/github/rdflib/rdflib/rdflib/parser.py
FTMP /Users/tbaker/github/rdflib/rdflib/rdflib/paths.py
FTMP /Users/tbaker/github/rdflib/rdflib/rdflib/plugin.py
FTMP /Users/tbaker/github/rdflib/rdflib/rdflib/query.py
FTMP /Users/tbaker/github/rdflib/rdflib/rdflib/resource.py
FTMP /Users/tbaker/github/rdflib/rdflib/rdflib/serializer.py
FTMP /Users/tbaker/github/rdflib/rdflib/rdflib/store.py
FTMP /Users/tbaker/github/rdflib/rdflib/rdflib/term.py
FTMP /Users/tbaker/github/rdflib/rdflib/rdflib/util.py
FTMP /Users/tbaker/github/rdflib/rdflib/rdflib/void.py
class RuleLine(object):
    def __init__(self, text_line):
        line = text_line

    def strip_comments(line):
        return line.partition('#')[0]

