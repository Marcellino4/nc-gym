import serial
import requests
from evdev import InputDevice, categorize, ecodes

# Inisialisasi port serial
serial_port = '/dev/rfcomm0'
ser = serial.Serial(serial_port, baudrate=9600, timeout=1)

# Fungsi untuk mendapatkan perangkat input yang sesuai (event1 atau event2)
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

scanned_code = ""

try:
    while True:
        for event in dev.read_loop():
            if event.type == ecodes.EV_KEY and event.value == 1:  # Hanya saat tombol ditekan
                if event.code in key_codes:
                    scanned_code += key_codes[event.code]
                elif event.code == ecodes.KEY_ENTER:
                    print(f"Scanned code: {scanned_code}")
                    
                    response = requests.post('URL_API', data={'scanned_code': scanned_code})
                    
                    if response.status_code == 200 and response.json().get('value') == 1:
                        ser.write(b'1')
                        print("Berhasil mengirim sinyal ke relay.")
                    
                    scanned_code = ""  # Reset setelah mengirim data
                    break

except KeyboardInterrupt:
    print("Program interrupted. Exiting...")
    ser.close()
