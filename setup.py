from setuptools import setup
import changes

setup(
    name=changes.__name__,
    version=changes.__version__,
    description=changes.__doc__,
    author=changes.__author__,
    author_email=changes.__email__,
    url=changes.__url__,
    packages=[changes.__name__],
    install_requires=[
        'docopt < 1.0.0',
        'semantic_version < 1.0.0'
    ],
    test_suite='nose.collector',
    license=open('LICENSE').read(),
)
