import os
import pathlib

TEST_ENV = os.environ.get('TEST')
PROJECT_ROOT = pathlib.Path(__file__).parent.parent.parent.absolute()


def db_factory():
    if  TEST_ENV == 'true':
        return (PROJECT_ROOT / 'test.db').absolute()
    else:
        return (PROJECT_ROOT / 'astromonitor.db').absolute()
