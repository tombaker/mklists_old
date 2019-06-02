mklists

Current tagline 
* Sync todo lists to your evolving rules

Alternative taglines
* Organize your todo lists by tweaking rules

Next steps:
* http://click.pocoo.org/6/utils/ - Click testing and file system isolation
* Update pip distribution
* mklists equivalent of git-grep?
* /.globalrules exists only if /mklistsrc exists
* subcommand: mklists grepx - as in: mklists grepx NOW 2018 dc... (gather args into list)

Maybe someday:
* Event logging?
* '--verify': Compare hash of data, before and after (really necessary?)
  * Function expects to be called twice, using 'yield' in non-iterative way?
* Add stringrule as Rule attribute so that error message can show what to edit
  * Maybe even with filename and line number? (really necessary?)

Note:
* Assumes that data lines start in first column (and if not, split() will
  disregard leading whitespace)

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
