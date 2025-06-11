# Encrypted-Password-Manager
Secure password manager with AES encryption, master password protection, and secure password generation.


# Encrypted Password Manager

A simple and secure password manager in Python with full database encryption.

## How does it work?

1. **First run**
   - The program asks you to set a master password (minimum 8 characters, double confirmation).
   - A random encryption key is generated and encrypted with your master password.
   - The key file is saved as `secure_key.enc` and protected with a SHA256 checksum (`secure_key.enc.sha256`).

2. **Login**
   - On every launch, you enter your master password.
   - If the password is correct, the database is decrypted only for the session.

3. **Adding and storing passwords**
   - Fill in: Website, Username, Password.
   - Enter your master password.
   - Click "Save/Encrypt" – the password is encrypted and stored in the database.

4. **Viewing saved passwords**
   - Select an entry from the list.
   - Enter your master password.
   - Click "Show" to decrypt and view the password.

5. **Strong password generation**
   - Click "Generate" to automatically create a strong password.

6. **Security features**
   - All passwords are encrypted with a key only you know.
   - The key file is encrypted with your master password and protected by a checksum.
   - Every failed login attempt is logged in `security.log`.
   - Key and database files are hidden on Windows.

## Requirements

- Python 3.8+
- `cryptography` library
- Tkinter (included with Python)

## Installation

```bash
pip install cryptography
```

## Running

```bash
python password_manager.py
```

## Security recommendations

- Never share your `secure_key.enc` or database files.
- Set a strong master password and never forget it – without it, you cannot decrypt your passwords!
- Regularly back up your files.
- If you forget your master password or delete `secure_key.enc`, your passwords are unrecoverable!

---

**This project is for portfolio purposes and demonstrates practical user data security.**


# Encrypted Password Manager (PL)

Prosty i bezpieczny menedżer haseł w Pythonie z pełnym szyfrowaniem bazy danych.

## Jak to działa?

1. **Pierwsze uruchomienie**
   - Program poprosi Cię o ustawienie hasła głównego (minimum 8 znaków, dwukrotne potwierdzenie).
   - Na podstawie tego hasła zostanie wygenerowany i zaszyfrowany klucz do szyfrowania Twoich haseł.
   - Plik klucza zostanie zapisany jako `secure_key.enc` i zabezpieczony sumą kontrolną (`secure_key.enc.sha256`).

2. **Logowanie**
   - Przy każdym uruchomieniu podajesz swoje hasło główne.
   - Jeśli hasło jest poprawne, baza zostaje odszyfrowana tylko na czas działania programu.

3. **Dodawanie i przechowywanie haseł**
   - Wypełnij pola: Website, Username, Password.
   - Wpisz swoje hasło główne.
   - Kliknij "Zapisz/Zaszyfruj" – hasło zostanie zaszyfrowane i zapisane w bazie.

4. **Podgląd zapisanych haseł**
   - Wybierz wpis z listy.
   - Wpisz swoje hasło główne.
   - Kliknij "Pokaż", aby odszyfrować i zobaczyć hasło.

5. **Generowanie silnych haseł**
   - Kliknij "Generuj", aby automatycznie wygenerować silne hasło.

6. **Bezpieczeństwo**
   - Wszystkie hasła są szyfrowane kluczem, który znasz tylko Ty.
   - Plik klucza jest zaszyfrowany Twoim hasłem głównym i chroniony sumą kontrolną.
   - Każda nieudana próba logowania jest zapisywana w pliku `security.log`.
   - Pliki klucza i bazy są ukrywane na Windows.

## Wymagania

- Python 3.8+
- Biblioteka `cryptography`
- Tkinter (standardowo w Pythonie)

## Instalacja

```bash
pip install cryptography
```

## Uruchomienie

```bash
python password_manager.py
```

## Zalecenia bezpieczeństwa

- Nie udostępniaj pliku `secure_key.enc` ani bazy danych osobom trzecim.
- Ustaw silne hasło główne i nie zapomnij go – bez niego nie odszyfrujesz swoich haseł!
- Regularnie twórz kopie zapasowe plików.
- Jeśli zapomnisz hasła głównego lub usuniesz plik `secure_key.enc`, nie odzyskasz swoich haseł!

---

**Projekt do portfolio – pokazuje praktyczne podejście do bezpieczeństwa danych użytkownika.**
