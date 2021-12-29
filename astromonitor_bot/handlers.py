from telegram import Update
from telegram.ext import CallbackContext

from astromonitor_bot.tokens import generate_api_token


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text(
        """
        Here the list of available commands:

        /register => register yourself with the service and receive an API token that can be used with astromonitor
        /delete_me => delete all of your API tokens, meaning we'll forget you ever existed with us :)
        """
    )


def register(update: Update, context: CallbackContext) -> None:
    """
    Register a user, returning back an API token that the users
    can later use for webhooks
    """
    user_id = update.message.from_user.id
    api_token = generate_api_token(user_id)
    base_text = f'Your API token is:\n {api_token}'
    update.message.reply_text(base_text)
