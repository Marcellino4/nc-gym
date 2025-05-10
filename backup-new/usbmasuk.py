import serial
import requests
import asyncio
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

# Inisialisasi perangkat serial USB pada COM0
usb_port = '/dev/ttyUSB0'
usb_ser = serial.Serial(usb_port, baudrate=9600, timeout=1)

print("Listening for barcode scanner input. Press 'q' to exit.")

async def main():
    scanned_code = ""
    try:
        while True:
            if usb_ser.in_waiting > 0:
                byte = usb_ser.read(1)
                if byte.isdigit():
                    scanned_code += byte.decode('utf-8')
                elif byte == b'\n':
                    print(f"Scanned code: {scanned_code}")
                    api_url = "https://nc-gym.com/api/gate-log"
                    payload = {'id': scanned_code, 'status': 'masuk'}
                    try:
                        response = requests.post(api_url, json=payload)
                        response.raise_for_status()  # Raise an exception for HTTP errors
                        if response.text == 'true':
                            ser.write(b'1')
                            print("Berhasil")
                            await send_telegram_message(f"Access granted (Entry Gate) for ID: {scanned_code}")
                        else:
                            print("Gagal")
                            await send_telegram_message(f"!!!!!Access denied (Entry Gate) for ID: {scanned_code}")
                    except requests.exceptions.RequestException as e:
                        print(f"Failed to send request: {e}")
                        await send_telegram_message(f"!!!!!Access denied (Entry Gate) for ID: {scanned_code}. Error: {e}")
                    
                    scanned_code = ""  # Reset setelah mengirim data
    except KeyboardInterrupt:
        print("Program interrupted. Exiting...")
    finally:
        ser.close()
        usb_ser.close()

# Jalankan loop event asyncio
asyncio.run(main())
