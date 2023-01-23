from telegram import Update
from telegram.ext import CallbackContext

from astromonitor_bot.tokens import delete_user, generate_api_token


async def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text(
        """
Here the list of available commands:

/register => register yourself with the service and receive an API token that can be used with astromonitor

/delete_me => delete your API token, meaning we'll forget you ever existed with us :)
        """
    )


async def register(update: Update, context: CallbackContext) -> None:
    """
    Register a user, returning back an API token that the users
    can later use for webhooks
    """
    user_id = update.message.from_user.id
    api_token = await generate_api_token(user_id)
    base_text = f"""
Your API token is:
{api_token}
"""
    await update.message.reply_text(base_text)


async def delete_user_token(update: Update, context: CallbackContext) -> None:
    """
    Delete all tokens for a given user
    """
    user_id = update.message.from_user.id
    await delete_user(user_id)
    await update.message.reply_text("Your token have been deleted")


async def start_command(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        """
Welcome to astromonitor!

This bot together with the astromonitor program you can install on your pc can help you with some things:
 - monitoring Kstars and notify you via telegram if it crashes
 - saving Kstars/INDI backups
 - restoring the previously saved backup
 - monitor the performance of your OS while running Kstars
 - monitor the file descriptors to check if there is any leak

To start, you need to receive an API TOKEN you can then use with astromonitor.

To install astromonitor refer to this guide: https://github.com/MattBlack85/astro_monitor#install

If you are using AstroArch astromonitor is already installed!

To see the available telegram commands type /help

To see what commands can be used with astromonitor type in the terminal on the computer where it's installed astromonitor --help


For any issue please reach out to me directly at matto.astro@gmail.com
        """  # NOQA
    )
