# 📖 Buku Tamu Online — Panduan Lengkap

## Struktur Proyek
```
bukutamu/
├── app_rentan.py          ← Versi rentan (untuk pengujian)
├── app_aman.py            ← Versi aman (setelah mitigasi)
├── templates/
│   ├── index_rentan.html
│   ├── daftar_rentan.html
│   ├── login_rentan.html
│   ├── dashboard_rentan.html
│   ├── index_aman.html
│   ├── daftar_aman.html
│   ├── login_aman.html
│   └── dashboard_aman.html
└── README.md
```

---

## Cara Install & Jalankan

### 1. Install Python (jika belum)
Download di: https://python.org/downloads
Centang ✅ "Add Python to PATH" saat instalasi.

### 2. Install Flask
Buka terminal/command prompt, ketik:
```bash
pip install flask
```

### 3. Jalankan Versi Rentan
```bash
cd bukutamu
python app_rentan.py
```
Buka browser: http://localhost:5000

### 4. Jalankan Versi Aman (terminal berbeda)
```bash
python app_aman.py
```
Buka browser: http://localhost:5001

---

## 🔴 Skenario Pengujian (Versi Rentan — port 5000)

### Pengujian 1: SQL Injection pada Login Admin
1. Buka http://localhost:5000/admin/login
2. Isi Username: `' OR '1'='1' --`
3. Isi Password: `apapun`
4. Klik Masuk
5. **Hasil:** Berhasil masuk tanpa password yang benar ✓ (CELAH TERBUKTI)
6. **Screenshot** halaman dashboard yang terbuka

### Pengujian 2: XSS pada Form Buku Tamu
1. Buka http://localhost:5000
2. Isi Nama: `Tamu XSS`
3. Isi Email: `test@test.com`
4. Isi Pesan: `<script>alert('XSS Berhasil!')</script>`
5. Klik Kirim, lalu buka halaman Daftar Tamu
6. **Hasil:** Muncul popup alert di browser ✓ (CELAH TERBUKTI)
7. **Screenshot** popup alert tersebut

### Pengujian 3: IDOR (Insecure Direct Object Reference)
1. TANPA login admin, buka URL langsung: http://localhost:5000/admin/hapus/1
2. **Hasil:** Data tamu dengan ID 1 berhasil dihapus tanpa autentikasi ✓ (CELAH TERBUKTI)

---

## 🟢 Verifikasi Mitigasi (Versi Aman — port 5001)

### Verifikasi 1: SQL Injection Gagal
1. Buka http://localhost:5001/admin/login
2. Isi Username: `' OR '1'='1' --`
3. Isi Password: `apapun`
4. **Hasil:** "Username atau password salah." — SQL Injection GAGAL ✓

### Verifikasi 2: XSS Gagal
1. Buka http://localhost:5001
2. Isi Pesan: `<script>alert('XSS')</script>`
3. Lihat daftar tamu
4. **Hasil:** Teks ditampilkan apa adanya, bukan dieksekusi ✓

### Verifikasi 3: IDOR Gagal
1. TANPA login, buka: http://localhost:5001/admin/hapus/1
2. **Hasil:** "Akses ditolak. Silakan login sebagai admin." ✓

---

## Kredensial Default
| Versi   | Username | Password    |
|---------|----------|-------------|
| Rentan  | admin    | admin123    |
| Aman    | admin    | Admin@2024! |
