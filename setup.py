"""Setup file for mklists project."""

from setuptools import setup, find_packages

setup(
    name='mklists',
    version='0.1.0',
    license='MIT',
    description='Rearrange plain text lists by tweaking rules',
    author='Tom Baker',
    url=' https://github.com/tombaker/mklists ',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'pyyaml', 
    ],
)
