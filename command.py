import logging
import subprocess
import re
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.error import TimedOut

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

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    help_text = (
        "Available commands:\n"
        "/help - Show this help message\n"
        "/restart - Restart the Bluetooth service\n"
        "/hcitool - Run a hcitool and show the results\n"
        "/speedtest - Run a speedtest and show the results\n"
        "/evtest - Run a evtest and show the event\n"
    )
    await update.message.reply_text(help_text)

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
        await update.message.reply_text('SPEEDTEST LAGI JALAN.. MOHON BERSABAR')

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

async def evtest(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat_id
    user = update.message.from_user
    logger.info(f"User {user.first_name} issued /evtest command")

    try:
        # Menjalankan perintah untuk mendapatkan daftar perangkat input
        result = subprocess.run(['sudo', 'evtest'], capture_output=True, text=True, input=b'\n')
        output = result.stdout

        # Memilih perangkat input secara otomatis (misalnya perangkat pertama)
        match = re.search(r'/dev/input/event\d+', output)
        if match:
            device = match.group(0)
            result = subprocess.run(['sudo', 'evtest', device], capture_output=True, text=True)
            output = result.stdout

            # Escape karakter khusus untuk MarkdownV2
            output = re.sub(r'([_*$begin:math:display$$end:math:display$()~`>#+\-={}!.])', r'\\\1', output)

            # Potong pesan jika terlalu panjang
            max_length = 4096
            parts = [output[i:i + max_length] for i in range(0, len(output), max_length)]

            for part in parts:
                await update.message.reply_text(f'Hasil dari evtest:\n```\n{part}\n```', parse_mode='MarkdownV2')
        else:
            await update.message.reply_text('Tidak ada perangkat input yang ditemukan.')

    except subprocess.CalledProcessError as e:
        logger.error(f"Error running evtest: {e}")
        await update.message.reply_text(f'Failed to run evtest: {e}')
    except TimedOut:
        logger.error("Request timed out")
        await update.message.reply_text("Request timed out while trying to run evtest.")

def main() -> None:
    # Membuat application dan pass the bot's token.
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Mendapatkan dispatcher untuk mendaftarkan handler
    application.add_handler(CommandHandler("restart", restart))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("hcitool", hcitool))
    application.add_handler(CommandHandler("speedtest", speedtest))
    application.add_handler(CommandHandler("evtest", evtest))

    async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        logger.error(msg="Exception while handling an update:", exc_info=context.error)
        try:
            raise context.error
        except TimedOut:
            await update.message.reply_text("Request timed out. Please try again.")
        except Exception as e:
            await update.message.reply_text(f"An error occurred: {e}")

    application.add_error_handler(error_handler)

    # Mulai bot
    application.run_polling()

if __name__ == '__main__':
    main()