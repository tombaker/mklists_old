from setuptools import setup, find_packages

def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name = 'mklists',
    version = '0.1.1',
    license = 'MIT',
    description = 'Manage plain text lists by tweaking rules',
    long_description=readme(),
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
        'pyyaml', 'click'
    ],
    entry_points = """
        [console_scripts]
        mklists=mklists.cli:cli
    """
)
