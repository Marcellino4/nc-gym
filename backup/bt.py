import serial
import time

# Sesuaikan dengan device file pada sistem Anda
scanner_device = '/dev/rfcomm1'
mikro_device = '/dev/rfcomm0'

# Mengatur koneksi dengan PB008
scanner_ser = serial.Serial(scanner_device, baudrate=9600, timeout=1)

# Mengatur koneksi dengan Mikro2
mikro_ser = serial.Serial(mikro_device, baudrate=9600, timeout=1)

try:
    while True:
        if scanner_ser.in_waiting > 0:
            try:
                input_data = scanner_ser.readline().decode('utf-8').strip()
                if input_data:
                    # Data diterima dari PB008, lakukan sesuatu dengan data tersebut
                    print(f"Data diterima dari PB008: {input_data}")
                    mikro_ser.write(b'1')  # Mengirim perintah ke Mikro2
                    print("Perintah terkirim ke Mikro2.")
            except serial.SerialException as e:
                print(f"SerialException: {e}")
                break  # Atau handle exception sesuai kebutuhan Anda
            except UnicodeDecodeError as e:
                print(f"UnicodeDecodeError: {e}")
                # Handle jika ada error decoding, mungkin dengan continue atau log error

        # Tunda loop untuk sementara waktu agar tidak menggunakan CPU terlalu banyak
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Program dihentikan oleh pengguna.")

finally:
    scanner_ser.close()
    mikro_ser.close()
    print("Koneksi Serial ditutup.")

