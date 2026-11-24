import asyncio
import datetime
import psutil

from telegram import Update
from telegram.ext import ContextTypes

from config import ADMIN_USER_ID

import system_monitor


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
        "⚙ General\n"
        "/start - Start the bot\n"
        "/help - Show available commands\n"
        "/myid - Get your Telegram user ID\n\n"
        "📊 Monitoring\n"
        "/stats - System statistics\n"
        "/battery - Battery information\n"
        "/uptime - System uptime\n"
        "/processes - Top processes by RAM\n"
    )

    await update.message.reply_text(message)

async def myid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    if user is None:
        return
    
    await update.message.reply_text(
        f"Your Telegram ID: {user.id}"
    )

async def stats(update: Update, context:ContextTypes.DEFAULT_TYPE):
    if not await is_authorized(update):
        await update.message.reply_text("Access denied.")
        return
    
    cpu = await asyncio.to_thread(system_monitor.get_cpu_ussage)
    memory = system_monitor.get_memory_info()
    disk = system_monitor.get_disk_info

    message = (
        "💻 Laptop Status\n\n"
        f"⚙️ CPU: {cpu}%\n"
        f"🧠 RAM: {memory.percent}% "
        f"({memory.used / (1024 ** 3):.2f} / "
        f"{memory.total / (1024 ** 3):.2f} GB)\n"
        f"💾 Disk (C:): {disk.percent}% "
        f"({disk.used / (1024 ** 3):.2f} / "
        f"{disk.total / (1024 ** 3):.2f} GB)"
    )

    await update.message.reply_text(message)

async def battery(update: Update, context:ContextTypes.DEFAULT_TYPE):
    if not await is_authorized(update):
        await update.message.reply_text("Access denied.")
        return
    
    battery_info = system_monitor.get_battery_info()

    if battery_info is None:
        await update.message.reply_text(
            "🔋 Battery information is unavailable",
            "Your device may not have a battery"
        )
        return
    
    status = "⚡ Charging" if battery_info.power_plugged else "🔋 Discharging"

    if battery_info.secsleft == psutil.POWER_TIME_UNLIMITED:
        remaining = "Calculating..."
    elif battery_info.secsleft == psutil.POWER_TIME_UNKNOWN:
        remaining = "Unknown..."
    else:
        seconds = battery_info.secsleft
        hours, remainder = divmod(seconds, 3600)
        minutes = remainder // 60
        remaining = f"{hours}h {minutes}m"
    
    message = (
        "🔋 Battery Status\n\n"
        f"Charge: {battery_info.percent}%\n"
        f"Status: {status}\n"
        f"Time remaining: {remaining}"
    )

    await update.message.reply_text(message)

async def uptime(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_authorized(update):
        await update.message.reply_text("Access denied.")
        return
    
    duration, boot_time = system_monitor.get_uptime()

    total_seconds = int(duration.total_seconds())

    days, remainder = divmod(total_seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)

    uptime_text = (
        f"{days}d {hours}h {minutes}m {seconds}s"
    )

    message = (
        "⏱ System Uptime\n\n"
        f"Running for: {uptime_text}\n"
        f"Last boot: {boot_time.strftime('%d.%m.%Y %H:%M:%S')}"
    )

    await update.message.reply_text(message)

async def processes(update: Update, context:ContextTypes.DEFAULT_TYPE):
    if not await is_authorized:
        await update.message.reply_text("Access denied.")
        return
    
    top_processes = await asyncio.to_thread(
        system_monitor.get_top_processes(),
        10
    )

    lines = ["📋 Top processes by RAM\n"]

    for index, process in enumerate(top_processes, start=1):
        memory_mb = process["memory"] / (1024 ** 2)

        lines.append(
            f"{index}. {process['name']}\\n"
            f"   PID: {process['pid']} | RAM: {memory_mb:.1f} MB"
        )

        message = "\n".join(lines)

        await update.message.reply_text(message)