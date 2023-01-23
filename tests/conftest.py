import os
import unittest.mock as mock
from pathlib import Path

import alembic
import pytest
import sqlalchemy
from falcon import testing

from astromonitor_bot.server import app


@pytest.fixture(scope="session", autouse=True)
def apply_migrations():
    here = Path(".")
    ini_path = here / "alembic.ini"
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


@pytest.fixture(autouse=True)
def client():
    # Assume the hypothetical `myapp` package has a function called
    # `create()` to initialize and return a `falcon.App` instance.
    return testing.TestClient(app)


@pytest.fixture
def user_999_token():
    return "98b16f31-16a6-40d3-8983-81ea9e3f07c6"


@pytest.fixture
async def user_999(request, event_loop, alembic_engine, user_999_token):
    from astromonitor_bot.database import session
    from astromonitor_bot.database.models import User
    from astromonitor_bot.tokens import delete_user

    def drop_user():
        async def drop():
            async with session():
                await delete_user(999)

        event_loop.run_until_complete(drop())

    async with session() as s:
        user = User(api_token=user_999_token, id=999)
        s.add(user)
        await s.commit()

    request.addfinalizer(drop_user)
    return user


@pytest.fixture(autouse=True)
def mock_telegram_send_message():
    """
    Mock automatically bot.send_message so that we won't try
    sending notification for real.
    """
    response = mock.AsyncMock()

    with mock.patch("astromonitor_bot.server.bot") as tbot:
        tbot.send_message.side_effect = response
        yield tbot
