"""Setup file for mklists project."""

from setuptools import setup, find_packages

setup(
    name = 'mklists',
    version = '0.1.0',
    license = 'MIT',
    description = 'Manage plain text lists by tweaking rules',
    author = 'Tom Baker',
    url = 'https://github.com/tombaker/mklists',
    packages = find_packages(exclude=['tests']),
    install_requires =[
        'pyyaml', 'posixpath', 'click'
    ],
    entry_points = """
        [console_scripts]
        mklists=mklists.cli:cli
    """
)
