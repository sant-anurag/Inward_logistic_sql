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
    """
    Retrieves a list of project names from the 'projects' table in the database.

    Returns:
    list: A list of project names.
    """

    # Define the database connection details
    db_config = serverdb_config

    try:
        # Create a connection to the MySQL database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Use the existing logistic database
        cursor.execute("USE logistic")

        # Query to select all project names from the 'projects' table
        query = "SELECT project_name FROM projects"
        cursor.execute(query)

        # Fetch all project names from the query result
        projects = [row[0] for row in cursor.fetchall()]

        # Close the cursor and connection objects
        cursor.close()
        conn.close()

        return projects
    except mysql.connector.Error as err:
        # Show an error messagebox if the connection to the server fails
        root = tk.Tk()
        root.withdraw()  # Hides the root window
        response = messagebox.askokcancel("Connection Error",
                                          "Could not connect to server. Please check your connection.")
        if response:
            root.destroy()
            sys.exit(1)  # Exit the application with a non-zero status code
        print(f"Error: {err}")
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