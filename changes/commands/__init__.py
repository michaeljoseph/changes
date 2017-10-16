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
        str(message),
        **STYLES[style]
    )


def info(message):
    _echo('{}...'.format(message), 'info')


def note(message):
    _echo(message, 'note')


def highlight(message):
    return click.style(message, fg='cyan', bold=True)


def error(message):
    _echo(message, 'error')
