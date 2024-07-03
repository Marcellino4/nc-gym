import serial
from inputs import get_key

# Inisialisasi port serial
serial_port = '/dev/rfcomm0'
ser = serial.Serial(serial_port, baudrate=9600, timeout=1)

print("Listening for keyboard events. Press 'q' to exit.")

# Daftar key code untuk angka 0-9
key_codes = {
    'KEY_0': b'0',
    'KEY_1': b'1',
    'KEY_2': b'2',
    'KEY_3': b'3',
    'KEY_4': b'4',
    'KEY_5': b'5',
    'KEY_6': b'6',
    'KEY_7': b'7',
    'KEY_8': b'8',
    'KEY_9': b'9'
}

try:
    while True:
        events = get_key()
        for event in events:
            if event.ev_type == 'Key' and event.ev_state == 1:  # Hanya saat tombol ditekan
                print(f"Event: {event.ev_type} - {event.ev_code} - {event.ev_state}")

                if event.ev_code in key_codes:
                    ser.write(key_codes[event.ev_code])
                    print(f"Sent '{key_codes[event.ev_code].decode()}' to serial port")

                # Keluar jika tombol 'q' ditekan
                if event.ev_code == 'KEY_Q':
                    print("Exiting...")
                    ser.close()
                    exit()

except KeyboardInterrupt:
    print("Program interrupted. Exiting...")
    ser.close()