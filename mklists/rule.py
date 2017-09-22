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
    def __init__(self, text_line):
        line = text_line

class Rule(object):
    """ Rule = namedtuple('Rule', 'srcmatch_awkf srcmatch_rgx src trg trgsort_awkf')
    """

