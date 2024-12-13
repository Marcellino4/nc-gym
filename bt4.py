from evdev import InputDevice, categorize, ecodes
import requests
import serial
import threading

key_mappings = {
    ecodes.KEY_1: '1',
    ecodes.KEY_2: '2',
    ecodes.KEY_3: '3',
    ecodes.KEY_4: '4',
    ecodes.KEY_5: '5',
    # Tambahkan lebih banyak pemetaan sesuai kebutuhan
    ecodes.KEY_ENTER: '\n',  # Digunakan untuk menandai akhir input
}

# Fungsi untuk menangani input dan logika untuk setiap keyboard
def handle_keyboard(device_path, status, serial_port):
    keyboard = InputDevice(device_path)
    print(f"Listening on {device_path} (device name: {keyboard.name})")

    try:
        while True:
            id_gabung = ''  # Inisialisasi ulang variabel untuk menyimpan kata
            print(f"\nReady for new input on {device_path}. Press ENTER to submit.")

            for event in keyboard.read_loop():
                if event.type == ecodes.EV_KEY:
                    data = categorize(event)
                    if data.keystate == data.key_down:
                        key_code = data.scancode
                        if key_code in key_mappings:
                            karakter = key_mappings[key_code]
                            print(karakter, end='', flush=True)
                            if karakter == '\n':
                                break
                            id_gabung += karakter

            if id_gabung.strip():
                payload = {'id': id_gabung.strip(), 'status': status}
                api_url = "http://192.168.100.47:8000/api/gate-log"

                try:
                    response = requests.post(api_url, json=payload)
                    if response.text == 'true':
                        try:
                            ser = serial.Serial(serial_port)
                            ser.write(b'1')
                            ser.close()
                            print(f"Action successful on {device_path}. Waiting for next input...")
                        except serial.SerialException as e:
                            print(f"Serial port error: {e}")
                    else:
                        print(f"API response was not true on {device_path}. Waiting for next input...")
                except requests.exceptions.RequestException as e:
                    print(f"HTTP Request error: {e}")
    except KeyboardInterrupt:
        print(f"\nExiting program for {device_path}.")

# Membuat dan menjalankan threads untuk kedua keyboard
thread1 = threading.Thread(target=handle_keyboard, args=('/dev/input/event2', 'masuk', '/dev/rfcomm0'))
thread2 = threading.Thread(target=handle_keyboard, args=('/dev/input/event3', 'keluar', '/dev/rfcomm1'))

thread1.start()
thread2.start()

thread1.join()
thread2.join()
