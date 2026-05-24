"""
APLIKASI BUKU TAMU ONLINE — VERSI AMAN (SECURE)
================================================
Versi ini menerapkan mitigasi terhadap semua celah yang ada di versi rentan:
1. Parameterized Query     → mencegah SQL Injection
2. HTML Escaping (Jinja2)  → mencegah XSS
3. Pengecekan Sesi Admin   → mencegah IDOR
4. Secret key aman         → dari environment variable
"""

from flask import Flask, request, render_template, redirect, url_for, session
import sqlite3
import os
import secrets

app = Flask(__name__)
# MITIGASI: gunakan secret key acak dan kuat
app.secret_key = os.environ.get("SECRET_KEY", secrets.token_hex(32))

DB_PATH = "bukutamu_aman.db"

# ─── Setup Database ────────────────────────────────────────────────
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS tamu (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT NOT NULL,
            email TEXT NOT NULL,
            pesan TEXT NOT NULL,
            waktu DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS admin (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    """)
    c.execute("SELECT COUNT(*) FROM admin")
    if c.fetchone()[0] == 0:
        # CATATAN: di produksi, gunakan bcrypt untuk hash password
        c.execute("INSERT INTO admin (username, password) VALUES (?, ?)", ("admin", "Admin@2024!"))
    conn.commit()
    conn.close()

# ─── Halaman Utama: Form Buku Tamu ─────────────────────────────────
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        nama  = request.form.get("nama", "").strip()
        email = request.form.get("email", "").strip()
        pesan = request.form.get("pesan", "").strip()

        # Validasi input
        if not nama or not email or not pesan:
            return render_template("index_aman.html", error="Semua field wajib diisi.")

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        # MITIGASI SQL INJECTION: gunakan parameterized query (placeholder ?)
        c.execute("INSERT INTO tamu (nama, email, pesan) VALUES (?, ?, ?)", (nama, email, pesan))
        conn.commit()
        conn.close()
        return redirect(url_for("daftar_tamu"))

    return render_template("index_aman.html")

# ─── Daftar Tamu: XSS dicegah oleh Jinja2 auto-escaping ───────────
@app.route("/tamu")
def daftar_tamu():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, nama, email, pesan, waktu FROM tamu ORDER BY waktu DESC")
    tamu_list = c.fetchall()
    conn.close()
    # MITIGASI XSS: render_template Jinja2 secara default melakukan HTML escape
    # JANGAN gunakan |safe kecuali benar-benar diperlukan dan data sudah disanitasi
    return render_template("daftar_aman.html", tamu_list=tamu_list)

# ─── Login Admin: Parameterized Query ───────────────────────────────
@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        # MITIGASI SQL INJECTION: parameterized query
        c.execute("SELECT * FROM admin WHERE username=? AND password=?", (username, password))
        admin = c.fetchone()
        conn.close()

        if admin:
            session["admin"] = username
            return redirect(url_for("admin_dashboard"))
        else:
            error = "Username atau password salah."

    return render_template("login_aman.html", error=error)

# ─── Dashboard Admin ─────────────────────────────────────────────────
@app.route("/admin/dashboard")
def admin_dashboard():
    # MITIGASI: selalu cek sesi sebelum akses halaman admin
    if "admin" not in session:
        return redirect(url_for("admin_login"))

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, nama, email, pesan, waktu FROM tamu ORDER BY waktu DESC")
    tamu_list = c.fetchall()
    conn.close()
    return render_template("dashboard_aman.html", tamu_list=tamu_list)

# ─── Hapus Tamu: Cek Sesi Dulu (Mencegah IDOR) ──────────────────────
@app.route("/admin/hapus/<int:tamu_id>")
def hapus_tamu(tamu_id):
    # MITIGASI IDOR: hanya admin yang login yang boleh hapus
    if "admin" not in session:
        return "Akses ditolak. Silakan login sebagai admin.", 403

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # MITIGASI SQL INJECTION: parameterized query
    c.execute("DELETE FROM tamu WHERE id=?", (tamu_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("admin_dashboard"))

# ─── Logout ──────────────────────────────────────────────────────────
@app.route("/admin/logout")
def logout():
    session.pop("admin", None)
    return redirect(url_for("admin_login"))

if __name__ == "__main__":
    init_db()
    # MITIGASI: debug=False di produksi
    app.run(debug=False, port=5001)
