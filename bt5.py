from evdev import InputDevice, categorize, ecodes
import requests
import serial
import threading
import datetime
import logging

# Konfigurasi logging
logging.basicConfig(filename='logfilepy.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Inisialisasi pemetaan key secara dinamis
key_mappings = {}
for name in dir(ecodes):
    if name.startswith("KEY_"):
        code = getattr(ecodes, name)
        # Menghapus prefix "KEY_" dari nama tombol dan filter out modifier keys
        if not name.endswith(("SHIFT", "CTRL", "ALT")):
            key_mappings[code] = name[4:]  # Potong "KEY_" dari nama

# Fungsi untuk menangani input dan logika untuk setiap keyboard
def handle_keyboard(device_path, status, serial_port):
    keyboard = InputDevice(device_path)
    logging.info(f"Listening on {device_path} (device name: {keyboard.name})")

    try:
        while True:
            current_time = datetime.datetime.now()
            id_gabung = ''  # Inisialisasi ulang variabel untuk menyimpan kata
            logging.info(f"\nReady for new input on {device_path}. Press ENTER to submit.")

            for event in keyboard.read_loop():
                if event.type == ecodes.EV_KEY:
                    data = categorize(event)
                    if data.keystate == data.key_down:
                        key_code = data.scancode
                        if key_code in key_mappings:
                            karakter = key_mappings[key_code]
                            if karakter == "ENTER":
                                break
                            else:
                                logging.info(karakter)  # Print the modified key name for demo purposes
                                id_gabung += karakter  # Concatenate the modified key name

            if id_gabung.strip():
                if serial_port == '/dev/rfcomm1':
                    # Mengirimkan payload ke API
                    payload = {'id': id_gabung.strip(), 'status': status}
                    api_url = "https://nc-gym.com/api/gate-log"

                    try:
                        response = requests.post(api_url, json=payload)
                        if response.text == 'true':
                            logging.info(f"API response true for {device_path} at {current_time}. Waiting for next input...\n")
                        else:
                            logging.info(f"API response was not true for {device_path} at {current_time}. Waiting for next input...\n")
                    except requests.exceptions.RequestException as e:
                        logging.error(f"HTTP Request error: {e}")
                else:
                    # Membuka port serial dan mengirimkan data
                    try:
                        ser = serial.Serial(serial_port)
                        ser.write(b'1')
                        ser.close()
                        logging.info(f"Serial data sent for {device_path} at {current_time}.")
                    except serial.SerialException as e:
                        logging.error(f"Serial port error: {e}")
    except KeyboardInterrupt:
        logging.info(f"\nExiting program for {device_path}.")

# Membuat dan menjalankan threads untuk kedua keyboard
# masuk
thread1 = threading.Thread(target=handle_keyboard, args=('/dev/input/event1', 'masuk', '/dev/rfcomm1'))
# keluar
thread2 = threading.Thread(target=handle_keyboard, args=('/dev/input/event2', 'keluar', '/dev/rfcomm0'))

thread1.start()
thread2.start()

thread1.join()
thread2.join()