import os
from pathlib import Path

import alembic
import pytest
import sqlalchemy


@pytest.fixture(scope="session", autouse=True)
def apply_migrations():
    here = Path(".")
    ini_path = here / "astromonitor_bot/database/alembic.ini"
    config = alembic.config.Config(ini_path.absolute())
    alembic.command.upgrade(config, "head")
    yield
    alembic.command.downgrade(config, "base")
    try:
        os.remove("/tmp/test.db")
    except FileNotFoundError:
        pass


@pytest.fixture
def alembic_engine():
    return sqlalchemy.create_engine("sqlite+aiosqlite:////tmp/test.db")
