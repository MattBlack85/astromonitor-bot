from astromonitor_bot.database.connection import connection
from astromonitor_bot.tokens import delete_all_user_tokens
from tests.factories import ApiTokenFactory


def test_delete_all_tokens():
    assert connection.count_tokens()[0] == 0

    user_1_id = 192387
    user_2_id = 691263

    for _ in range(5):
        obj = ApiTokenFactory(user_id=user_1_id)
        connection.execute("INSERT INTO api_tokens VALUES (?, ?)", (obj.api_token, obj.user_id))
    for _ in range(5):
        obj = ApiTokenFactory(user_id=user_2_id)
        connection.execute("INSERT INTO api_tokens VALUES (?, ?)", (obj.api_token, obj.user_id))

    delete_all_user_tokens(user_1_id)

    assert connection.count_tokens()[0] == 5
