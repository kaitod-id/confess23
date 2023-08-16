from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, MessageHandler, Filters
from telegram.ext import Updater
import threading
import logging
from datetime import datetime, timedelta
from config import start, help_command, receive_confession, send_notification, status, tambah_hak, kurang_hak

# Konfigurasi bot Anda
TOKEN = "6344639589:AAEIxPkMYUUr2K6PloxytU"

def main():
    # Inisialisasi logger
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    logger = logging.getLogger(__name__)

    try:
        # Buat objek Updater
        updater = Updater(token=TOKEN, use_context=True)
        dispatcher = updater.dispatcher

        # Tambahkan handler perintah
        dispatcher.add_handler(CommandHandler("start", start))
        dispatcher.add_handler(CommandHandler("help", help_command))
        dispatcher.add_handler(CommandHandler("status", status))
        dispatcher.add_handler(CommandHandler("tambahhak", tambah_hak, pass_args=True))
        dispatcher.add_handler(CommandHandler("kuranghak", kurang_hak, pass_args=True))
        dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, receive_confession))
        dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, send_notification))

        # Jalankan bot
        updater.start_polling()
        updater.idle()

    except Exception as e:
        logger.error("Error saat menjalankan bot: %s", str(e))

if __name__ == "__main__":
    main()
