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

send_telegram_message "Starting Orangepi..."