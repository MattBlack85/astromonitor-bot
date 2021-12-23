import uuid

from astromonitor_bot.database import connection


def generate_api_token(user_id: int) -> str:
    # Generate a random UUID4 that will serve as API TOKEN
    api_token = str(uuid.uuid4())

    # Store it into the database together with the user id
    connection.execute(
        "INSERT INTO api_tokens VALUES (?, ?)", (api_token, user_id)
    )
    return api_token
