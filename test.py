import serial
import datetime
import os

# Fungsi untuk menulis log ke file
def write_log(message):
    with open('log_gate.log', 'a') as f:
        f.write(f"{datetime.datetime.now()} - {message}\n")

# Memeriksa dan mengatur izin file log_gate.log
def check_file_permissions(file_path):
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            pass
    os.chmod(file_path, 0o666)

# Path ke port serial yang terhubung
serial_port = '/dev/rfcomm1'  # Pastikan path ini sesuai dengan perangkat yang terhubung

# Memastikan file log_gate.log memiliki izin yang tepat
check_file_permissions('log_gate.log')

try:
    # Membuka koneksi serial
    ser = serial.Serial(serial_port)
    ser.write(b'1')  # Menulis data ke port serial
    write_log("Data telah dikirim.")
except serial.SerialException as e:
    write_log(f"Terjadi kesalahan saat membuka atau menggunakan port serial: {e}")
except Exception as e:
    write_log(f"Terjadi kesalahan: {e}")
finally:
    # Pastikan koneksi serial ditutup dengan benar
    if 'ser' in locals() and ser.is_open:
        ser.close()
        write_log("Koneksi serial telah ditutup.")