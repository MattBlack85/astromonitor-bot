import os

import falcon.asgi
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from telegram import Bot

from astromonitor_bot.database import session
from astromonitor_bot.database.models import User

TOKEN = os.environ['TELEGRAM_TOKEN']
bot = Bot(TOKEN)


class AstroMonitor:
    async def on_post(self, req, resp, api_token):
        # check the token exists in the DB
        # fire a request to telegram to notify the user
        async with session() as s:
            try:
                query = select(User).filter_by(api_token=str(api_token))
                q = await s.scalars(query)
                user = q.one()
                await bot.send_message(user.id, 'Kstars crashed! Please check it')
                resp.status = falcon.HTTP_200
            except NoResultFound:
                resp.status = falcon.HTTP_404


class Backup:
    async def on_post(self, req, resp, api_token):
        body = await req.stream.read()

        with open("/tmp/falcon_read.tar", "wb") as f:
            f.write(body)
        resp.status = falcon.HTTP_200


app = falcon.asgi.App()
app.add_route('/hook/{api_token:uuid}', AstroMonitor())
app.add_route('/backup/db/{api_token:uuid}', Backup())
