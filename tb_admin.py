import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="program_kasir"
)

cursor = db.cursor()
sql ="""CREATE TABLE admin (
    nama_admin VARCHAR(255),
    password VARCHAR(10)
)
"""
cursor.execute(sql)
print("Table user berhasil dibuat")

