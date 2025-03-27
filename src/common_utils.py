# Get Display Scaling Factor
from header import *

user32 = ctypes.windll.user32
GetDpiForWindow = user32.GetDpiForWindow
GetDpiForWindow.restype = ctypes.c_int
GetDpiForWindow.argtypes = [ctypes.c_void_p]

def get_scaling_factor():
    hwnd = ctypes.windll.user32.GetForegroundWindow()
    dpi = GetDpiForWindow(hwnd)
    return dpi / 96.0  # 96 DPI is the base scale

def scaled_value(value):
    return int(value * get_scaling_factor())

def is_valid_numeric_input(input_str):
    try:
        float(input_str)
        return True
    except ValueError:
        return False

def donothing(event=None):
    print("Button is disabled")
    pass

def get_project_names():
    try:
        with open("projects.txt", "r") as file:
            projects = [line.strip() for line in file if line.strip()]
        return projects
    except FileNotFoundError:
        return []


from cryptography.fernet import Fernet
import pandas as pd
import os


# Generate a key and save it securely (Do this only once)
def generate_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)


# Load the saved key
def load_key():
    return open("secret.key", "rb").read()


# Encrypt the file
def encrypt_file(filename):
    key = load_key()
    cipher = Fernet(key)

    with open(filename, "rb") as file:
        file_data = file.read()

    encrypted_data = cipher.encrypt(file_data)

    with open(filename + ".enc", "wb") as file:
        file.write(encrypted_data)

    os.remove(filename)  # Delete the original file


# Decrypt the file
def decrypt_file(encrypted_filename, output_filename):
    key = load_key()
    cipher = Fernet(key)

    with open(encrypted_filename, "rb") as file:
        encrypted_data = file.read()

    decrypted_data = cipher.decrypt(encrypted_data)

    with open(output_filename, "wb") as file:
        file.write(decrypted_data)

    os.remove(encrypted_filename)  # Delete the encrypted file

"""
# Example Usage
# generate_key()  # Run this once to create the key
encrypt_file("database.xlsx")  # Encrypt
decrypt_file("database.xlsx.enc", "database.xlsx")  # Decrypt
"""