"""Rules docstring"""

import re
import sys
from collections import defaultdict
from dataclasses import dataclass
from mklists.rule import Rule

@dataclass
class Rules:
    """Parse YAML rule files and produce lists of Rule objects."""

    rules: list = None

    def parse(self, *rulefiles):
        """docstring"""
        raw = self._parse_yaml(*rulefiles)
        self.rules = self._instantiate_rule_objects(raw)
        self._validate_rule_objects()
        return self.rules

    def _parse_yaml(self, *rulefiles):
        """docstring"""
        rules_raw = []
        for rulefile in rulefiles:
            try:
                with open(rulefile) as rf:
                    rules_raw.extend(yaml.load(rf))
            except FileNotFoundError:
                raise RuleFileNotFoundError(f'{rulefile}" not found.')
        return rules_raw

    def _instantiate_rule_objects(self, raw_rules: list = None):
        """docstring"""
        rules_validated = []
        for raw_rule in raw_rules:
            Rule.validate(raw_rule)
            rules_validated.append(Rule(*raw_rule))
        self.rules = rules_validated

    def validate(self):
        self._rule_sources_have_precedents()

    def _validate_rule_objects(self):
        validated_rules = []
        for rule in self.rules:
            Rule.validate(rule)
            validated_rules.append(rule)
        self.rules = validated_rules
        return self.rules

    def _rule_sources_have_precedents(self):
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
                    eth_sortorder = rule.target_sortorder - 1
                    decorated = [(line.split()[eth_sortorder], __, line)
                                 for __, line in enumerate(rule.target)]
                    decorated.sort()
                    rule.target = [line for ___, __, line in decorated]

            return all

        return datalines_dict

class RulesErrors(SystemExit):
    """Category of exceptions related to sets or rules."""

class RuleFileNotFoundError(RulesErrors):
    """Rule file not found or not accessible."""

class SourceNotPrecedentedError(RulesErrors):
    """Source has not been previously initialized."""
