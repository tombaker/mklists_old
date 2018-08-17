"""Rules docstring"""

import re
import sys
from collections import defaultdict
from dataclasses import dataclass
from mklists.rule import Rule

@dataclass
class Rules:
    """Parses files in special 'rules' format to get Rule objects.

    Attributes:
        stringrules: list of lines read in from rule files, before parsing
        splitrules: list of stringrules parsed into lists of fields
        rules: list of Rule objects
    """

    stringrules: list = None
    splitrules: list = None
    rules: list = None

    def parse(self, *rulefiles):
        """Parse rule files adding resulting instance of Rule to Rules.

        Args:
            *rulefiles: Names of files with unparsed rules (list).

        Returns:
        """
        self._get_stringrules(*rulefiles)
        self._parse_stringrules_to_splitrules()
        self._instantiate_splitrules_as_ruleobjects()
        self._rule_sources_have_precedents()
        self._validate_rules()

    def _get_stringrules(self, *rulefiles):
        """Given filenames of rule files, gets lines ("stringrules").

        Args:
            *rulefiles: list of rule files

        Returns:
            self.stringrules: list of stringrules

        Raises:
            FileNotFoundError: if a rule file is not accessible.
        """
        stringrules = []
        for rulefile in rulefiles:
            try:
                with open(rulefile, 'r') as rulefile:
                    stringrules.extend(rulefile.read().splitrules())
            except FileNotFoundError:
                sys.exit(f'Rule file "{rulefile}" is not accessible.')
        self.stringrules = stringrules
        return self.stringrules

    def _parse_stringrules_to_splitrules(self):
        """Returns splitrules - stringrules parsed into fields.

        Rule file format, designed for ease of editing, requires
        special parsing procedure implemented here.

        Returns:
            self.splitrules: stringrules parsed into fields using algorithm.
        """
        splitrules = []
        for line in self.stringrules:
            line_fielded = []
            line_field1, __, line_rest = line.partition('/')
            line_fielded.append(line_field1.strip())
            regex, __, line_rest = line_rest.rpartition('/')
            line_fielded.append(regex)
            line_rest = line_rest.partition('#')[0].strip()
            line_fielded.extend(line_rest.split())
            line_fielded = [f for f in line_fielded if not re.match('#', f)]
            line_fielded = [f for f in line_fielded if f] # drops empty items
            if line_fielded:
                splitrules.append(line_fielded)
        self.splitrules = splitrules
        return self.splitrules

    def _instantiate_splitrules_as_ruleobjects(self):
        """Returns list of rule objects.

        Validates each splitrule and creates rule objects from splitrules
        (after validation).

        Raises:
        """
        rules = []
        for rule in self.splitrules:
            Rule.validate(rule)
            rules.append(Rule(*rule))
        self.rules = rules
        return self.rules

    def _rule_sources_have_precedents(self):
        """Verifies that each "source" has been previously initialized.

        Returns:
            True

        Raises:
            SourceNotPrecedentedError: if any "source" not initialized.
        """
        initialized = False
        sources = []

        for rule in self.rules:
            if not initialized:
                sources.append(rule.source)
                initialized = True
            if rule.source not in sources:
                print(f"Oh no! {rule.source} is not one of {sources}!")
                raise SourceNotPrecedentedError
            if rule.target not in sources:
                sources.append(rule.target)
        return True

    def _validate_rules(self):
        """Validates list of rule objects.

        Calls Rule class to validate each rule.

        Returns:
            self.rules: validated and lightly corrected list of rule objects.
        """
        validated_rules = []
        for rule in self.rules:
            Rule.validate(rule)
            validated_rules.append(rule)
        self.rules = validated_rules
        return self.rules

    def apply(self, datalines):
        """
        Args:
            datalines: all datalines (list)

        Initializes dictionary structure where:
        * values hold (changing) portions of 'datalines'
        * keys are filenames to which values will be written
        """

        datalines_dict = defaultdict(list)
        initialized = False

        for rule in self.rules:

            if not initialized:
                datalines_dict[rule.source] = rule.source
                initialized = True

            for line in datalines:

                # skip match if rule.source_matchfield out of range
                if rule.source_matchfield > len(line.split()):
                    continue

                # match against entire line if rule.source_matchfield is zero
                if rule.source_matchfield == 0:
                    rgx = rule.source_matchpattern
                    positives = [line for line in rule.source
                                 if re.search(rgx, line)]
                    negatives = [line for line in rule.source
                                 if not re.search(rgx, line)]
                    rule.target.extend(positives)
                    rule.source = negatives

                # match field if rule.source_matchfield > 0 and within range
                if rule.source_matchfield > 0:
                    eth = rule.source_matchfield - 1
                    rgx = rule.source_matchpattern
                    positives = [line for line in rule.source
                                 if re.search(rgx, line.split()[eth])]
                    negatives = [line for line in rule.source
                                 if not re.search(rgx, line.split()[eth])]
                    rule.target.extend(positives)
                    rule.source = negatives

                # sort target if rule.target_sortorder greater than zero
                if rule.target_sortorder:
                    decorated = [(line.split()[rule.target_sortorder - 1], __, line)
                                 for __, line in enumerate(rule.target)]
                    decorated.sort()
                    rule.target = [line for ___, __, line in decorated]

            return all

        return datalines_dict


class SourceNotPrecedentedError(SystemExit):
    """Source has not been previously initialized."""
