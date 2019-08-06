#!/bin/bash

# This command creates (or refreshes) the website at https://tombaker.github.io/mklists/
# The command must be run from the root directory of the https://github.com/tombaker/mklists/ repo
# MkDocs must be installed - see http://www.mkdocs.org/#installation
# Behind the scenes, MkDocs builds the docs and uses the ghp-import tool to commit them
# to the gh-pages branch and push the gh-pages branch to GitHub.

mkdocs gh-deploy
