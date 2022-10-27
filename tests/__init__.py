from changes.config import Config

module_name = 'test_app'
context = Config(
    module_name,
    True,
    True,
    True,
    f'{module_name}/requirements.txt',
    '0.0.2',
    '0.0.1',
    'https://github.com/someuser/test_app',
    None,
)

context.gh_token = 'foo'
context.requirements = f'{module_name}/requirements.txt'
context.tmp_file = f'{module_name}/__init__.py'
context.initial_init_content = [
    '"""A test app"""',
    '',
    "__version__ = '0.0.1'",
    "__url__ = 'https://github.com/someuser/test_app'",
    "__author__ = 'Some User'",
    "__email__ = 'someuser@gmail.com'",
]
