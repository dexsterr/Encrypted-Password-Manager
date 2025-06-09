import sqlite3
import tkinter as tk
from tkinter.messagebox import showinfo, showwarning
from cryptography.fernet import Fernet
import os
import base64

# Generowanie i zapisywanie klucza do pliku
key_file = "private.key"
if not os.path.exists(key_file):
    key = Fernet.generate_key()
    with open(key_file, "wb") as f:
        f.write(key)
else:
    with open(key_file, "rb") as f:
        key = f.read()

cipher = Fernet(key)

# Inicjalizacja bazy danych
conn = sqlite3.connect('data/passwords.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS passwords 
             (id INTEGER PRIMARY KEY, website TEXT, username TEXT, encrypted_password TEXT)''')
conn.commit()

# Funkcja dodawania hasła
def add_password(website, username, password):
    encrypted_pass = cipher.encrypt(password.encode())
    c.execute("INSERT INTO passwords (website, username, encrypted_password) VALUES (?, ?, ?)",
              (website, username, encrypted_pass))
    conn.commit()
    update_list()

# Funkcja generowania hasła
def generate_password(length=12):
    import random
    import string
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

# Funkcja aktualizacji listy haseł
def update_list():
    password_list.delete(0, tk.END)
    c.execute("SELECT website, username, encrypted_password FROM passwords")
    for row in c.fetchall():
        password_list.insert(tk.END, f"{row[0]} | {row[1]} | [Encrypted]")

# Funkcja odszyfrowywania
def decrypt_password(encrypted_pass, provided_key=None):
    try:
        temp_cipher = Fernet(provided_key.encode() if provided_key else key)
        return temp_cipher.decrypt(encrypted_pass).decode()
    except Exception as e:
        return f"Error: {str(e)}"

# Interfejs GUI
root = tk.Tk()
root.title("Encrypted Password Manager")

# Pola wprowadzania
tk.Label(root, text="Website").grid(row=0, column=0)
tk.Label(root, text="Username").grid(row=1, column=0)
tk.Label(root, text="Password").grid(row=2, column=0)
tk.Label(root, text="Private Key (optional)").grid(row=3, column=0)

website_entry = tk.Entry(root)
username_entry = tk.Entry(root)
password_entry = tk.Entry(root)
key_entry = tk.Entry(root, show="*")

website_entry.grid(row=0, column=1)
username_entry.grid(row=1, column=1)
password_entry.grid(row=2, column=1)
key_entry.grid(row=3, column=1)

# Przyciski
def save_password():
    if not website_entry.get() or not username_entry.get() or not password_entry.get():
        showwarning("Warning", "All fields are required!")
        return
    add_password(website_entry.get(), username_entry.get(), password_entry.get())
    website_entry.delete(0, tk.END)
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)

tk.Button(root, text="Save", command=save_password).grid(row=4, column=0, columnspan=2)

def generate_and_set_password():
    password_entry.delete(0, tk.END)  # Wyczyść pole przed wstawieniem nowego hasła
    password_entry.insert(0, generate_password())

tk.Button(root, text="Generate Password", command=generate_and_set_password).grid(row=5, column=0, columnspan=2)

# Lista haseł
password_list = tk.Listbox(root, width=50)
password_list.grid(row=6, column=0, columnspan=2)

update_list()

# Odszyfrowywanie wybranego hasła
def show_decrypted():
    selected = password_list.curselection()
    if not selected:
        showwarning("Warning", "Select a password to decrypt!")
        return
    index = selected[0]
    c.execute("SELECT website, username, encrypted_password FROM passwords")
    row = c.fetchall()[index]
    website, username, encrypted_pass = row
    provided_key = key_entry.get() or None
    decrypted = decrypt_password(encrypted_pass, provided_key)
    showinfo("Decrypted Password", f"Website: {website}\nUsername: {username}\nPassword: {decrypted}")

tk.Button(root, text="Show Decrypted", command=show_decrypted).grid(row=7, column=0, columnspan=2)

root.mainloop()

# Zamknięcie połączenia
conn.close()