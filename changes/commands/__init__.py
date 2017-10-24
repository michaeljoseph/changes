import click

STYLES = {
    'debug': {
        'fg': 'blue',
    },
    'info': {
        'fg': 'green',
        'bold': True,
    },
    'highlight': {
        'fg': 'cyan',
        'bold': True,
    },
    'note': {
        'fg': 'blue',
        'bold': True,
    },
    'error': {
        'fg': 'red',
        'bold': True,
    }
}


def _echo(message, style):
    click.secho(
        str(message),
        **STYLES[style]
    )
def debug(message):
    _echo('{}...'.format(message), 'debug')


def info(message):
    _echo('{}...'.format(message), 'info')


def note(message):
    _echo(message, 'note')


def note_style(message):
    return click.Style(message, **STYLES['note'])


def highlight(message):
    return click.style(message, **STYLES['highlight'])


def error(message):
    _echo(message, 'error')
