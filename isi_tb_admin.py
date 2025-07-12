import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="program_kasir"
)

cursor = db.cursor()

# Perbaiki syntax SQL
sql = "INSERT INTO admin (nama_admin, password) VALUES (%s, %s)"
val = ("admin", 123)

cursor.execute(sql, val)

db.commit()

print("{} data ditambahkan".format(cursor.rowcount))
