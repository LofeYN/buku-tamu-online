"""
APLIKASI BUKU TAMU ONLINE — VERSI AMAN (DEPLOY-READY)
======================================================
Perbaikan untuk deployment:
1. DB_PATH menggunakan path absolut berbasis lokasi file
2. init_db() dipanggil otomatis saat startup
3. Entry point untuk gunicorn: app (object Flask)
4. PORT dari environment variable (wajib untuk Render/Railway/Heroku)
"""

from flask import Flask, request, render_template, redirect, url_for, session
import sqlite3
import os
import secrets

app = Flask(__name__)
# SECRET_KEY wajib di-set sebagai environment variable di platform deploy
app.secret_key = os.environ.get("SECRET_KEY", secrets.token_hex(32))

# Gunakan path absolut supaya DB ditemukan di mana pun app dijalankan
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "bukutamu.db")


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
        # Password admin bisa diubah via env var ADMIN_PASSWORD
        admin_password = os.environ.get("ADMIN_PASSWORD", "Admin@2024!")
        c.execute("INSERT INTO admin (username, password) VALUES (?, ?)", ("admin", admin_password))
    conn.commit()
    conn.close()


# Inisialisasi DB saat modul pertama kali dimuat (termasuk saat gunicorn load)
init_db()


# ─── Halaman Utama: Form Buku Tamu ─────────────────────────────────
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        nama  = request.form.get("nama", "").strip()
        email = request.form.get("email", "").strip()
        pesan = request.form.get("pesan", "").strip()

        if not nama or not email or not pesan:
            return render_template("index_aman.html", error="Semua field wajib diisi.")

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("INSERT INTO tamu (nama, email, pesan) VALUES (?, ?, ?)", (nama, email, pesan))
        conn.commit()
        conn.close()
        return redirect(url_for("daftar_tamu"))

    return render_template("index_aman.html")


# ─── Daftar Tamu ───────────────────────────────────────────────────
@app.route("/tamu")
def daftar_tamu():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, nama, email, pesan, waktu FROM tamu ORDER BY waktu DESC")
    tamu_list = c.fetchall()
    conn.close()
    return render_template("daftar_aman.html", tamu_list=tamu_list)


# ─── Login Admin ────────────────────────────────────────────────────
@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
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
    if "admin" not in session:
        return redirect(url_for("admin_login"))

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, nama, email, pesan, waktu FROM tamu ORDER BY waktu DESC")
    tamu_list = c.fetchall()
    conn.close()
    return render_template("dashboard_aman.html", tamu_list=tamu_list)


# ─── Hapus Tamu ──────────────────────────────────────────────────────
@app.route("/admin/hapus/<int:tamu_id>")
def hapus_tamu(tamu_id):
    if "admin" not in session:
        return "Akses ditolak. Silakan login sebagai admin.", 403

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
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
    # Ambil PORT dari env variable (wajib di Render/Railway/Heroku)
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)
