import logging
import subprocess
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Token API Telegram Anda
TELEGRAM_BOT_TOKEN = '7243366231:AAGxqP4QhS_cPv1-JHfN5NbFrT1wk7Y-TBk'

# Mengatur logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Fungsi untuk menangani perintah /start
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hello! I am your bot. Use /restart to restart the Bluetooth service.')

# Fungsi untuk menangani perintah /restart
# def restart(update: Update, context: CallbackContext) -> None:
#     chat_id = update.message.chat_id
#     user = update.message.from_user
#     logger.info(f"User {user.first_name} issued /restart command")

#     # Mengirim pesan konfirmasi ke Telegram
#     update.message.reply_text('Restarting Bluetooth service...')

#     # Menjalankan perintah sistem
#     try:
#         subprocess.run(['sudo', 'systemctl', 'restart', 'bluetooth'], check=True)
#         subprocess.run(['sudo', 'systemctl', 'daemon-reload'], check=True)
#         subprocess.run(['sudo', 'systemctl', 'restart', 'connect-bluetooth.service'], check=True)
#         update.message.reply_text('Bluetooth service restarted successfully.')
#     except subprocess.CalledProcessError as e:
#         logger.error(f"Error restarting services: {e}")
#         update.message.reply_text(f'Failed to restart Bluetooth service: {e}')

def main() -> None:
    # Membuat updater dan pass the bot's token.
    updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)

    # Mendapatkan dispatcher untuk mendaftarkan handler
    dispatcher = updater.dispatcher

    # Pada /start command, jalankan fungsi start
    dispatcher.add_handler(CommandHandler("start", start))

    # Pada /restart command, jalankan fungsi restart
    # dispatcher.add_handler(CommandHandler("restart", restart))

    # Mulai bot
    updater.start_polling()

    # Bot akan terus berjalan sampai Anda menghentikannya
    updater.idle()

if __name__ == '__main__':
    main()