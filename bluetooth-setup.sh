ss#!/bin/bash

# untuk menjalankan zerotier 
sudo zerotier-cli join 56374ac9a46a7313

# Pastikan layanan Bluetooth sudah berjalan
sudo systemctl start bluetooth

# Scan perangkat untuk memastikan perangkat target dapat ditemukan
# Bluetoothctl scan on

# Pasangkan dengan perangkat (ganti XX:XX:XX:XX:XX:XX dengan alamat perangkat Anda)
echo -e 'pair 98:D3:31:FB:5F:57\nconnect 98:D3:31:FB:5F:57\nquit' | bluetoothctl

# Koneksi ke perangkat
# Sudah ditangani dengan baris sebelumnya, tapi bisa diulangi jika diperlukan
# echo -e 'connect XX:XX:XX:XX:XX:XX\nquit' | bluetoothctl

echo "Bluetooth setup selesai."

