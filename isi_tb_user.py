import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="program_kasir"
)

cursor = db.cursor()

# Perbaiki syntax SQL
sql = "INSERT INTO user (nama_user, nomor_meja) VALUES (%s, %s)"
val = ("fina", 1)

cursor.execute(sql, val)

db.commit()

print("{} data ditambahkan".format(cursor.rowcount))
