import os

import pytest

from astromonitor_bot.database.connection import connection
from astromonitor_bot.database.factory import db_factory


@pytest.fixture(autouse=True)
def setup_test_env_fixture(request, scope='session'):
    connection.start()

    def drop_db():
        os.remove(db_factory())

    request.addfinalizer(drop_db)
