#!/bin/bash

# Konfigurasi
LOGFILE="/var/www/nc-gym/startup.log"
TELEGRAM_BOT_TOKEN="7243366231:AAGxqP4QhS_cPv1-JHfN5NbFrT1wk7Y-TBk"
TELEGRAM_CHAT_ID="-1002204066531"
API_URL="https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/sendMessage"

# Buat file log
exec > >(tee -a "$LOGFILE") 2>&1

send_telegram_message() {
    local message="$1"
    curl -s -X POST $API_URL -d chat_id=$TELEGRAM_CHAT_ID -d text="$message"
}

# echo "Starting Bluetooth connection..."
# send_telegram_message "Starting Bluetooth connection..."
# lxterminal -e "bluetoothctl && connect DC:0D:30:93:BF:11; exec bash"

# # Tunggu beberapa detik agar bluetoothctl selesai
# sleep 10

# echo "Connecting rfcomm0..."
# send_telegram_message "Connecting rfcomm0..."
# lxterminal -e "sudo rfcomm connect rfcomm0 98:D3:31:FB:5E:5C; exec bash"

# echo "Connecting rfcomm1..."
# send_telegram_message "Connecting rfcomm1..."
# lxterminal -e "sudo rfcomm connect rfcomm1 98:D3:31:FB:5F:57; exec bash"

# # Tunggu beberapa detik agar rfcomm selesai
# sleep 10

echo "Running Python scripts..."
send_telegram_message "Running Python scripts..."
lxterminal -e "cd /var/www/nc-gym && python test3.py; exec bash"
# lxterminal -e "cd /var/www/nc-gym && python test2.py; exec bash"

# Kirimkan log ke Telegram setelah semua perintah selesai
send_telegram_message "Startup script completed. Log:\n$(cat $LOGFILE)"