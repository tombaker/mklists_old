# """Rule = namedtuple('Rule', 'srcmatch_awkf srcmatch_rgx src trg trgsort_awkf')"""

def get_rulesfiles(*rules_files):
    """

def get_rules(*rules_files):
    """
    split line once on hash (#)
    keep half of line before hash
    strip whitespace on both sides
    delete blank lines
    rules_l = list()
    for line in rules_l:
        line_split = line.split()
        Something like for line, line_split in ..
        
        split the line 
        bail (citing line) if any line is not exactly five fields long
        try:
            $1.isdigit()  - which includes zero
            $5.isdigit()  - which includes zero
            $1 = int($1)
            $5 = int($1)
        except SourceMatchAndTargetSortOrderDigits:
            bail (citing line) with error message
        $3 = re.compile($3)
        $4 and $5:
            must have only permitted characters
                valid_chars = '@:-_=.{}{}'.format(string.ascii_letters, string.digits)
        if it gets this far:
            append line to rules_l

    return rules_l (list of five-item tuples)
    """
    pass

# RuleFile
#     print(rulefilename)
#         NoRuleFileError('Rule file does not exist or is unusable.')
# 
# RuleString
#     Fields 1 and 5 must be digits
#         try:
#             if field1.isdigit():
#                 field1 = int(field1)
#                 field5 = int(field5)
#         except ValueError as e:
#             print(rule_s)
#                 print('First rule item (field in source line matched) must be a digit.')
#                 print('Fifth rule item (sort order of target file) must be a digit.')
# 
#     Field 2, a regex
#                 print('Second rule item (regex matched to field in source line) must be a digit.')
#                 def exit_rule_regex_must_be_escaped(line):
#                     print("In rule: %r" % line)
#                     print("...in order to match the regex string: %r" % linesplitonorbar[1])
#                     print("...the rule component must be escaped as follows: %r" % re.escape(linesplitonorbar[1])
# 
#     Not five fields long
#         print(rulestring)
# 
#     No source 
#         probably because not yet created by target
# 
# Definitions
#     Digit = any of the numerals from 0 to 9, especially when forming part of a number
#     Integer = any whole number, including negative numbers

