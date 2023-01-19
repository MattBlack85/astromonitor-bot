import uuid

from astromonitor_bot.database import session
from astromonitor_bot.database.models import User


async def generate_api_token(user_id: int) -> str:
    # Store it into the database together with the user id
    async with session() as s:
        # Check first if we have already such a user, a user will always
        # have 1 token
        user = await s.get(User, user_id)

        if not user:
            # Generate a random UUID4 that will serve as API TOKEN
            api_token = str(uuid.uuid4())
            user = User(api_token=api_token, id=user_id)
            s.add(user)
            await s.commit()
        else:
            api_token = user.api_token

    return api_token


async def delete_user(user_id: int) -> None:
    async with session() as s:
        user = await s.get(User, user_id)
        await s.delete(user)
        await s.commit()
