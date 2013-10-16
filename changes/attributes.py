import ast
import logging
import tempfile

from path import path

from changes import shell

log = logging.getLogger(__name__)


def extract_attribute(app_name, attribute_name):
    """Extract metatdata property from a module"""
    with open('%s/__init__.py' % app_name) as input_file:
        for line in input_file:
            if line.startswith(attribute_name):
                return ast.literal_eval(line.split('=')[1].strip())


def replace_attribute(app_name, attribute_name, new_value, dry_run=True):
    init_file = '%s/__init__.py' % app_name
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
        log.debug(shell.execute(
            'diff %s %s' % (tmp_file, init_file),
            dry_run=False
        ))


def has_attribute(app_name, attribute_name):
    init_file = '%s/__init__.py' % app_name
    return any(
        [attribute_name in init_line for
         init_line in open(init_file).readlines()]
    )
