import pypandoc


def md2rst(markdown):
    return pypandoc.convert(
        markdown.decode('utf-8'),
        'rst',
        format='md'
    )
