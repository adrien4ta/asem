import serial
import time

# Konfigurasi Port (Sesuaikan dengan komputer Anda)
PORT = '/dev/ttyUSB0' # Ubah jika pakai Windows (misal: 'COM3')
BAUD = 9600

try:
    print(f"Menghubungkan ke {PORT}...")
    ser = serial.Serial(PORT, BAUD, timeout=2)
    
    # 1. Tunggu Arduino Restart (Wajib!)
    print("Menunggu Arduino siap (2 detik)...")
    time.sleep(2)
    
    # Bersihkan buffer sisa (sampah data saat booting)
    ser.reset_input_buffer()

    # 2. Kirim Perintah "GET"
    print("Mengirim perintah cek jadwal...")
    ser.write(b"GET\n") # Jangan lupa \n

    # 3. Baca Balasan
    # Arduino mungkin butuh waktu milidetik untuk memproses, kita coba baca loop
    start_time = time.time()
    data_found = False

    while (time.time() - start_time) < 3: # Timeout 3 detik
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            
            # Filter hanya pesan yang diawali "JADWAL:"
            if line.startswith("JADWAL:"):
                # Format: JADWAL:17,30,5,15
                isi_data = line.split(":")[1] # Ambil bagian angkanya saja
                parts = isi_data.split(",")
                
                if len(parts) == 4:
                    on_j, on_m, off_j, off_m = parts
                    
                    print("\n" + "="*30)
                    print("   DATA JADWAL DARI EEPROM")
                    print("="*30)
                    print(f"LAMPU NYALA (ON)  : {on_j.zfill(2)}:{on_m.zfill(2)}")
                    print(f"LAMPU MATI  (OFF) : {off_j.zfill(2)}:{off_m.zfill(2)}")
                    print("="*30 + "\n")
                    data_found = True
                    break
            else:
                # Debug: Tampilkan data lain yang mungkin masuk (misal data monitoring)
                # print(f"Data lain diterima: {line}") 
                pass

    if not data_found:
        print("Gagal: Tidak menerima balasan jadwal dari Arduino.")

    ser.close()

except serial.SerialException:
    print("Error: Port tidak ditemukan atau sedang digunakan.")
except Exception as e:
    print(f"Error tidak terduga: {e}")
