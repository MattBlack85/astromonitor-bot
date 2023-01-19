import asyncio
import logging
import os
import sys

sys.path.append("../")  # NOQA

import uvicorn  # NOQA
from telegram import Bot  # NOQA
from telegram.ext import Application, CommandHandler  # NOQA

from astromonitor_bot import handlers  # NOQA
from astromonitor_bot.server import app  # NOQA

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

TOKEN = os.environ['TELEGRAM_TOKEN']


telegram_app = Application.builder().token(TOKEN).build()


async def start() -> None:
    # on different commands - answer in Telegram
    telegram_app.add_handler(CommandHandler('help', handlers.help_command))
    telegram_app.add_handler(CommandHandler('register', handlers.register))
    telegram_app.add_handler(CommandHandler('delete_me', handlers.delete_user_token))

    webserver = uvicorn.Server(config=uvicorn.Config(app, host="127.0.0.1", port=9050, log_level="info"))
    # Start the updater for the bot and the falcon API
    async with telegram_app:
        await telegram_app.start()
        await telegram_app.updater.start_polling()
        await webserver.serve()
        await telegram_app.updater.stop()
        await telegram_app.stop()


if __name__ == '__main__':
    asyncio.run(start())
