import sqlite3
import tkinter as tk
from tkinter.messagebox import showinfo, showwarning
from cryptography.fernet import Fernet
import os
import base64
import hashlib

# Generowanie i zapisanie zaszyfrowanego klucza
key_file = "secure_key.enc"
encrypted_key = b""  # Domyślna wartość
if not os.path.exists(key_file):
    master_password = "dexsterpasswordmenager"
    master_key = base64.urlsafe_b64encode(hashlib.sha256(master_password.encode('utf-8')).digest()[:32])
    cipher_master = Fernet(master_key)
    secret_key = Fernet.generate_key()
    with open(key_file, "wb") as f:
        f.write(cipher_master.encrypt(secret_key))
    showinfo("Setup", "New key created. Use 'dexsterpasswordmenager' as Private Key.")
else:
    with open(key_file, "rb") as f:
        encrypted_key = f.read()

# Funkcja do odszyfrowania klucza z hasłem
def get_cipher(password):
    if not password:
        return None
    master_key = base64.urlsafe_b64encode(hashlib.sha256(password.encode('utf-8')).digest()[:32])
    try:
        cipher_master = Fernet(master_key)
        secret_key = cipher_master.decrypt(encrypted_key)
        return Fernet(secret_key)
    except Exception as e:
        showwarning("Error", f"Invalid password: {str(e)}. Ensure 'dexsterpasswordmenager' is correct.")
        return None

# Inicjalizacja bazy danych
conn = sqlite3.connect('data/passwords.db')
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS passwords (id INTEGER PRIMARY KEY, website TEXT, username TEXT, encrypted_password TEXT)")
conn.commit()

# Funkcje
def save_encrypt():
    cipher_instance = get_cipher(e4.get())
    if not all([e1.get(), e2.get(), e3.get()]) or not cipher_instance:
        return showwarning("Warning", "Fill all fields or enter correct key!")
    encrypted = cipher_instance.encrypt(e3.get().encode('utf-8'))
    c.execute("INSERT INTO passwords (website, username, encrypted_password) VALUES (?, ?, ?)", (e1.get(), e2.get(), encrypted))
    conn.commit()
    update_list()
    [e.delete(0, tk.END) for e in [e1, e2, e3]]

def generate_password():
    import string, random
    return ''.join(random.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(12))

def update_list():
    password_list.delete(0, tk.END)
    c.execute("SELECT website, username, encrypted_password FROM passwords")
    for row in c.fetchall():
        password_list.insert(tk.END, f"{row[0]} | {row[1]} | [Encrypted]")

def show_decrypted():
    cipher_instance = get_cipher(e4.get())
    if not password_list.curselection() or not cipher_instance:
        return showwarning("Warning", "Select a password or enter correct key!")
    idx = password_list.curselection()[0]
    c.execute("SELECT website, username, encrypted_password FROM passwords")
    row = c.fetchall()[idx]
    try:
        decrypted = cipher_instance.decrypt(row[2]).decode('utf-8')
        showinfo("Decrypted", f"Website: {row[0]}\nUsername: {row[1]}\nPassword: {decrypted}")
    except Exception as e:
        showwarning("Error", f"Decryption failed: {str(e)}")

# GUI
root = tk.Tk()
root.title("Password Manager")

tk.Label(root, text="Website").grid(row=0, column=0)
tk.Label(root, text="Username").grid(row=1, column=0)
tk.Label(root, text="Password").grid(row=2, column=0)
tk.Label(root, text="Private Key").grid(row=3, column=0)

e1, e2, e3, e4 = tk.Entry(root), tk.Entry(root), tk.Entry(root), tk.Entry(root, show="*")
for i, e in enumerate([e1, e2, e3, e4], 0): e.grid(row=i, column=1)

tk.Button(root, text="Save/Encrypt", command=save_encrypt).grid(row=4, column=0, columnspan=2)
tk.Button(root, text="Generate", command=lambda: e3.delete(0, tk.END) or e3.insert(0, generate_password())).grid(row=5, column=0, columnspan=2)
password_list = tk.Listbox(root, width=50)
password_list.grid(row=6, column=0, columnspan=2)
tk.Button(root, text="Show", command=show_decrypted).grid(row=7, column=0, columnspan=2)

update_list()
root.mainloop()
conn.close()