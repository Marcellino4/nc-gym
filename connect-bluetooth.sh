
sudo zerotier-cli join 56374ac9a46a7313

#!/bin/bash
# Controller bluetooth aktif dan mengatur default-agent
bluetoothctl power on
bluetoothctl agent on
bluetoothctl default-agent

# Menandai device sebagai trusted
#bluetoothctl trust DC:0D:30:93:BF:11 #PB008
#bluetoothctl trust DC:0D:30:93:BF:8C #PB008
#bluetoothctl trust 98:D3:31:FB:5F:57 #Mikro2
#bluetoothctl trust 98:D3:31:FB:5E:5C #Mikro3


# Melakukan binding terhadap rfcomm0 dan rfcomm1
#rfcomm bind rfcomm0 98:D3:31:FB:5E:5C 1
#rfcomm bind rfcomm1 98:D3:31:FB:5F:57 1
#sleep 5

chmod +x /var/www/bt5.py

#Mengkoneksikan bluetooth dengan perangkat 
timeout 10 bluetoothctl connect DC:0D:30:93:BF:8C &> /var/www/logfile.log
sleep 10
timeout 10 bluetoothctl connect DC:0D:30:93:BF:11 &> /var/www/logfile.log
sleep 10

connect_rfcomm() {
    local rfcomm_device=$1
    local bt_address=$2
    while true; do
        echo "Mencoba terhubung dengan rfcomm device $rfhost_device ke $bt_address..."
        sudo rfcomm connect "$rfcomm_device" "$bt_address" 1 &> /var/www/logfile.log
        echo "Terhubung dengan rfcomm device $rfcomm_device ke $bt_address. Menjaga koneksi..."
        sleep 10 # Berikan jeda antara setiap percobaan untuk menghindari beban berlebihan
    done
}

connect_rfcomm rfcomm1 98:D3:31:FB:5F:57 &
connect_rfcomm rfcomm0 98:D3:31:FB:5E:5C &

# Menjalankan perintah python
if ! timeout 20 python /var/www/bt5.py; then
    echo "Python script encountered an error"
fi &> /var/www/logfilepy.log
