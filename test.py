import serial
import requests
import asyncio
from evdev import InputDevice, categorize, ecodes
from telegram import Bot

# Inisialisasi port serial
serial_port = '/dev/rfcomm1'
ser = serial.Serial(serial_port, baudrate=9600, timeout=1)

TELEGRAM_BOT_TOKEN = '7243366231:AAGxqP4QhS_cPv1-JHfN5NbFrT1wk7Y-TBk'
CHAT_ID = '-1002204066531'

# Inisialisasi bot telegram
bot = Bot(token=TELEGRAM_BOT_TOKEN)

# Fungsi untuk mengirim pesan ke Telegram
async def send_telegram_message(message):
    try:
        await bot.send_message(chat_id=CHAT_ID, text=message)
    except Exception as e:
        print(f"Failed to send message: {e}")

# Fungsi untuk mendapatkan perangkat input yang sesuai (event2)
def find_input_device():
    try:
        dev2 = InputDevice('/dev/input/event2')
        return dev2
    except FileNotFoundError:
        raise Exception("No suitable input device found at /dev/input/event2.")

# Inisialisasi perangkat input
dev = find_input_device()

print("Listening for keyboard events. Press 'q' to exit.")

# Daftar key code untuk angka 0-9
key_codes = {
    ecodes.KEY_0: '0',
    ecodes.KEY_1: '1',
    ecodes.KEY_2: '2',
    ecodes.KEY_3: '3',
    ecodes.KEY_4: '4',
    ecodes.KEY_5: '5',
    ecodes.KEY_6: '6',
    ecodes.KEY_7: '7',
    ecodes.KEY_8: '8',
    ecodes.KEY_9: '9'
}

async def main():
    scanned_code = ""
    try:
        while True:
            for event in dev.read_loop():
                if event.type == ecodes.EV_KEY and event.value == 1:  # Hanya saat tombol ditekan
                    if event.code in key_codes:
                        scanned_code += key_codes[event.code]
                    elif event.code == ecodes.KEY_ENTER:
                        print(f"Scanned code: {scanned_code}")
                        api_url = "https://nc-gym.com/api/gate-log"
                        payload = {'id': scanned_code, 'status': 'masuk'}
                        response = requests.post(api_url, json=payload)

                        if response.text == 'true':
                            ser.write(b'1')
                            print("Berhasil")
                            await send_telegram_message(f"Access granted (Entry Gate) for ID: {scanned_code}")
                        else:
                            print("Gagal")
                            await send_telegram_message(f"!!!!!Access denied (Entry Gate) for ID: {scanned_code}")
                        
                        scanned_code = ""  # Reset setelah mengirim data
                        break
    except KeyboardInterrupt:
        print("Program interrupted. Exiting...")
    finally:
        ser.close()
        dev.close()

# Jalankan loop event asyncio
asyncio.run(main())
