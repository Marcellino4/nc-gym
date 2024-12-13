from evdev import InputDevice, categorize, ecodes
import serial

# Buat pemetaan sederhana dari beberapa kode tombol ke karakter
key_mappings = {
    ecodes.KEY_1: '1',
    ecodes.KEY_ENTER: '\n',  # Menggunakan newline untuk ENTER
}

# Ganti dengan path ke perangkat input keyboard yang sesuai
keyboard_path = '/dev/input/event0'
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
                            ser = serial.Serial('/dev/rfcomm0')
                            ser.write(b'1')  # Kirim byte '1'
                            ser.close()
                        except serial.SerialException as e:
                            print(f"Serial port error: {e}")
except KeyboardInterrupt:
    print("\nExiting program.")
