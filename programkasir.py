import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime
import mysql.connector


class Database:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="program_kasir"
        )
        self.cursor = self.conn.cursor()

    def check_login(self, username, password):
        sql = "SELECT * FROM admin WHERE nama_admin = %s AND password = %s"
        self.cursor.execute(sql, (username, password))
        result = self.cursor.fetchone()
        return True if result else False

    def insert_pesanan(self, nama_user, nama_menu, nomor_meja, harga):
        sql = "INSERT INTO pesanan (nama_user, nama_menu, nomor_meja, harga) VALUES (%s, %s, %s, %s)"
        self.cursor.execute(sql, (nama_user, nama_menu, nomor_meja, harga))
        self.conn.commit()


class LoginPage:
    def __init__(self, master):
        self.master = master
        self.master.title("Login - NusaDine")
        self.master.geometry("400x250")
        self.master.configure(bg="#f0f0f0")

        self.db = Database()
        self.create_widgets()

    def create_widgets(self):
        title = tk.Label(
            self.master,
            text="🔒 Login NusaDine 🔒",
            font=("Helvetica", 18, "bold"),
            bg="#f0f0f0"
        )
        title.pack(pady=20)

        frame = tk.Frame(self.master, bg="#ffffff", padx=20, pady=20, bd=2, relief=tk.RIDGE)
        frame.pack(pady=10)

        tk.Label(frame, text="Username:", bg="#ffffff", font=("Helvetica", 12)).grid(row=0, column=0, sticky="w")
        self.username_entry = ttk.Entry(frame)
        self.username_entry.grid(row=1, column=0, pady=5)

        tk.Label(frame, text="Password:", bg="#ffffff", font=("Helvetica", 12)).grid(row=2, column=0, sticky="w")
        self.password_entry = ttk.Entry(frame, show="*")
        self.password_entry.grid(row=3, column=0, pady=5)

        login_button = ttk.Button(frame, text="Login", command=self.check_login)
        login_button.grid(row=4, column=0, pady=10)

    def check_login(self):
        nama_admin = self.username_entry.get()
        password = self.password_entry.get()

        is_valid = self.db.check_login(nama_admin, password)

        if is_valid:
            messagebox.showinfo("Login Berhasil", f"Selamat datang, {nama_admin}!")
            self.master.destroy()
            root = tk.Tk()
            PesananGUI(root, nama_admin, self.db) # untuk memanggil menu setelah login
            root.mainloop()
        else:
            messagebox.showerror("Login Gagal", "Username atau password salah!")


class PesananGUI:
    def __init__(self, master, nama_user, db):
        self.master = master
        self.nama_user = nama_user
        self.db = db

        self.master.title("🍽️ NusaDine - Pemesanan Menu 🍽️")
        self.master.geometry("700x600")
        self.master.configure(bg="#f0f0f0")

        self.menu_list = [
            ("Nasi Goreng", 15000),
            ("Mie Ayam", 12000),
            ("Es Teh", 5000),
            ("Es Jeruk", 6000),
            ("Ayam Geprek", 20000),
            ("Kwetiau Goreng", 15000),
            ("Soto Lamongan", 20000),
            ("Es Pisang Ijo", 10000),
        ]

        self.total_semua = 0
        self.struk = ""
        self.nomor_pesanan = 1
        self.nomor_meja = 1  # Meja dimulai dari 1
        self.menu_dipesan = []

        self.create_widgets()

    def create_widgets(self):
        title = tk.Label(
            self.master,
            text="🌟 Selamat Datang di NusaDine 🌟",
            font=("Helvetica", 20, "bold"),
            bg="#f0f0f0",
            fg="#333"
        )
        title.pack(pady=10)

        frame = tk.Frame(self.master, bg="#ffffff", padx=20, pady=20, bd=2, relief=tk.RIDGE)
        frame.pack(pady=10)

        label_menu = tk.Label(frame, text="Menu:", font=("Helvetica", 12, "bold"), bg="#ffffff")
        label_menu.grid(row=0, column=0, sticky="w")

        self.listbox = tk.Listbox(frame, height=10, width=40, font=("Helvetica", 10))
        for idx, (nama, harga) in enumerate(self.menu_list, start=1):
            self.listbox.insert(tk.END, f"{idx}. {nama} - Rp{harga:,}")
        self.listbox.grid(row=1, column=0, pady=5)

        label_jumlah = tk.Label(frame, text="Jumlah:", font=("Helvetica", 12, "bold"), bg="#ffffff")
        label_jumlah.grid(row=2, column=0, sticky="w", pady=(10, 0))

        self.jumlah_entry = ttk.Entry(frame, width=10)
        self.jumlah_entry.grid(row=3, column=0, sticky="w")

        self.pesan_button = ttk.Button(frame, text="Pesan Menu", command=self.pesan_menu)
        self.pesan_button.grid(row=4, column=0, pady=10, sticky="w")

        self.cetak_button = ttk.Button(frame, text="Cetak Struk", command=self.cetak_struk)
        self.cetak_button.grid(row=5, column=0, pady=5, sticky="w")

        self.cek_button = ttk.Button(frame, text="Cek Menu Dipesan", command=self.cek_menu_dipesan)
        self.cek_button.grid(row=6, column=0, pady=5, sticky="w")

        self.text_area = tk.Text(self.master, height=15, width=70, font=("Courier New", 10))
        self.text_area.pack(pady=10)

    def pesan_menu(self):
        selected = self.listbox.curselection()
        if not selected:
            messagebox.showwarning("Peringatan", "Pilih menu terlebih dahulu!")
            return

        jumlah = self.jumlah_entry.get()
        if not jumlah.isdigit() or int(jumlah) <= 0:
            messagebox.showerror("Error", "Jumlah tidak valid!")
            return

        idx = selected[0]
        nama, harga = self.menu_list[idx]
        total = harga * int(jumlah)

        self.total_semua += total
        self.struk += f"{self.nomor_pesanan}. {nama} x{jumlah} (Meja {self.nomor_meja}) = Rp{total:,}\n"
        self.menu_dipesan.append(nama)
        self.nomor_pesanan += 1

        # Insert ke database, kirim nomor meja yang sesuai
        self.db.insert_pesanan(self.nama_user, nama, self.nomor_meja, total)

        messagebox.showinfo("Berhasil!", f"{nama} berhasil ditambahkan ke pesanan! (Meja {self.nomor_meja})")

        # Nomor meja bertambah setiap pesanan baru
        self.nomor_meja += 1

    def cetak_struk(self):
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, "=== Struk Pembelian ===\n\n")
        self.text_area.insert(tk.END, f"{self.struk}\n")
        self.text_area.insert(tk.END, f"Total Bayar: Rp{self.total_semua:,}\n")
        self.text_area.insert(tk.END, "\n=== Terima Kasih ===")

    def cek_menu_dipesan(self):
        menu_dicari = simpledialog.askstring("Cek Menu", "Masukkan nama menu yang ingin dicek:")
        if not menu_dicari:
            return

        if menu_dicari.isdigit():
            messagebox.showerror("Error", "Inputan harus berupa huruf!")
            return

        if menu_dicari in self.menu_dipesan:
            messagebox.showinfo("Cek Menu", f"'{menu_dicari}' ADA di daftar pesanan.")
        else:
            messagebox.showinfo("Cek Menu", f"'{menu_dicari}' BELUM dipesan.")


if __name__ == "__main__":
    root = tk.Tk()
    LoginPage(root)
    root.mainloop()
