import pytest
from mklists.util import *

def test_is_utf81():
    with pytest.raises(SystemExit):
        is_utf8('/Users/tbaker/github/tombaker/mklists/mklists/tests/_non-text.png')

