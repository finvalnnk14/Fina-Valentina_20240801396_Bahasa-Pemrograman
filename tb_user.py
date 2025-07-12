import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="program_kasir"
)

cursor = db.cursor()
sql ="""CREATE TABLE user (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    nama_user VARCHAR(255),
    nomor_meja INT(2)
)
"""
cursor.execute(sql)
print("Table user berhasil dibuat")

