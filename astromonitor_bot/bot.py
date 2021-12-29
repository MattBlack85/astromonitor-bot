import logging
import os

from telegram.bot import Bot
from telegram.ext import CommandHandler, Updater

from astromonitor_bot import handlers

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

TOKEN = os.environ['TELEGRAM_TOKEN']

bot = Bot(TOKEN)


def start_bot() -> None:
    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler('help', handlers.help_command))
    dispatcher.add_handler(CommandHandler('register', handlers.register))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    # updater.idle()


if __name__ == '__main__':
    start_bot()
