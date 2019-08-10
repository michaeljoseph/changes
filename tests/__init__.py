from changes.config import Config

module_name = 'test_app'
context = Config(
    module_name,
    True,
    True,
    True,
    '%s/requirements.txt' % module_name,
    '0.0.2',
    '0.0.1',
    'https://github.com/someuser/test_app',
    None,
)
context.gh_token = 'foo'
context.requirements = '%s/requirements.txt' % module_name
context.tmp_file = '%s/__init__.py' % module_name
context.initial_init_content = [
    '"""A test app"""',
    '',
    "__version__ = '0.0.1'",
    "__url__ = 'https://github.com/someuser/test_app'",
    "__author__ = 'Some User'",
    "__email__ = 'someuser@gmail.com'",
]
