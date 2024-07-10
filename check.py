import subprocess
import requests
import time

# Daftar MAC address dengan deskripsi
devices = {
    "98:D3:31:FB:5F:57": "rfcomm1",
    "98:D3:31:FB:5E:5C": "rfcomm0",
    "DC:0D:30:93:BF:8C": "PB Masuk",
    "DC:0D:30:93:BF:11": "PB Keluar"
}

# Telegram bot token dan chat ID
TELEGRAM_BOT_TOKEN = '7243366231:AAGxqP4QhS_cPv1-JHfN5NbFrT1wk7Y-TBk'
CHAT_ID = "-1002204066531"

def check_connections():
    try:
        output = subprocess.check_output("hcitool con", shell=True).decode()
        print(output)  # Untuk debugging, bisa dihapus nanti
        connected_mac_addresses = [line.split()[2] for line in output.split('\n') if 'ACL' in line]
        for mac, description in devices.items():
            if mac not in connected_mac_addresses:
                send_telegram_message(f"Device {description} (MAC address {mac}) tidak terhubung!")
    except subprocess.CalledProcessError as e:
        print(f"Error saat menjalankan hcitool: {e}")

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": message
    }
    response = requests.post(url, data=data)
    if response.status_code != 200:
        print(f"Error mengirim pesan ke Telegram: {response.text}")

if __name__ == "__main__":
    while True:
        check_connections()
        time.sleep(300)  # Tunggu 5 menit (300 detik) sebelum pengecekan berikutnya