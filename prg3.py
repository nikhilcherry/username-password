import tkinter as tk
from tkinter import ttk
import csv
import pyodbc
import pandas as pd

def submit_action():

    user = username_text.get()
    pwd = password_text.get()

    csv_path = r"C:\Users\Nikhi\OneDrive\Desktop\python\password.csv"
    with open(csv_path, "r") as f:
        reader = csv.reader(f)
        rows = list(reader)   # Convert reader to a list so we can index

    # Example: Get the 3rd row (index 2)
    for row in rows:
        if user == row[0] and pwd == row[1]:
            label3 = tk.Label(main_window, text="login successful")
            label3.grid(row=5, column=150, padx=0, pady=10)
            break
    else:
        label4 = tk.Label(main_window, text="login failed")
        label4.grid(row=6, column=150, padx=0, pady=10)

def check_action():
    user = username_text.get()
    pwd = password_text.get()
    if pwd[0].isupper() and len(pwd) >= 8 and any(char.isdigit() for char in pwd):
        label6 = tk.Label(main_window, text="strong password")
        label6.grid(row=7, column=150, padx=0, pady=10)
        save = tk.Button(main_window, text="save", command=save_action)
        save.grid(row=3, column=120, padx=0, pady=10)

    else:
        label7 = tk.Label(main_window, text="weak password")
        label7.grid(row=8, column=150, padx=0, pady=10)
        username_text.delete(0, tk.END)
        password_text.delete(0, tk.END)
        username_text.focus()
        label5.config(text="")
        
    
def save_action():
    user = username_text.get()
    pwd = password_text.get()

    if user and pwd:
        csv_path = r"C:\Users\Nikhi\OneDrive\Desktop\python\password.csv"
        with open(csv_path, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([user, pwd])
        label5.config(text="Credentials saved", fg="green")
    else:
        label5.config(text="Please enter both username and password", fg="red")

def clear_action():
    username_text.delete(0, tk.END)
    password_text.delete(0, tk.END)
    label5.config(text="")

def csv_to_sqlserver():
    # Read CSV
    csv_path = r"C:\Users\Nikhi\OneDrive\Desktop\python\password.csv"
    df = pd.read_csv(csv_path)

    # Connect to SQL Server
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=localhost,1433;"
        "UID=sa;"
        "PWD=Nikhil@123;"
    )
    cursor = conn.cursor()

    # Create table if it does not exist
    cursor.execute("""
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='users' AND xtype='U')
    CREATE TABLE users (
        username VARCHAR(50),
        password VARCHAR(50)
    )
    """)
    conn.commit()

    # Insert rows
    for _, row in df.iterrows():
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", row.username, row.password)

    conn.commit()
    cursor.close()
    conn.close()

    print("CSV successfully imported into SQL Server!")

main_window = tk.Tk()
main_window.geometry("400x300")
main_window.title("my first project")
label1 = tk.Label(main_window, text="enter username and password")
label1.grid(row=0, column=150, padx=0, pady=10)

username = tk.Label(main_window, text="username")
username.grid(row=1, column=0, padx=5, pady=10)

username_text = tk.Entry(main_window)
username_text.grid(row=1, column=1, padx=5, pady=10)

password = tk.Label(main_window, text="password")
password.grid(row=2, column=0, padx=5, pady=10)

password_text = tk.Entry(main_window)
password_text.grid(row=2, column=1, padx=5, pady=10)

check = tk.Button(main_window, text="check", command=check_action)
check.grid(row=3, column=100, padx=0, pady=10)

submit = tk.Button(main_window, text="submit", command=submit_action)
submit.grid(row=3, column=150, padx=0, pady=10)

clear = tk.Button(main_window, text="Clear", command=clear_action)
clear.grid(row=3, column=160, padx=0, pady=10)

# Add a label for feedback after saving
label5 = tk.Label(main_window, text="")
label5.grid(row=4, column=1, padx=5, pady=10)


main_window.mainloop()
csv_to_sqlserver()
