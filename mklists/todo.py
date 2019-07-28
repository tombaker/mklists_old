"""Todo"""


def move_certain_datafiles_to_other_directories(files2dirs_dict=None):
    """Args: files2dirs_dict: filename (key) and destination directory (value)
    See /Users/tbaker/github/tombaker/mklists/tests/test_todo_move_certain_datafiles_to_other_directories
    """


def write_datadict_to_htmlfiles_in_htmldir(datadict={}, verbose=False):
    """
    See /Users/tbaker/github/tombaker/mklists/tests/test_todo_write_datadict_to_htmlfiles_in_htmldir
    -- Create htmldir (if it does not already exist).
    -- Delete files in htmldir (if files already exist there).
    -- Write out contents of datadict to working directory:
       -- datadict keys are filenames.
          -- for each filename, add file extension '.html'
       -- datadict values are contents of files.
          -- filter each line through return_htmlstr_from_textstr.
    """
