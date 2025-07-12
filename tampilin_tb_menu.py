import mysql.connector

# Koneksi ke database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="program_kasir"
)

cursor = db.cursor()

# Tampilkan isi tabel user
cursor.execute("SELECT * FROM menu")

# Ambil semua data
results = cursor.fetchall()

# Tampilkan header kolom
print("{:<10} {:<20} {:<10}".format("id_menu", "nama_menu", "harga"))
print("-" * 40)

# Tampilkan setiap baris data
for row in results:
    print("{:<10} {:<20} {:<10}".format(row[0], row[1], row[2]))

# Tutup koneksi
db.close()
