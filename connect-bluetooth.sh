#!/bin/bash

# Bergabung dengan ZeroTier network (sesuaikan jika perlu)
sudo zerotier-cli join 56374ac9a46a7313

# Controller Bluetooth aktif dan mengatur default-agent
bluetoothctl power on
bluetoothctl agent on
bluetoothctl default-agent

# Menandai device sebagai trusted (uncomment jika perlu)
# bluetoothctl trust DC:0D:30:93:BF:11 #PB008
# bluetoothctl trust DC:0D:30:93:BF:8C #PB0081
# bluetoothctl trust 98:D3:31:FB:5F:57 #Mikro2
# bluetoothctl trust 98:D3:31:FB:5E:5C #Mikro3

# Melakukan binding terhadap rfcomm0 dan rfcomm1 (uncomment jika perlu)
# rfcomm bind rfcomm0 98:D3:31:FB:5E:5C 1
# rfcomm bind rfcomm1 98:D3:31:FB:5F:57 1
# sleep 5


# Fungsi untuk mengkoneksikan device menggunakan bluetoothctl
connect_bluetooth() {
  local bt_address=$1
  while true; do
    echo "Mencoba terhubung dengan Bluetooth device $bt_address..."
    echo -e "connect $bt_address\nquit" | bluetoothctl &> /var/www/nc-gym/logfile.log
    if [[ $? -eq 0 ]]; then
      echo "Terhubung dengan Bluetooth device $bt_address. Menjaga koneksi..."
      sleep 2
    else
      echo "Gagal terhubung atau koneksi terputus. Mencoba kembali dalam 10 detik..."
      sleep 2
    fi
  done
}


# Menghubungkan Bluetooth ke perangkat
connect_bluetooth DC:0D:30:93:BF:8C &
connect_bluetooth DC:0D:30:93:BF:11 &

# Fungsi untuk mengkoneksikan rfcomm
connect_rfcomm() {
  local rfcomm_device=$1
  local bt_address=$2
  while true; do
    echo "Mencoba terhubung dengan rfcomm device $rfcomm_device ke $bt_address..."
    sudo rfcomm connect "$rfcomm_device" "$bt_address" &> /var/www/nc-gym/logfile.log
    if [[ $? -eq 0 ]]; then
      echo "Terhubung dengan rfcomm device $rfcomm_device ke $bt_address. Menjaga koneksi..."
      sleep 2
    else
      echo "Gagal terhubung atau koneksi terputus. Mencoba kembali dalam 10 detik..."
      sleep 2
    fi
  done
}
# Menghubungkan rfcomm devices
connect_rfcomm rfcomm1 98:D3:31:FB:5F:57 &
connect_rfcomm rfcomm0 98:D3:31:FB:5E:5C &
sleep 2
# Menjalankan perintah python
if ! timeout 30 python /var/www/nc-gym/bt5.py &> /var/www/nc-gym/logfilepy.log; then
    echo "Python script encountered an error" &> /var/www/nc-gym/logfilepy.log
fi