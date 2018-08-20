def _rule_objects_are_valid(list_of_rule_objects):
    source_list_initialized = False
    source_list = []

    for rule in list_of_rule_objects:
        if not source_list_initialized:
            source_list.append(rule.source)
            source_list.append(rule.target)
            source_list_initialized = True
        if rule.source not in source_list:
            raise SourceNotPrecedentedError("source has no precedent")
        else:
            source_list.append(rule.target)

        if rule.is_valid():
            pass

        return True

