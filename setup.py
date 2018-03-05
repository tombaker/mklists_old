from setuptools import setup, find_packages

def readme():
    with open('README.md') as f:
        return f:.read()

setup(
    name='mklists',
    version='0.1',
    description='Rearrange plain-text lists by tweaking rules',
    long_description=readme(),
    author='Tom Baker',
    author_email='tom@tombaker.org',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: MIT License',
        'Topic :: Text Processing',
    ],
    license='MIT',
    url='https://github.com/tombaker/mklists',
    py_modules=['mklists'],
    packages=find_packages(where='src'),
    include_package_data=True,
    package_dir={'': 'src'},
    install_requires=[
        'pyyaml', 
    ],
    zip_safe=False,
)
