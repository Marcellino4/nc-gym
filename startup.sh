#!/bin/bash

# Jalankan bluetoothctl di terminal baru
gnome-terminal -- bash -c "bluetoothctl && connect DC:0D:30:93:BF:11; exec bash"

# Tunggu beberapa detik agar bluetoothctl selesai
sleep 10

# Jalankan rfcomm connect di terminal baru
gnome-terminal -- bash -c "sudo rfcomm connect rfcomm0 98:D3:31:FB:5E:5C; exec bash"

sleep 10

gnome-terminal -- bash -c "sudo rfcomm connect rfcomm1 98:D3:31:FB:5F:57; exec bash"

# Tunggu beberapa detik agar rfcomm selesai
sleep 10

# Jalankan skrip Python di terminal baru
gnome-terminal -- bash -c "cd /var/www/nc-gym && python test.py; exec bash"

sleep 10

gnome-terminal -- bash -c "cd /var/www/nc-gym && python test2.py; exec bash"