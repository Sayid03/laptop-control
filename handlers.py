from telegram import Update
from telegram.ext import ContextTypes

from config import ADMIN_USER_ID


async def is_authorized(update: Update) -> bool:
    user = update.effective_user

    if user is None:
        return False
    
    return user.id == ADMIN_USER_ID

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_authorized(update):
        await update.message.reply_text("Access denied.")
        return
    
    await update.message.reply_text(
        "Welcome to Laptop Controller!\n\n"
        "Your remote control bot is online.\n"
        "Use /help to see available commands."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_authorized(update):
        await update.message.reply_text("Access denied.")
        return
    
    message = (
        "Laptop Controller — Commands\n\n"
        "/start - Start the bot\n"
        "/help - Show available commands\n"
        "/myid - Get your Telegram user ID"
    )

    await update.message.reply_text(message)

async def myid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    if user is None:
        return
    
    await update.message.reply_text(
        f"Your Telegram ID: {user.id}"
    )