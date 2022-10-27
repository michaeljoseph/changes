import click

STYLES = {
    'debug': {'fg': 'blue'},
    'info': {'fg': 'green', 'bold': True},
    'highlight': {'fg': 'cyan', 'bold': True},
    'note': {'fg': 'blue', 'bold': True},
    'error': {'fg': 'red', 'bold': True},
}


def echo(message, style):
    click.secho(str(message), **STYLES[style])


def debug(message):
    echo(f'{message}...', 'debug')


def info(message):
    echo(f'{message}...', 'info')


def note(message):
    echo(message, 'note')


def note_style(message):
    return click.style(message, **STYLES['note'])


def highlight(message):
    return click.style(message, **STYLES['highlight'])


def error(message):
    echo(message, 'error')
