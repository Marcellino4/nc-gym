import serial

serial_port = '/dev/rfcomm1'  # Pastikan path ini sesuai dengan perangkat yang terhubung

try:
    ser = serial.Serial(serial_port)  # Membuka koneksi serial
    ser.write(b'1')  # Menulis data ke port serial
    ser.close()  # Menutup koneksi serial
    print("Data telah dikirim.")
except serial.SerialException as e:
    print(f"Terjadi kesalahan saat membuka atau menggunakan port serial: {e}")
except Exception as e:
    print(f"Terjadi kesalahan: {e}")