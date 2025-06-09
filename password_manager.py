import os, sqlite3, base64, hashlib, time, tkinter as tk
from tkinter.simpledialog import askstring
from tkinter.messagebox import showinfo, showwarning
from cryptography.fernet import Fernet

key_file, key_hash, db_file, db_enc, log_file = "secure_key.enc", "secure_key.enc.sha256", "data/passwords.db", "data/passwords.db.enc", "security.log"

def log_security(event):
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {event}\n")

def hide_file(f):
    try:
        import ctypes; ctypes.windll.kernel32.SetFileAttributesW(f, 0x02)
    except: pass

def file_sha256(f):
    h = hashlib.sha256()
    with open(f, "rb") as fi:
        [h.update(chunk) for chunk in iter(lambda: fi.read(4096), b"")]
    return h.hexdigest()

def prompt_master():
    root = tk.Tk(); root.withdraw()
    while True:
        p1 = askstring("Set master password", "Set new master password (min. 8 chars):", show="*")
        if not p1 or len(p1) < 8: showwarning("Error", "Password must be at least 8 characters."); continue
        p2 = askstring("Confirm password", "Confirm master password:", show="*")
        if p1 != p2: showwarning("Error", "Passwords do not match."); continue
        root.destroy(); return p1

if not os.path.exists(key_file):
    mp = prompt_master()
    mk = base64.urlsafe_b64encode(hashlib.sha256(mp.encode()).digest()[:32])
    ck = Fernet(mk); sk = Fernet.generate_key()
    with open(key_file, "wb") as f: f.write(ck.encrypt(sk))
    with open(key_hash, "w") as f: f.write(file_sha256(key_file))
    showinfo("Setup", "New key created. Remember your master password!")
    with open(key_file, "rb") as f: ek = f.read()
else:
    if not os.path.exists(key_hash) or open(key_hash).read().strip() != file_sha256(key_file):
        showwarning("Error", "Key file tampering detected! Exiting."); log_security("Key file tampering detected!"); exit(1)
    with open(key_file, "rb") as f: ek = f.read()

def get_cipher(pw):
    if not pw: return None
    mk = base64.urlsafe_b64encode(hashlib.sha256(pw.encode()).digest()[:32])
    try: return Fernet(Fernet(mk).decrypt(ek))
    except: log_security("Failed login attempt"); return None

def decrypt_db(c):
    if os.path.exists(db_enc):
        with open(db_enc, "rb") as f: ed = f.read()
        try: dd = c.decrypt(ed)
        except: showwarning("Error", "Cannot decrypt database. Check master password."); exit(1)
        with open(db_file, "wb") as f: f.write(dd)
    else: open(db_file, "wb").close()

def encrypt_db(c):
    if os.path.exists(db_file):
        try:
            with open(db_file, "rb") as f: d = f.read()
            ed = c.encrypt(d)
            if os.path.exists(db_enc): os.remove(db_enc)
            with open(db_enc, "wb") as f: f.write(ed)
            hide_file(db_enc); os.remove(db_file)
        except Exception as e:
            showwarning("Error", f"Cannot write encrypted DB: {e}")

os.makedirs("data", exist_ok=True)
root_pw = tk.Tk(); root_pw.withdraw()
mp = askstring("Master password", "Enter master password:", show="*")
cipher_for_db = get_cipher(mp)
if not cipher_for_db: showwarning("Error", "Invalid master password. Exiting."); exit(1)
decrypt_db(cipher_for_db)
hide_file(key_file); hide_file(key_hash)

conn = sqlite3.connect(db_file)
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS passwords (id INTEGER PRIMARY KEY, website TEXT, username TEXT, encrypted_password BLOB)")
conn.commit()

def save_encrypt():
    ci = get_cipher(e4.get())
    if not all([e1.get(), e2.get(), e3.get()]): return showwarning("Warning", "Fill all fields!")
    if not ci: return showwarning("Warning", "Enter correct master password!")
    c.execute("INSERT INTO passwords (website, username, encrypted_password) VALUES (?, ?, ?)",
              (e1.get(), e2.get(), ci.encrypt(e3.get().encode())))
    conn.commit(); update_list(); [e.delete(0, tk.END) for e in [e1, e2, e3]]

def generate_password():
    import string, random
    return ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(16))

def update_list():
    password_list.delete(0, tk.END)
    c.execute("SELECT website, username, encrypted_password FROM passwords")
    for row in c.fetchall(): password_list.insert(tk.END, f"{row[0]} | {row[1]} | [Encrypted]")

def show_decrypted():
    ci = get_cipher(e4.get())
    if not password_list.curselection(): return showwarning("Warning", "Select an entry!")
    if not ci: return showwarning("Warning", "Enter correct master password!")
    idx = password_list.curselection()[0]
    c.execute("SELECT website, username, encrypted_password FROM passwords")
    row = c.fetchall()[idx]
    try:
        decrypted = ci.decrypt(row[2]).decode('utf-8')
        showinfo("Decrypted", f"Website: {row[0]}\nUsername: {row[1]}\nPassword: {decrypted}")
    except: showwarning("Error", "Decryption failed. Check master password.")

root = tk.Tk(); root.title("Password Manager")
for i, txt in enumerate(["Website", "Username", "Password", "Master password"]):
    tk.Label(root, text=txt).grid(row=i, column=0)
e1, e2, e3, e4 = (tk.Entry(root) for _ in range(4)); e4.config(show="*")
for i, e in enumerate([e1, e2, e3, e4]): e.grid(row=i, column=1)
tk.Button(root, text="Save/Encrypt", command=save_encrypt).grid(row=4, column=0, columnspan=2)
tk.Button(root, text="Generate", command=lambda: e3.delete(0, tk.END) or e3.insert(0, generate_password())).grid(row=5, column=0, columnspan=2)
password_list = tk.Listbox(root, width=50); password_list.grid(row=6, column=0, columnspan=2)
tk.Button(root, text="Show", command=show_decrypted).grid(row=7, column=0, columnspan=2)
update_list()

def on_close():
    try:
        conn.commit(); conn.close()
    except: pass
    encrypt_db(cipher_for_db)
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()