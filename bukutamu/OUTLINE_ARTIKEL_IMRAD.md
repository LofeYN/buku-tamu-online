# OUTLINE ARTIKEL ILMIAH FORMAT IMRAD
## Standar Jurnal SINTA 3–5 | 6–10 Halaman

---

**JUDUL (pilih salah satu):**
- "Analisis Kerentanan SQL Injection, Cross-Site Scripting, dan IDOR pada Aplikasi Web Buku Tamu Berbasis Flask serta Implementasi Mitigasinya"
- "Pengujian Keamanan Aplikasi Web Menggunakan Metode OWASP Top 10: Studi Kasus Sistem Buku Tamu Online"

**Penulis:** [Nama Kamu], [Nama Kampus], [Email]

---

## I. INTRODUCTION (Pendahuluan) — ~1 halaman

**Paragraf 1 — Latar belakang umum:**
- Pertumbuhan aplikasi web dan risiko keamanan siber
- Data statistik serangan siber di Indonesia (cari dari BSSN atau Kominfo)
- Kutip 2–3 jurnal tentang tren serangan web

**Paragraf 2 — Masalah spesifik:**
- SQL Injection dan XSS masuk OWASP Top 10 secara konsisten
- Banyak aplikasi web masih rentan karena kurangnya validasi input
- Referensi: studi kasus serangan SQL Injection di aplikasi nyata

**Paragraf 3 — Tujuan penelitian:**
- Membangun prototipe aplikasi web yang sengaja rentan (vulnerable by design)
- Menguji tiga jenis celah: SQL Injection, XSS, dan IDOR
- Mengimplementasikan mitigasi dan memverifikasi efektivitasnya

**Research Gap (wajib ada):**
- Penelitian sebelumnya banyak yang hanya menguji tanpa membangun aplikasi sendiri
- Penelitian ini membangun dua versi aplikasi (rentan vs aman) untuk perbandingan langsung

**Tujuan & Manfaat:**
> "Penelitian ini bertujuan untuk menganalisis kerentanan SQL Injection, XSS, dan IDOR pada aplikasi web berbasis Flask, serta mengimplementasikan mitigasi dengan pendekatan parameterized query dan output encoding."

---

## II. LITERATURE REVIEW / TINJAUAN PUSTAKA — ~1–1.5 halaman

*(Masukkan di bagian Introduction atau buat sub-section tersendiri, tergantung template jurnal)*

**A. Keamanan Aplikasi Web**
- Definisi dan konsep dasar keamanan aplikasi web
- OWASP Top 10 — apa itu dan mengapa penting
- Referensi: [cari jurnal SINTA tentang OWASP]

**B. SQL Injection**
- Definisi SQL Injection
- Cara kerja serangan: input tidak tersanitasi dieksekusi sebagai query SQL
- Dampak: bypass autentikasi, pencurian data, penghapusan database
- Referensi: min. 2 jurnal

**C. Cross-Site Scripting (XSS)**
- Definisi XSS (Reflected, Stored, DOM-based)
- Cara kerja: skrip berbahaya dieksekusi di browser korban
- Dampak: pencurian cookie, session hijacking, defacement
- Referensi: min. 2 jurnal

**D. IDOR (Insecure Direct Object Reference)**
- Definisi IDOR
- Cara kerja: akses objek langsung via ID tanpa verifikasi otorisasi
- Referensi: min. 1 jurnal

**E. Flask dan SQLite**
- Penjelasan singkat framework Flask
- SQLite sebagai database ringan untuk prototyping

---

## III. METHODOLOGY (Metode Penelitian) — ~1.5 halaman

**A. Desain Penelitian**
- Jenis: penelitian eksperimental (pengujian keamanan)
- Pendekatan: black-box testing dan white-box testing
- Diagram alur penelitian (buat flowchart sederhana)

**B. Lingkungan Pengujian**
| Komponen | Spesifikasi |
|----------|-------------|
| OS | Windows 10 / Ubuntu 20.04 |
| Bahasa | Python 3.x |
| Framework | Flask 2.x |
| Database | SQLite 3 |
| Tools Pengujian | Browser DevTools, Burp Suite Free |

**C. Tahapan Penelitian**
1. **Perancangan sistem** — desain arsitektur aplikasi buku tamu
2. **Pembangunan versi rentan** — implementasi tanpa proteksi
3. **Pengujian keamanan** — eksekusi skenario serangan
4. **Implementasi mitigasi** — perbaikan celah yang ditemukan
5. **Verifikasi** — pengujian ulang setelah mitigasi

**D. Skenario Pengujian**

| No | Jenis Serangan | Input Uji | Indikator Keberhasilan |
|----|---------------|-----------|------------------------|
| 1 | SQL Injection | `' OR '1'='1' --` | Berhasil login tanpa password |
| 2 | XSS Stored | `<script>alert('XSS')</script>` | Popup alert muncul di browser |
| 3 | IDOR | Akses URL `/admin/hapus/1` tanpa login | Data berhasil dihapus |

