import os
import shutil

from changes.cli import Changes


module_name = 'test_app'
tmp_file = '%s/__init__.py' % module_name
initial_init_content = [
    '"""A test app"""',
    '',
    "__version__ = '0.0.1'",
    "__url__ = 'https://github.com/someuser/test_app'",
    "__author__ = 'Some User'",
    "__email__ = 'someuser@gmail.com'"
]
context = Changes(module_name, True, True, True, 'requirements.txt', '0.0.2', '0.0.1', 'https://github.com/someuser/test_app', None)


def setup():
    if not os.path.exists(module_name):
        os.mkdir(module_name)

    with open(tmp_file, 'w') as init_file:
        init_file.write('\n'.join(initial_init_content))

    with open('%s/requirements.txt' % module_name, 'w') as req_file:
        req_file.write('unittest2')


def teardown():
    if os.path.exists(tmp_file):
        shutil.rmtree(module_name)
