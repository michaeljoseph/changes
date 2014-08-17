import io
import re
from setuptools import setup

init_py = io.open('changes/__init__.py').read()
metadata = dict(re.findall("__([a-z]+)__ = '([^']+)'", init_py))
metadata['doc'] = re.findall('"""(.+)"""', init_py)[0]

setup(
    name='changes',
    version=metadata['version'],
    description=metadata['doc'],
    author=metadata['author'],
    author_email=metadata['email'],
    url=metadata['url'],
    packages=['changes'],
    install_requires=io.open('requirements/runtime.txt').readlines(),
    entry_points={
        'console_scripts': [
            'changes = changes:main',
        ],
    },
    license=open('LICENSE').read(),
)
