import os

import pytest
from click.testing import CliRunner
from plumbum.cmd import git

pytest_plugins = 'pytester'

# TODO: textwrap.dedent.heredoc
INIT_CONTENT = [
    '"""A test app"""',
    '',
    "__version__ = '0.0.1'",
    "__url__ = 'https://github.com/someuser/test_app'",
    "__author__ = 'Some User'",
    "__email__ = 'someuser@gmail.com'"
]
SETUP_PY = [
    'from setuptools import setup',
    "setup(name='test_app'",
]
README_MARKDOWN = [
    '# Test App',
    '',
    'This is the test application.'
]

PYTHON_MODULE = 'test_app'

FILE_CONTENT = {
    '%s/__init__.py' % PYTHON_MODULE: INIT_CONTENT,
    'setup.py': SETUP_PY,
    'requirements.txt': ['pytest'],
    'README.md': README_MARKDOWN,
    'CHANGELOG.md': [''],
}


def git_init(files_to_add):
    git('init')
    git('remote', 'add', 'origin', 'https://github.com/michaeljoseph/test_app.git')
    for file_to_add in files_to_add:
        git('add', file_to_add)
    git('commit', '-m', 'Initial commit')


def github_merge_commit():
    github = 'Merge pull request #111 from test_app/test-branch'
    git('checkout', '-b', 'test-branch')
    git('commit', '--allow-empty', '-m', 'Test branch commit message')
    git('checkout', 'master')
    git('merge', '--no-ff', 'test-branch')
    git('commit', '--allow-empty', '--amend', '-m', github)


@pytest.fixture
def git_repo():
    with CliRunner().isolated_filesystem():
        readme_path = 'README.md'
        open(readme_path, 'w').write(
            '\n'.join(README_MARKDOWN)
        )
        git_init([readme_path])

        yield


@pytest.fixture
def git_repo_with_merge_commit(git_repo):
    github_merge_commit()


@pytest.fixture
def python_module():
    with CliRunner().isolated_filesystem():
        os.mkdir(PYTHON_MODULE)

        for file_path, content in FILE_CONTENT.items():
            open(file_path, 'w').write(
                '\n'.join(content)
            )

        git_init(FILE_CONTENT.keys())

        yield
