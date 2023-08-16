import logging
import threading
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import CallbackContext

# Pengaturan bot
TOKEN = '6344639589:AAEIxPkMYUUr2K6PloxytU-CR-oeMYLeErU'
CHANNEL_1_ID = -1001825244023  # Ganti dengan ID channel tujuan 1
CHANNEL_2_ID = -1001855788004  # Ganti dengan ID channel tujuan 2
OWNER_ID = 1753533568  # Ganti dengan ID pemilik
CREATOR_ID = 5633222043  # Ganti dengan ID creator
ADMIN_IDS = [OWNER_ID, CREATOR_ID, 5633222043]  # Tambahkan CREATOR_ID ke daftar admin

# Kamus untuk menyimpan aktivitas pengguna
USER_ACTIVITY = {}

# Daftar pengguna yang dibatasi
BANNED_USERS = []

def setup_logging():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def reset_user_activity():
    global USER_ACTIVITY
    USER_ACTIVITY = {}

# Fungsi untuk memeriksa apakah pengguna adalah pemilik atau creator
def adalah_pemilik(update: Update):
    return update.effective_user.id == OWNER_ID or update.effective_user.id == CREATOR_ID

# Fungsi untuk mengirim notifikasi dan tautan pesan
def send_notification(update: Update, context: CallbackContext):
    update.message.reply_text("Pengakuan Anda telah berhasil terkirim!")
    user_id = update.effective_user.id
    message_id = update.message.message_id
    chat_id = update.message.chat_id
    message_link = f"https://t.me/{context.bot.username}/{chat_id}?message={message_id}"
    update.message.reply_text(f"Anda dapat melihat pengakuan Anda di sini:\n{message_link}")

# Fungsi untuk memulai bot
def start(update: Update, context: CallbackContext):
    user_id = update.effective_user.id

    if user_id not in USER_ACTIVITY:
        USER_ACTIVITY[user_id] = {'count': 0, 'last_submission': datetime.now()}

    current_time = datetime.now()
    if current_time.day != USER_ACTIVITY[user_id]['last_submission'].day:
        USER_ACTIVITY[user_id] = {'count': 0, 'last_submission': current_time}

    if USER_ACTIVITY[user_id]['count'] >= 3:
        update.message.reply_text("Anda telah mencapai batas maksimal pengiriman menfess hari ini.")
        return

    update.message.reply_text("Hai! Selamat datang di bot pengakuan anonim. Gunakan perintah /help untuk bantuan.")

# Fungsi untuk menampilkan bantuan
def help_command(update: Update, context: CallbackContext):
    update.message.reply_text("Gunakan perintah berikut:\n\n/start - Memulai penggunaan bot\n/help - Menampilkan pesan bantuan\n/menfess [Pesan] - Mengirim pesan anonim\n/status - Menampilkan informasi Anda")
    user_id = update.effective_user.id
    context.bot.send_message(user_id, "Jika Anda ingin mengirim pesan anonim, gunakan perintah /menfess [Pesan].")

# Fungsi untuk menerima pengakuan
def receive_confession(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    message = update.message
    message_text = message.text.lower()
    message_caption = message.caption.lower() if message.caption else ""

    valid_hashtags = [
        "#rpconfess", "#rpmenfess", "#rpmfs",
        "#rpcurhat", "#rprandom", "#rpnanyea",
        "#rpgalau", "#rpgamon", "#rpgabut",
        "#rphates", "#rpjokes"
    ]
    
    if any(hashtag in message_text for hashtag in valid_hashtags) or \
       any(hashtag in message_caption for hashtag in valid_hashtags):
        
        if message.text:
            context.bot.send_message(CHANNEL_1_ID, f"Pengakuan teks dari pengguna {user_id}:\n{message_text}")
        elif message.photo:
            context.bot.send_photo(CHANNEL_1_ID, message.photo[-1].file_id, caption=f"Pengakuan gambar dari pengguna {user_id}")
        elif message.audio:
            context.bot.send_audio(CHANNEL_1_ID, message.audio.file_id, caption=f"Pengakuan audio dari pengguna {user_id}")

        # Kirim notifikasi dan tautan pesan
        send_notification(update, context)

    else:
        pesan = "Pesan Anda tidak mengandung hashtag yang valid untuk menfess. Gunakan salah satu dari hashtag berikut:\n\n" + "\n".join(valid_hashtags)
        update.message.reply_text(pesan)

# Fungsi untuk menampilkan informasi pengguna dan admin
def status(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    user_info = f"ID Pengguna: {user_id}\n"
    user_info += f"Username: {update.effective_user.username}\n"
    user_info += f"Nama: {update.effective_user.first_name} {update.effective_user.last_name}\n"

    if user_id == OWNER_ID or user_id == CREATOR_ID:
        user_info += f"\nAdmins: {', '.join(str(admin_id) for admin_id in ADMIN_IDS)}"
        user_info += f"\nDaftar Terbatas: {', '.join(str(banned_user) for banned_user in BANNED_USERS)}"

    update.message.reply_text(user_info)

# Fungsi untuk mengubah hak pengguna
def ubah_hak_pengguna(update: Update, context: CallbackContext, mode, target_id):
    if update.effective_user.id in [OWNER_ID, CREATOR_ID]:
        if target_id in BANNED_USERS:
            if mode == "tambah":
                BANNED_USERS.remove(target_id)
                update.message.reply_text("Hak kirim menfess telah diberikan kepada pengguna.")
            elif mode == "kurang":
                update.message.reply_text("Pengguna sudah memiliki hak kirim menfess.")
        else:
            if mode == "tambah":
                update.message.reply_text("Pengguna sudah memiliki hak kirim menfess.")
            elif mode == "kurang":
                BANNED_USERS.append(target_id)
                update.message.reply_text("Hak kirim menfess telah dihapus dari pengguna.")
    else:
        update.message.reply_text("Anda tidak memiliki izin untuk melakukan ini.")

# Fungsi untuk menambah hak pengguna
def tambah_hak(update: Update, context: CallbackContext, target_id):
    ubah_hak_pengguna(update, context, "tambah", target_id)

# Fungsi untuk mengurangi hak pengguna
def kurang_hak(update: Update, context: CallbackContext, target_id):
    ubah_hak_pengguna(update, context, "kurang", target_id)
