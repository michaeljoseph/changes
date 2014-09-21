import ast
import logging
import tempfile

from plumbum.cmd import diff
from path import path


log = logging.getLogger(__name__)


def extract_attribute(module_name, attribute_name):
    """Extract metatdata property from a module"""
    with open('%s/__init__.py' % module_name) as input_file:
        for line in input_file:
            if line.startswith(attribute_name):
                return ast.literal_eval(line.split('=')[1].strip())


def replace_attribute(module_name, attribute_name, new_value, dry_run=True):
    """Update a metadata attribute"""
    init_file = '%s/__init__.py' % module_name
    _, tmp_file = tempfile.mkstemp()

    with open(init_file) as input_file:
        with open(tmp_file, 'w') as output_file:
            for line in input_file:
                if line.startswith(attribute_name):
                    line = "%s = '%s'\n" % (attribute_name, new_value)

                output_file.write(line)

    if not dry_run:
        path(tmp_file).move(init_file)
    else:
        log.info(diff(tmp_file, init_file, retcode=None))


def has_attribute(module_name, attribute_name):
    """Is this attribute present?"""
    init_file = '%s/__init__.py' % module_name
    return any(
        [attribute_name in init_line for
         init_line in open(init_file).readlines()]
    )
