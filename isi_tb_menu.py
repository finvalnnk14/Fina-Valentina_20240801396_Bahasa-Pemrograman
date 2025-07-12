import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="program_kasir"
)

cursor = db.cursor()

# Perbaiki syntax SQL
sql = "INSERT INTO menu (nama_menu, harga) VALUES (%s, %s)"
val = [
    ("Nasi Goreng", 15000),
    ("Mie Ayam", 12000),
    ("Es Teh", 5000),
    ("Es Jeruk", 6000),
    ("Ayam Geprek", 20000),
    ("Kwetiau Goreng", 15000),
    ("Soto Lamongan", 20000),
    ("Es Pisang Ijo", 10000),
]


cursor.executemany(sql, val)

db.commit()

print("{} data ditambahkan".format(cursor.rowcount))
