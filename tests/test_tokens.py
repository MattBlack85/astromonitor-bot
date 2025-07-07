import pytest
from sqlalchemy import select

from astromonitor_bot.database import session
from astromonitor_bot.database.models import User
from astromonitor_bot.tokens import delete_user
from tests.factories import ApiTokenFactory


async def test_delete_all_tokens(alembic_engine):
    async with session() as s:
        query = select(User)
        users = await s.execute(query)

    assert len(users.all()) == 0

    user_1_id = 192387
    user_2_id = 691263

    async with session() as s:
        obj = ApiTokenFactory(user_id=user_1_id)
        s.add(User(api_token=obj.api_token, id=obj.user_id))
        obj = ApiTokenFactory(user_id=user_2_id)
        s.add(User(api_token=obj.api_token, id=obj.user_id))
        await s.commit()

    async with session() as s:
        query = select(User)
        users = await s.execute(query)

    assert len(users.all()) == 2

    async with session() as s:
        await delete_user(user_1_id)

    async with session() as s:
        query = select(User)
        users = await s.execute(query)

    assert len(users.all()) == 1
