import logging

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes
)

from config import BOT_TOKEN
from handlers import (
    start, 
    help_command, 
    myid,
    stats,
    battery,
    uptime,
    processes
    )

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

async def post_init(application: Application):
    commands = [
        ("start", "Start the bot"),
        ("help", "Show available commands"),
        ("myid", "Get your Telegram ID")
    ]

    await application.bot.set_my_commands(commands)

async def main():
    application = (
        Application.builder()
        .token(BOT_TOKEN)
        .post_init(post_init)
        .build()
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("myid", myid))

    application.add_handler(CommandHandler("stats", stats))
    application.add_handler(CommandHandler("battery", battery))
    application.add_handler(CommandHandler("uptime", uptime))
    application.add_handler(CommandHandler("processes", processes))

    print("Laptop Controller is running...")

    await application.initialize()
    await application.start()
    await application.updater.start_polling()

    import asyncio

    await asyncio.Event().wait()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())