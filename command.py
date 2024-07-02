import logging
import subprocess
import re
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

async def hcitool(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat_id
    user = update.message.from_user
    logger.info(f"User {user.first_name} issued /hcitool command")

    # Menjalankan perintah sistem
    try:
        result = subprocess.run(['hcitool', 'con'], check=True, capture_output=True, text=True)
        output = result.stdout
        await update.message.reply_text(f'Hasil dari hcitool con:\n```\n{output}\n```', parse_mode='MarkdownV2')
    except subprocess.CalledProcessError as e:
        logger.error(f"Error running hcitool: {e}")
        await update.message.reply_text(f'Failed to run hcitool: {e}')

# Fungsi untuk menangani perintah /speedtest
async def speedtest(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat_id
    user = update.message.from_user
    logger.info(f"User {user.first_name} issued /speedtest command")

    # Menjalankan perintah sistem
    try:
        result = subprocess.run(['speedtest', '--simple'], check=True, capture_output=True, text=True)
        output = result.stdout

        # Escape karakter khusus untuk MarkdownV2
        def escape_markdown_v2(text):
            escape_chars = r'_*[]()~`>#+-=|{}.!'
            return re.sub(f'([{re.escape(escape_chars)}])', r'\\\1', text)

        output = escape_markdown_v2(output)
        
        # Potong pesan jika terlalu panjang
        max_length = 4096
        parts = [output[i:i + max_length] for i in range(0, len(output), max_length)]

        for part in parts:
            await update.message.reply_text(f'Hasil dari speedtest:\n```\n{part}\n```', parse_mode='MarkdownV2')

    except subprocess.CalledProcessError as e:
        logger.error(f"Error running speedtest: {e}")
        await update.message.reply_text(f'Failed to run speedtest: {e}')

def main() -> None:
    # Membuat application dan pass the bot's token.
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Mendapatkan dispatcher untuk mendaftarkan handler
    application.add_handler(CommandHandler("restart", restart))
    application.add_handler(CommandHandler("hcitool", hcitool))
    application.add_handler(CommandHandler("speedtest", speedtest))
    # application.add_handler(CommandHandler("restart", restart))

    # Mulai bot
    application.run_polling()

if __name__ == '__main__':
    main()