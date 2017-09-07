from collections import defaultdict
import glob

def get_globlines_list(cwd='.'):
    """Something like:
    all_lines = []
    for file in glob.glob('*'):
        all_lines.append(file.readlines())
    """
    pass

def shuffle(rules_list, globlines_list):
    """
    Rule = namedtuple('Rule', 'matchfield_int matchfield_regex sourcename_key targetname_key targetsort_int')
    """

    mklists_dict = defaultdict(list)

    for index, rule in enumerate(rules_list):
        if index == 0:
            mklists_dict[sourcename_key] = globlines_list
        for globline_string in globlines_list:
            if len(globline_string.split()) <= targetsort_int:
                mklists_dict[sourcename_key] = [ line for line in globlines_list if not re.search(
        return mklists_dict

        """
        for rule in rules:
            mklists_dict[source] = [line for line in lines if not re.search(searchkey, line)] # over-writes
            mklists_dict[target].append([line for line in lines if re.search(searchkey, line)]) # appends
            if sort_order > 0:
                mklists_dict[target] according to targetsort_int
        """
        
