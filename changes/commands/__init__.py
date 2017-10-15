import click

STYLES = {
    'info': {
        'fg': 'green',
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
        '{}...'.format(message),
        **STYLES[style]
    )


def info(message):
    _echo(message, 'info')


def note(message):
    _echo(message, 'note')


def error(message):
    _echo(message, 'error')
