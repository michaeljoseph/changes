import re
from setuptools import setup

import changes

init_py = open('changes/__init__.py').read()
metadata = dict(re.findall("__([a-z]+)__ = '([^']+)'", init_py))
metadata['doc'] = re.findall('"""(.+)"""', init_py)[0]

setup(
    name='changes',
    version=metadata['version'],
    description=metadata['doc'],
    long_description=changes.md2rst('README.md'),
    author=metadata['author'],
    author_email=metadata['email'],
    url=metadata['url'],
    packages=['changes'],
    install_requires=[
        'docopt < 1.0.0',
        'iterpipes < 1.0.0',
        'pypandoc < 1.0.0',
        'path.py < 5.0.0',
        'semantic_version < 3.0.0',
        'virtualenv < 2.0.0',
    ],
    entry_points={
        'console_scripts': [
            'changes = changes:main',
        ],
    },
    test_suite='nose.collector',
    license=open('LICENSE').read(),
)