**E. Teknik Mitigasi yang Diterapkan**
| Celah | Mitigasi |
|-------|---------|
| SQL Injection | Parameterized Query (Prepared Statement) |
| XSS | HTML Auto-Escaping oleh Jinja2 (tanpa `\|safe`) |
| IDOR | Pengecekan sesi login sebelum akses resource |

---

## IV. RESULTS (Hasil) — ~2 halaman

**A. Hasil Pengujian Versi Rentan**

**4.1 SQL Injection**
- Deskripsi: dengan input `' OR '1'='1' --` pada field username, sistem berhasil diakses tanpa password yang valid
- Query yang dieksekusi: `SELECT * FROM admin WHERE username='' OR '1'='1' --' AND password='...'`
- Lampirkan: screenshot halaman dashboard yang terbuka
- Dampak: attacker dapat bypass autentikasi dan mengakses semua data tamu

**4.2 XSS (Cross-Site Scripting)**
- Deskripsi: payload `<script>alert('XSS Berhasil!')</script>` yang dimasukkan pada field pesan berhasil dieksekusi oleh browser
- Lampirkan: screenshot popup alert yang muncul
- Dampak: pada skenario nyata, skrip dapat digunakan untuk mencuri cookie sesi pengguna lain

**4.3 IDOR**
- Deskripsi: URL `/admin/hapus/1` dapat diakses langsung tanpa proses login
- Lampirkan: screenshot sebelum dan sesudah data dihapus tanpa autentikasi
- Dampak: siapapun dapat menghapus data tamu secara massal

**B. Hasil Verifikasi Setelah Mitigasi**

| Jenis Serangan | Sebelum Mitigasi | Setelah Mitigasi |
|---------------|-----------------|-----------------|
| SQL Injection | ✅ Berhasil | ❌ Gagal — "Username/password salah" |
| XSS Stored | ✅ Berhasil | ❌ Gagal — skrip ditampilkan sebagai teks |
| IDOR | ✅ Berhasil | ❌ Gagal — "Akses ditolak, 403" |

---

## V. DISCUSSION (Pembahasan) — ~1.5 halaman

**A. Analisis SQL Injection**
- Mengapa parameterized query efektif: parameter dipisahkan dari query, tidak bisa dimanipulasi
- Bandingkan dengan penelitian sebelumnya
- Rekomendasi tambahan: gunakan ORM (SQLAlchemy) untuk keamanan lebih kuat

**B. Analisis XSS**
- Mengapa Jinja2 auto-escaping efektif: karakter `<`, `>`, `"` diubah menjadi HTML entities
- Pentingnya tidak menggunakan `|safe` kecuali data sudah disanitasi
- Rekomendasi tambahan: implementasi Content Security Policy (CSP)

**C. Analisis IDOR**
- Pengecekan sesi sudah cukup untuk kasus ini
- Rekomendasi tambahan: gunakan UUID alih-alih ID integer sekuensial

**D. Keterbatasan Penelitian**
- Pengujian dilakukan di lingkungan lokal, bukan production
- Tidak menggunakan tools otomatis seperti OWASP ZAP (bisa ditambahkan)
- Password belum di-hash dengan bcrypt (rekomendasi untuk pengembangan lanjut)

---

## VI. CONCLUSION (Kesimpulan) — ~0.5 halaman

1. Aplikasi web buku tamu berbasis Flask yang dibangun terbukti rentan terhadap tiga jenis serangan: SQL Injection, XSS, dan IDOR
2. Mitigasi menggunakan parameterized query, HTML auto-escaping, dan pengecekan sesi terbukti efektif mencegah ketiga jenis serangan tersebut
3. Pengembang aplikasi web wajib menerapkan praktik keamanan sejak tahap pengembangan (security by design)

**Saran pengembangan:**
- Implementasi hash password dengan bcrypt
- Penambahan rate limiting untuk mencegah brute force
- Pengujian lanjutan menggunakan OWASP ZAP

---

## DAFTAR PUSTAKA (min. 8–15 referensi, 10 tahun terakhir)

Format APA / IEEE (sesuaikan dengan template jurnal target).

**Kata kunci untuk cari di Google Scholar / Portal Garuda:**
- "SQL Injection web application" site:garuda.kemdikbud.go.id
- "XSS Cross Site Scripting Flask Python" jurnal
- "OWASP keamanan aplikasi web" SINTA
- "kerentanan aplikasi web Indonesia"
- "parameterized query SQL injection mitigation"

**Jurnal SINTA yang bisa dituju:**
- Jurnal Ilmiah Teknik Informatika (SINTA 4)
- Jurnal Sistem Informasi dan Sains Teknologi (SINTA 4)
- Jurnal RESTI (SINTA 2) — jika tulisan sangat baik
- Jurnal Pseudocode (SINTA 4)
- Seminar Nasional APTISI (prosiding, lebih mudah)

---

*Catatan: Tulis artikel dalam bahasa yang mengalir natural, hindari copy-paste langsung dari AI. Gunakan outline ini sebagai kerangka, isi dengan kata-katamu sendiri berdasarkan hasil pengujian nyata.*
