import serial
from evdev import InputDevice, list_devices, categorize, ecodes

# Inisialisasi port serial
serial_port = '/dev/rfcomm1'
ser = serial.Serial(serial_port, baudrate=9600, timeout=1)

# Fungsi untuk mendapatkan perangkat input yang sesuai
def find_input_device():
    devices = [InputDevice(fn) for fn in list_devices()]
    for device in devices:
        print(f"Found device: {device.name} at {device.fn}")
        # Asumsikan perangkat yang cocok adalah PB008
        if 'PB008' in device.name:
            return device
    raise Exception("No suitable input device found.")

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
                    ser.write(b'1')
                    scanned_code = ""  # Reset setelah mengirim data
                    break

except KeyboardInterrupt:
    print("Program interrupted. Exiting...")
    ser.close()