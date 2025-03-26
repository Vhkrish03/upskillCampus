import os
import tkinter as tk
from tkinter import messagebox
import random
import string
import sqlite3
from cryptography.fernet import Fernet

# ------------------ KEY MANAGEMENT ------------------
key_file = "key.key"

if os.path.exists(key_file):
    with open(key_file, "rb") as file:
        key = file.read()
else:
    key = Fernet.generate_key()
    with open(key_file, "wb") as file:
        file.write(key)

cipher_suite = Fernet(key)

# ------------------ DATABASE SETUP ------------------
conn = sqlite3.connect("passwords.db")
cursor = conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS passwords (
    account TEXT PRIMARY KEY,
    password TEXT
)""")
conn.commit()
conn.close()

# ------------------ PASSWORD GENERATION ------------------
def generate_password():
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(12))

# ------------------ ENCRYPTION FUNCTIONS ------------------
def encrypt_password(password):
    return cipher_suite.encrypt(password.encode()).decode()

def decrypt_password(encrypted_password):
    return cipher_suite.decrypt(encrypted_password.encode()).decode()

# ------------------ GUI SETUP ------------------
root = tk.Tk()
root.title("Password Manager")
root.geometry("400x300")

# Labels and Entry Fields
tk.Label(root, text="Account Name:").pack()
account_entry = tk.Entry(root)
account_entry.pack()

tk.Label(root, text="Password:").pack()
password_entry = tk.Entry(root, show="*")  # Hides password input
password_entry.pack()

# ------------------ PASSWORD STORAGE ------------------
def store_password():
    account = account_entry.get()
    password = password_entry.get()

    if not account or not password:
        messagebox.showwarning("Warning", "All fields are required!")
        return

    encrypted_password = encrypt_password(password)

    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()
    
    try:
        cursor.execute("INSERT INTO passwords VALUES (?, ?)", (account, encrypted_password))
        conn.commit()
        messagebox.showinfo("Success", "Password Stored Successfully!")
    except sqlite3.IntegrityError:
        messagebox.showwarning("Error", "Account already exists!")
    
    conn.close()

# ------------------ PASSWORD RETRIEVAL ------------------
def retrieve_password():
    account = account_entry.get()

    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM passwords WHERE account=?", (account,))
    result = cursor.fetchone()
    conn.close()

    if result:
        decrypted_password = decrypt_password(result[0])
        messagebox.showinfo("Retrieved Password", f"Password for {account}: {decrypted_password}")
    else:
        messagebox.showwarning("Error", "Account not found!")

# Buttons
store_button = tk.Button(root, text="Store Password", command=store_password)
store_button.pack()

retrieve_button = tk.Button(root, text="Retrieve Password", command=retrieve_password)
retrieve_button.pack()

# ------------------ RUN APPLICATION ------------------
root.mainloop()
