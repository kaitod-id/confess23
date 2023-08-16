from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, MessageHandler, Filters
from telegram.ext import Updater
import threading
import logging
from datetime import datetime, timedelta
from config import start, help_command, receive_confession, log_info_pengguna, turunkan_admin, angkat_admin, send_notification, status, tambah_hak, kurang_hak
from config import config
import logging
import asyncio
import configparser
from pyrogram import Client, filters, idle, emoji
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery



# Inisialisasi logger
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

def main():
    from config import setup_logging, reset_user_activity

    setup_logging()

    # Reset aktivitas pengguna setiap hari pukul 1 pagi
    reset_time = datetime.now().replace(hour=1, minute=0, second=0, microsecond=0) + timedelta(days=1)
    time_until_reset = (reset_time - datetime.now()).seconds
    threading.Timer(time_until_reset, reset_user_activity).start()

    try:
        # Buat objek Updater
        updater = Updater(token=TOKEN, use_context=True)
        dispatcher = updater.dispatcher

        # Tambahkan handler perintah
        dispatcher.add_handler(CommandHandler("start", start))
        dispatcher.add_handler(CommandHandler("help", help_command))
        dispatcher.add_handler(CommandHandler("turunkanadmin", turunkan_admin, pass_args=True))
        dispatcher.add_handler(CommandHandler("angkatadmin", angkat_admin, pass_args=True))
        dispatcher.add_handler(CommandHandler("status", status))
        dispatcher.add_handler(CommandHandler("tambahhak", tambah_hak, pass_args=True))
        dispatcher.add_handler(CommandHandler("kuranghak", kurang_hak, pass_args=True))
        dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, receive_confession))
        dispatcher.add_handler(MessageHandler(Filters.photo & ~Filters.command, receive_confession))
        dispatcher.add_handler(MessageHandler(Filters.audio & ~Filters.command, receive_confession))
        dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, send_notification))

        # Jalankan bot
        updater.start_polling()
        updater.idle()

    except Exception as e:
        logger.error("Error saat menjalankan bot: %s", str(e))

if __name__ == "__main__":
    main()
