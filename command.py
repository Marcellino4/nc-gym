import logging
import subprocess
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Token API Telegram Anda
TELEGRAM_BOT_TOKEN = '7243366231:AAGxqP4QhS_cPv1-JHfN5NbFrT1wk7Y-TBk'

# Mengatur logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Fungsi untuk menangani perintah /start
async def restart(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Testing restart masbroooo')

# # Fungsi untuk menangani perintah /restart
# async def restart(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     chat_id = update.message.chat_id
#     user = update.message.from_user
#     logger.info(f"User {user.first_name} issued /restart command")

#     # Mengirim pesan konfirmasi ke Telegram
#     await update.message.reply_text('Restarting Bluetooth service...')

#     # Menjalankan perintah sistem
#     try:
#         subprocess.run(['sudo', 'systemctl', 'restart', 'bluetooth'], check=True)
#         subprocess.run(['sudo', 'systemctl', 'daemon-reload'], check=True)
#         subprocess.run(['sudo', 'systemctl', 'restart', 'connect-bluetooth.service'], check=True)
#         await update.message.reply_text('Bluetooth service restarted successfully.')
#     except subprocess.CalledProcessError as e:
#         logger.error(f"Error restarting services: {e}")
#         await update.message.reply_text(f'Failed to restart Bluetooth service: {e}')

def main() -> None:
    # Membuat application dan pass the bot's token.
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Mendapatkan dispatcher untuk mendaftarkan handler
    application.add_handler(CommandHandler("restart", start))
    # application.add_handler(CommandHandler("restart", restart))

    # Mulai bot
    application.run_polling()

if __name__ == '__main__':
    main()