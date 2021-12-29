import falcon.asgi

from astromonitor_bot.bot import bot, start_bot
from astromonitor_bot.database.connection import connection


class AstroMonitor:
    async def on_post(self, req, resp, api_token):
        # check the token exists in the DB
        # fire a request to telegram to notify the user
        query = connection.execute(
            """
            SELECT api_token, user_id from api_tokens WHERE api_token = '%s'
            """
            % api_token
        ).fetchone()

        if query:
            _, user_id = query
            bot.send_message(user_id, 'Kstars crashed! Please check it')
            resp.status = falcon.HTTP_200
        else:
            resp.status = falcon.HTTP_404


connection.start()
app = falcon.asgi.App()
app.add_route('/hook/{api_token:uuid}', AstroMonitor())
start_bot()
