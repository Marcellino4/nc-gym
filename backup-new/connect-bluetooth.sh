#!/bin/bash

# Bergabung dengan ZeroTier network (sesuaikan jika perlu)
sudo zerotier-cli join 56374ac9a46a7313

# Controller Bluetooth aktif dan mengatur default-agent
bluetoothctl power on
bluetoothctl agent on
bluetoothctl default-agent

# Menjalankan skrip Python
python /var/www/nc-gym/command.py &>> /var/www/nc-gym/logfilepy.log

# Menjaga skrip tetap berjalan
while true; do
  sleep 60
done