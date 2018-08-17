from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name = 'mklists',
    version = '0.1.1',
    license = 'MIT',
    description = 'Rebuild plain-text todo lists using rules',
    long_description=long_description,
    author = 'Tom Baker',
    author_email='tom@tombaker.org',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: MIT License',
        'Topic :: Text Processing',
    ],
    url = 'https://github.com/tombaker/mklists',
    packages = find_packages(exclude=['tests']),
    install_requires =[
        'pyyaml', 'Click', 'dataclasses'
    ],
    entry_points = """
        [console_scripts]
        mklists=mklists.cli:cli
    """
)
