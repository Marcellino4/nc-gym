from evdev import InputDevice, categorize, ecodes
import serial

# Buat pemetaan sederhana dari beberapa kode tombol ke karakter
key_mappings = {
    ecodes.KEY_1: '1',
    ecodes.KEY_ENTER: '\n',  # Menggunakan newline untuk ENTER
}

# Ganti dengan path ke perangkat input keyboard yang sesuai
keyboard_path = '/dev/input/event2'
keyboard = InputDevice(keyboard_path)

print(f"Listening on {keyboard_path} (device name: {keyboard.name})")

try:
    # Loop untuk membaca input dari keyboard
    for event in keyboard.read_loop():
        if event.type == ecodes.EV_KEY:
            # Dapatkan data event
            data = categorize(event)
            # Cek apakah tombol ditekan (bukan dilepaskan atau autorepeat)
            if data.keystate == data.key_down:
                key_code = data.scancode
                if key_code in key_mappings:
                    # Cetak karakter yang sesuai dengan kode tombol
                    print(key_mappings[key_code], end='', flush=True)
                    # Khusus untuk tombol '1', kirim '1' melalui serial port
                    if key_mappings[key_code] == '1':
                        try:
                            ser = serial.Serial('/dev/rfcomm1')
                            ser.write(b'1')  # Kirim byte '1'
                            ser.close()
                        except serial.SerialException as e:
                            print(f"Serial port error: {e}")
except KeyboardInterrupt:
    print("\nExiting program.")
from evdev import InputDevice, categorize, ecodes
import serial

# Inisialisasi pemetaan kosong
key_mappings = {}

# Tambahkan angka 0-9
for code in range(ecodes.KEY_1, ecodes.KEY_9 + 1):
    key_mappings[code] = str(code - ecodes.KEY_1 + 1)
key_mappings[ecodes.KEY_0] = '0'  # KEY_0 biasanya mengikuti KEY_9

# Tambahkan huruf A-Z
for code in range(ecodes.KEY_A, ecodes.KEY_Z + 1):
    key_mappings[code] = chr(code - ecodes.KEY_A + ord('A'))

# Tambahkan tombol ENTER
key_mappings[ecodes.KEY_ENTER] = '\n'  # Menggunakan newline untuk ENTER

# Ganti dengan path ke perangkat input keyboard yang sesuai
keyboard_path = '/dev/input/event2'
keyboard = InputDevice(keyboard_path)

print(f"Listening on {keyboard_path} (device name: {keyboard.name})")

try:
    # Loop untuk membaca input dari keyboard
    for event in keyboard.read_loop():
        if event.type == ecodes.EV_KEY:
            # Dapatkan data event
            data = categorize(event)
            # Cek apakah tombol ditekan (bukan dilepaskan atau autorepeat)
            if data.keystate == data.key_down:
                key_code = data.scancode
                if key_code in key_mappings:
                    character = key_mappings[key_code]
                    # Cetak karakter yang sesuai dengan kode tombol
                    print(character, end='', flush=True)
                    # Khusus untuk karakter '1', kirim '1' melalui serial port
                    if character == '1':
                        try:
                            ser = serial.Serial('/dev/rfcomm0')
                            ser.write(b'1')  # Kirim byte '1'
                            ser.close()
                        except serial.SerialException as e:
                            print(f"Serial port error: {e}")
except KeyboardInterrupt:
    print("\nExiting program.")
