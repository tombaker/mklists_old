mklists

Current tagline - change in: README.md /setup.py /mklists/cli.py /mkdocs.yml $MKLNOTES/README.md
* Recompose plain text lists by tweaking rules

Next steps:
* Update pip distribution

Note:
* Assumes that data lines start in first column (and if not, split() will
  disregard leading whitespace)

Uses:
* [Click](http://click.pocoo.org/7/utils/) - Click testing and file system isolation
* [Pytest](https://pytest.org/)

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
