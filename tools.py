def dsusort(data_lines, sort_field_number):
    """
    Given: 
    * 'data_lines': a list of data lines
    * 'sort_field_number': number of field by which 'data_lines' is to be sorted

    Returns: 
    * 'data_lines' sorted by 'sort_field_number'
    """
    data_lines_decorated = []
    for line in data_lines:
        if int(sort_field_number) <= len(line.split()):
            sort_field_contents = line.split()[int(sort_field_number) - 1]
        else:
            sort_field_contents = ''
        data_lines_decorated.append((sort_field_contents, line))
    data_lines_decorated.sort()
    return [ t[1] for t in data_lines_decorated ]

