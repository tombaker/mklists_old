"""Show how various things are handled in pytest functions."""

import os
import pathlib
from mklists.decorators import preserve_cwd

CONTENT = "content"


@preserve_cwd
def test_mkdir_with_tmpdir(tmpdir):
    """Show how directory changes are handled in pytest functions."""
    print()
    print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
    print(f"{tmpdir} : fixture of this pytest function, is of type {type(tmpdir)}.")
    print(f"{str(tmpdir)} : str(tmpdir)")
    print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
    startdir_pathname = os.getcwd()
    print(f"{startdir_pathname} : CWD before changing to any other directories in test")
    os.chdir(tmpdir)
    middledir_pathname = os.getcwd()
    print(f"{middledir_pathname} : CWD after os.chdir(tmpdir) and os.getcwd()")
    path = pathlib.Path("p/q/r")
    path.mkdir(parents=True, exist_ok=True)
    os.chdir(path)
    afterdir_pathname = os.getcwd()
    print(f"{afterdir_pathname} : CWD after creating/changing to subdir 'p/q/r'")
    print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
    assert True


@preserve_cwd
def test_mkdir_with_tmp_path(tmp_path):
    """As per https://docs.pytest.org/en/latest/tmpdir.html,
    pytest fixture 'tmpdir' appears to be deprecated in favor of 'tmp_path'."""
    print()
    print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
    print(f"{tmp_path} : fixture of this pytest function, is of type {type(tmp_path)}.")
    print(f"{str(tmp_path)} : str(tmp_path)")
    print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
    startdir_pathname = os.getcwd()
    print(f"{startdir_pathname} : CWD before changing to any other directories in test")
    os.chdir(tmp_path)
    middledir_pathname = os.getcwd()
    print(f"{middledir_pathname} : CWD after os.chdir(tmp_path) and os.getcwd()")
    path = pathlib.Path("p/q/r")
    path.mkdir(parents=True, exist_ok=True)
    os.chdir(path)
    afterdir_pathname = os.getcwd()
    print(f"{afterdir_pathname} : CWD after creating/changing to subdir 'p/q/r'")
    print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
    assert True


@preserve_cwd
def test_mkdir_with_tmp_path_as_per_pytest_documentation(tmp_path):
    d = tmp_path / "sub"
    d.mkdir()
    p = d / "hello.txt"
    p.write_text(CONTENT)
    assert p.read_text() == CONTENT
    assert len(list(tmp_path.iterdir())) == 1
