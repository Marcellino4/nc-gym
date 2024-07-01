#!/bin/bash

# Fungsi untuk mengecek status koneksi perangkat Bluetooth
check_connections() {
  local addresses=("DC:0D:30:93:BF:11" "DC:0D:30:93:BF:8C" "98:D3:31:FB:5F:57" "98:D3:31:FB:5E:5C")
  local connected_addresses=($(hcitool con | grep -oP '([0-9A-F]{2}:){5}[0-9A-F]{2}'))
  
  for address in "${addresses[@]}"; do
    if [[ ! " ${connected_addresses[@]} " =~ " ${address} " ]]; then
      echo "Device $address tidak terhubung. Restarting Bluetooth service..." &>> /var/www/nc-gym/logfile.log
      sudo systemctl restart bluetooth
      sudo systemctl daemon-reload
      sudo systemctl restart connect-bluetooth.service
      return 1
    fi
  done
  return 0
}

# Loop untuk menjalankan pengecekan setiap 10 detik
while true; do
  check_connections
  sleep 45
done