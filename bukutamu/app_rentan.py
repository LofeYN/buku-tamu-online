"""
APLIKASI BUKU TAMU ONLINE — VERSI RENTAN (VULNERABLE)
=======================================================
PERINGATAN: File ini sengaja dibuat TIDAK AMAN untuk tujuan pengujian keamanan akademik.
JANGAN gunakan kode ini di lingkungan produksi!

Celah keamanan yang sengaja ditanamkan:
1. SQL Injection — pada login admin dan pencarian tamu
2. XSS (Cross-Site Scripting) — pada form buku tamu
3. IDOR (Insecure Direct Object Reference) — pada hapus data tamu
"""

from flask import Flask, request, render_template, redirect, url_for, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "rahasia123"  # CELAH: secret key lemah & hardcoded

DB_PATH = "bukutamu_rentan.db"

# ─── Setup Database ────────────────────────────────────────────────
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS tamu (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT,
            email TEXT,
            pesan TEXT,
            waktu DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS admin (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT
        )
    """)
    # Cek apakah admin sudah ada
    c.execute("SELECT COUNT(*) FROM admin")
    if c.fetchone()[0] == 0:
        c.execute("INSERT INTO admin (username, password) VALUES ('admin', 'admin123')")
    conn.commit()
    conn.close()

# ─── Halaman Utama: Form Buku Tamu ─────────────────────────────────
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        nama  = request.form.get("nama", "")
        email = request.form.get("email", "")
        pesan = request.form.get("pesan", "")

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        # CELAH SQL INJECTION: nilai langsung dimasukkan ke query
        query = f"INSERT INTO tamu (nama, email, pesan) VALUES ('{nama}', '{email}', '{pesan}')"
        c.execute(query)
        conn.commit()
        conn.close()
        return redirect(url_for("daftar_tamu"))

    return render_template("index_rentan.html")

# ─── Daftar Tamu: Tampil Tanpa Escaping (XSS) ──────────────────────
@app.route("/tamu")
def daftar_tamu():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, nama, email, pesan, waktu FROM tamu ORDER BY waktu DESC")
    tamu_list = c.fetchall()
    conn.close()
    # CELAH XSS: pesan ditampilkan dengan |safe — tidak di-escape
    return render_template("daftar_rentan.html", tamu_list=tamu_list)

# ─── Login Admin: SQL Injection ─────────────────────────────────────
@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        # CELAH SQL INJECTION: query langsung digabung dengan input user
        query = f"SELECT * FROM admin WHERE username='{username}' AND password='{password}'"
        print(f"[DEBUG] Query dijalankan: {query}")  # jangan lakukan ini di produksi!
        c.execute(query)
        admin = c.fetchone()
        conn.close()

        if admin:
            session["admin"] = username
            return redirect(url_for("admin_dashboard"))
        else:
            error = "Username atau password salah."

    return render_template("login_rentan.html", error=error)

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
    return render_template("dashboard_rentan.html", tamu_list=tamu_list)

# ─── Hapus Tamu: IDOR ────────────────────────────────────────────────
@app.route("/admin/hapus/<int:tamu_id>")
def hapus_tamu(tamu_id):
    # CELAH IDOR: tidak ada pengecekan apakah user adalah admin
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(f"DELETE FROM tamu WHERE id={tamu_id}")
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
    app.run(debug=True, port=5000)  # CELAH: debug=True di produksi
