#!/bin/bash

# Token API Telegram Anda
TELEGRAM_BOT_TOKEN="7243366231:AAGxqP4QhS_cPv1-JHfN5NbFrT1wk7Y-TBk"
# Ganti dengan chat ID yang Anda dapatkan dari getUpdates
CHAT_ID="-1002204066531"

# Fungsi untuk mengirim pesan ke Telegram
send_telegram_message() {
  local message=$1
  local max_length=4096
  local part
  
  # Escape karakter khusus untuk HTML
  message=$(echo "$message" | sed 's/&/&amp;/g; s/</&lt;/g; s/>/&gt;/g; s/"/&quot;/g; s/'"'"'/&apos;/g')

  while [ ${#message} -gt $max_length ]; do
    part=${message:0:$max_length}
    message=${message:$max_length}
    curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
         -d chat_id=${CHAT_ID} \
         -d text="${part}" \
         -d parse_mode="MarkdownV2" >/dev/null 2>&1
  done

  curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
       -d chat_id=${CHAT_ID} \
       -d text="${message}" \
       -d parse_mode="MarkdownV2" >/dev/null 2>&1
}


send_telegram_message2() {
  local message=$1
  curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
       -d chat_id=${CHAT_ID} \
       -d text="${message}" \
       -d parse_mode="HTML"
}

# Fungsi untuk mengecek status koneksi perangkat Bluetooth
check_connections() {
  local addresses=("DC:0D:30:93:BF:11" "DC:0D:30:93:BF:8C" "98:D3:31:FB:5F:57" "98:D3:31:FB:5E:5C")
  local connected_addresses=($(hcitool con | grep -oP '([0-9A-F]{2}:){5}[0-9A-F]{2}'))
  local hcitool_output=$(hcitool con)
  local loopnum = 0;

  for address in "${addresses[@]}"; do
    # send_telegram_message "connectnya : ${address}"
    # send_telegram_message "harusnya : ${connected_addresses[loopnum]}"
    if [[ "${address}" != "${connected_addresses[loopnum]}" ]]; then
      echo "$(date): Device $address tidak terhubung. Restarting Bluetooth service..." &>> /var/www/nc-gym/logfile.log

      # Mengirim hasil dari hcitool con ke Telegram
      send_telegram_message "Hasil dari hcitool con:\`\`\`${hcitool_output}\`\`\`"
      send_telegram_message2 "Device $address tidak terhubung. Restarting Bluetooth service..."
      send_telegram_message2 "--------------------------------"

      sudo systemctl restart bluetooth
      sudo systemctl daemon-reload
      sudo systemctl restart connect-bluetooth.service
      return 1
    else
      echo "$(date): Device $address terhubung." &>> /var/www/nc-gym/logfile.log
      # send_telegram_message2 "Device $address terhubung."
    fi
    loopnum=$((loopnum + 1))
  done
  return 0
}

# Jalankan pengecekan dan log hasilnya
check_connections &>> /var/www/nc-gym/check_connections.log