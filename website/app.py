from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime
import mysql.connector

app = Flask(__name__)
app.secret_key = 'nusadine_secret_key'

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="program_kasir"
    )

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM admin WHERE nama_admin=%s AND password=%s", (username, password))
        admin = cursor.fetchone()
        conn.close()

        if admin:
            session['user'] = username
            return redirect(url_for('menu'))
        else:
            flash('Login gagal! Username atau password salah.')
            return redirect(url_for('login'))
    return render_template('login.html')


@app.route('/menu', methods=['GET', 'POST'])
def menu():
    if 'user' not in session:
        return redirect(url_for('login'))

    menu_list = [
        ("Nasi Goreng", 15000),
        ("Mie Ayam", 12000),
        ("Es Teh", 5000),
        ("Es Jeruk", 6000),
        ("Ayam Geprek", 20000),
        ("Kwetiau Goreng", 15000),
        ("Soto Lamongan", 20000),
        ("Es Pisang Ijo", 10000),
    ]

    if 'pesanan' not in session:
        session['pesanan'] = []
        session['total'] = 0
        session['meja'] = 1

    if request.method == 'POST':
        idx = int(request.form['menu_index'])
        jumlah = int(request.form['jumlah'])

        nama, harga = menu_list[idx]
        total_harga = harga * jumlah
        meja = session['meja']

        # simpan ke database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO pesanan (nama_user, nama_menu, nomor_meja, harga) VALUES (%s, %s, %s, %s)",
            (session['user'], nama, meja, total_harga)
        )
        conn.commit()
        conn.close()

        # update session
        session['pesanan'].append(f"{nama} x{jumlah} (Meja {meja}) = Rp{total_harga:,}")
        session['total'] += total_harga
        session['meja'] += 1

        flash(f"{nama} berhasil ditambahkan ke pesanan!")

    return render_template('menu.html', username=session['user'], menu_list=menu_list, pesanan=session['pesanan'], total=session['total'])

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)
