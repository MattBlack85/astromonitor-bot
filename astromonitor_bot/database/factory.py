import os
import pathlib

TEST_ENV = os.environ.get('TESTING')
PROJECT_ROOT = pathlib.Path(__file__).parent.parent.parent.absolute()


def db_factory():
    if TEST_ENV == '1':
        return "sqlite+aiosqlite:////tmp/test.db"
        # return (PROJECT_ROOT / 'test.db').absolute()
    else:
        DB_PATH = os.environ.get('DB_PATH', f"sqlite+aiosqlite:////{(PROJECT_ROOT / 'astromonitor.db').absolute()}")
        return DB_PATH
