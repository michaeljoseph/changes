import os
import io
import shutil

from changes.config import Changes


module_name = 'test_app'
context = Changes(module_name, True, True, True, '%s/requirements.txt' % module_name, '0.0.2', '0.0.1', 'https://github.com/someuser/test_app', None)
context.requirements = '%s/requirements.txt' % module_name
context.tmp_file = '%s/__init__.py' % module_name
context.initial_init_content = [
    '"""A test app"""',
    '',
    "__version__ = '0.0.1'",
    "__url__ = 'https://github.com/someuser/test_app'",
    "__author__ = 'Some User'",
    "__email__ = 'someuser@gmail.com'"
]

def setup():
    if not os.path.exists(context.module_name):
        os.mkdir(context.module_name)

    with open(context.tmp_file, 'w') as init_file:
        init_file.write('\n'.join(context.initial_init_content))

    with open(context.requirements, 'w') as req_file:
        req_file.write('pytest')


def teardown():
    if os.path.exists(context.tmp_file):
        shutil.rmtree(module_name)
