import serial
from evdev import InputDevice, list_devices, categorize, ecodes

# Inisialisasi port serial
serial_port = '/dev/rfcomm0'
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
    ecodes.KEY_0: b'0',
    ecodes.KEY_1: b'1',
    ecodes.KEY_2: b'2',
    ecodes.KEY_3: b'3',
    ecodes.KEY_4: b'4',
    ecodes.KEY_5: b'5',
    ecodes.KEY_6: b'6',
    ecodes.KEY_7: b'7',
    ecodes.KEY_8: b'8',
    ecodes.KEY_9: b'9'
}

try:
    for event in dev.read_loop():
        if event.type == ecodes.EV_KEY and event.value == 1:  # Hanya saat tombol ditekan
            print(f"Event: {event.type} - {event.code} - {event.value}")

            if event.code in key_codes:
                ser.write(key_codes[event.code])
                print(f"Sent '{key_codes[event.code].decode()}' to serial port")

            # Keluar jika tombol 'q' ditekan
            if event.code == ecodes.KEY_Q:
                print("Exiting...")
                ser.close()
                break

except KeyboardInterrupt:
    print("Program interrupted. Exiting...")
    ser.close()