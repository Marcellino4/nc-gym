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

def main() -> None:
    # Membuat updater dan pass the bot's token.
    updater = Updater(TELEGRAM_BOT_TOKEN)

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