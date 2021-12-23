from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from astromonitor_bot.tokens import generate_api_token


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Still to be implemented')


def register(update: Update, context: CallbackContext) -> None:
    """
    Register a user, returning back an API token that the users
    can later use for webhooks
    """
    user_id = update.message.from_user.id
    api_token = generate_api_token(user_id)
    base_text = f'Your API token is:\n {api_token}'
    update.message.reply_text(base_text)
