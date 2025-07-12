import mysql.connector

# Koneksi ke database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="program_kasir"
)

cursor = db.cursor()

# Tampilkan isi tabel admin
cursor.execute("SELECT * FROM admin")

# Ambil semua data
results = cursor.fetchall()

# Tampilkan header kolom
print("{:<20} {:<20}".format("nama_admin", "password"))
print("-" * 40)

# Tampilkan setiap baris data
for row in results:
    print("{:<20} {:<20}".format(row[0], row[1]))

# Tutup koneksi
db.close()
