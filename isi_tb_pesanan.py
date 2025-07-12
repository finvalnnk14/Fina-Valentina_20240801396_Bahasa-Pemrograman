import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="program_kasir"
)

cursor = db.cursor()

sql = "INSERT INTO pesanan (nama_user, nama_menu, nomor_meja, harga) VALUES (%s, %s, %s, %s)"
val = ("Fina", "Nasi Goreng", 1, 15000)

cursor.execute(sql, val)
db.commit()

print("{} data ditambahkan".format(cursor.rowcount))
