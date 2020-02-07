"""Trivial test of contents of string constants."""


from mklists.constants import (
    CONFIGFILE_NAME,
    ROOTDIR_RULEFILE_NAME,
    DATADIR_RULEFILE_NAME,
)


def test_defaults_configfile_name():
    """Trivially checks whether constants carry correct values."""
    assert CONFIGFILE_NAME == "mklists.yml"
    assert ROOTDIR_RULEFILE_NAME == "rules.cfg"
    assert DATADIR_RULEFILE_NAME == ".rules"
