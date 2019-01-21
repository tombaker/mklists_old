from mklists.utils import write_initial_rule_yamlfiles


def test_write_initial_rule_yamlfiles(myrepo_empty):
    write_initial_rule_yamlfiles()
    assert False
