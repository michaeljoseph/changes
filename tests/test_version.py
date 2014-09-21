import mock
from click.testing import CliRunner

from changes import cli, version
from . import *



def test_increment():
    assert '1.0.0' == version.increment('0.0.1', major=True)

    assert '0.1.0' == version.increment('0.0.1', minor=True)

    assert '1.0.1' == version.increment('1.0.0', patch=True)



def test_current_version():
    assert '0.0.1' == version.current_version(module_name)


def test_get_new_version():
    with mock.patch('__builtin__.raw_input') as mock_raw_input:
        mock_raw_input.return_value = None
        assert '0.1.0' == version.get_new_version(
            module_name,
            '0.0.1',
            True,
            minor=True,
        )
