import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="program_kasir"
)

cursor = db.cursor()
sql ="""CREATE TABLE menu (
    id_menu INT AUTO_INCREMENT PRIMARY KEY,
    nama_menu VARCHAR(255),
    harga INT(10)
)
"""
cursor.execute(sql)
print("Table user berhasil dibuat")

