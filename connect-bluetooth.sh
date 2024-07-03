#!/bin/bash

# Bergabung dengan ZeroTier network (sesuaikan jika perlu)
sudo zerotier-cli join 56374ac9a46a7313

# Controller Bluetooth aktif dan mengatur default-agent
bluetoothctl power on
bluetoothctl agent on
bluetoothctl default-agent

# Fungsi untuk mengkoneksikan device menggunakan bluetoothctl
connect_bluetooth() {
  local bt_address=$1
  while true; do
    echo "Mencoba terhubung dengan Bluetooth device $bt_address..." &>> /var/www/nc-gym/logfile.log
    echo -e "connect $bt_address\n" | bluetoothctl &>> /var/www/nc-gym/logfile.log
    if [[ $? -eq 0 ]]; then
      echo "Terhubung dengan Bluetooth device $bt_address. Menjaga koneksi..." 
      return 0
    else
      echo "Gagal terhubung atau koneksi terputus. Mencoba kembali dalam 10 detik..."
      sleep 5
    fi
  done
}

# Fungsi untuk scan ulang perangkat bluetooth dan mencoba koneksi
scan_and_connect_bluetooth() {
  local bt_address=$1
  while true; do
    echo "Scanning for Bluetooth devices..."
    echo -e "scan on\n" | bluetoothctl &>> /var/www/nc-gym/logfile.log
    sleep 5
    echo -e "scan off\n" | bluetoothctl &>> /var/www/nc-gym/logfile.log
    if connect_bluetooth $bt_address; then
      break
    fi
  done
}

# Fungsi untuk mengkoneksikan rfcomm
connect_rfcomm() {
  local rfcomm_device=$1
  local bt_address=$2
  while true; do
    echo "Mencoba terhubung dengan rfcomm device $rfcomm_device ke $bt_address..." &>> /var/www/nc-gym/logfile.log
    sudo rfcomm connect "$rfcomm_device" "$bt_address" 
    if [[ $? -eq 0 ]]; then
      echo "Terhubung dengan rfcomm device $rfcomm_device ke $bt_address. Menjaga koneksi..." &>> /var/www/nc-gym/logfile.log
      return 0
    else
      echo "Gagal terhubung atau koneksi terputus. Mencoba kembali dalam 10 detik..." &>> /var/www/nc-gym/logfile.log
      sleep 5
    fi
  done
}

# remove DC:0D:30:93:BF:11
# pair DC:0D:30:93:BF:11
# connect DC:0D:30:93:BF:11
# connect DC:0D:30:93:BF:8C
# trust DC:0D:30:93:BF:11

# Fungsi utama untuk menghubungkan semua perangkat
connect_all_devices() {
  scan_and_connect_bluetooth DC:0D:30:93:BF:11 &
  scan_and_connect_bluetooth DC:0D:30:93:BF:8C &
  # connect_rfcomm rfcomm1 98:D3:31:FB:5F:57 &
  # connect_rfcomm rfcomm0 98:D3:31:FB:5E:5C &

  # Menunggu sampai semua koneksi berhasil
  wait

  # Jika semua koneksi berhasil, tandai sukses
  return 0
}

# Fungsi untuk menjalankan skrip Python
run_python_script() {
  while true; do
    echo "Menjalankan skrip Python..."
    
    # if ! timeout 10 python /var/www/nc-gym/bt5.py &>> /var/www/nc-gym/logfilepy.log; then
    #   echo "bt5.py encountered an error. Mencoba kembali dalam 10 detik..." &>> /var/www/nc-gym/logfilepy.log
    #   sleep 10
    # else
    #   sleep 5
    # fi
    
    if ! timeout 10 python /var/www/nc-gym/command.py &>> /var/www/nc-gym/logfilepy.log; then
      echo "command.py encountered an error. Mencoba kembali dalam 10 detik..." &>> /var/www/nc-gym/logfilepy.log
      sleep 10
    else
      sleep 5
    fi
    
  done
}

# Fungsi untuk mengecek status koneksi perangkat Bluetooth
check_connections() {
  local addresses=("DC:0D:30:93:BF:11" "DC:0D:30:93:BF:8C" "98:D3:31:FB:5F:57" "98:D3:31:FB:5E:5C")
  for address in "${addresses[@]}"; do
    if ! bluetoothctl info "$address" | grep -q "Connected: yes"; then
      echo "Device $address tidak terhubung. Restarting Bluetooth service..."
      sudo systemctl restart bluetooth
      sudo systemctl daemon-reload
      sudo systemctl restart connect-bluetooth.service
      return 1
    fi
  done
  return 0
}

# Jalankan skrip Python di latar belakang
run_python_script &

# Jalankan fungsi utama untuk menghubungkan semua perangkat
while true; do
  if connect_all_devices; then
    echo "Semua perangkat terhubung dengan sukses. Memantau koneksi..." &>> /var/www/nc-gym/logfile.log
  else
    # sudo systemctl restart bluetooth
    # sudo systemctl daemon-reload
    # sudo systemctl restart connect-bluetooth.service
    # echo "Terjadi masalah saat menghubungkan perangkat. Mencoba kembali dalam 10 detik..." &>> /var/www/nc-gym/logfile.log
    # sleep 5
  fi

  # Periksa koneksi setiap 60 detik
  # sleep 10
  # check_connections
done