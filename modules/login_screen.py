# login.py

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
from modules.dashboard import show_dashboard

def show_login_screen():
    login_win = tk.Tk()
    login_win.title("Login | MeloSpeech")
    login_win.geometry("800x500")
    login_win.resizable(False, False)

    # 👉 Load background image
    bg_path = os.path.join("assets", "backgroundsimple.png")
    try:
        bg_image = Image.open(bg_path)
        bg_image = bg_image.resize((800, 500), Image.LANCZOS)
        bg_photo = ImageTk.PhotoImage(bg_image)
    except Exception as e:
        messagebox.showerror("Image Error", f"Failed to load background:\n{e}")
        login_win.destroy()
        return

    # 👉 Set background
    bg_label = tk.Label(login_win, image=bg_photo)
    bg_label.image = bg_photo
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    # 👉 Frame for login form
    frame = tk.Frame(login_win, bg="white", bd=2, relief="ridge")
    frame.place(x=250, y=100, width=300, height=300)

    title = tk.Label(frame, text="Login to MeloSpeech", font=("Arial", 16, "bold"), bg="white", fg="#1e90ff")
    title.pack(pady=15)

    # 👉 Username
    tk.Label(frame, text="Username", font=("Arial", 10), bg="white").pack(pady=(10, 0))
    username_entry = tk.Entry(frame, font=("Arial", 11))
    username_entry.pack(ipady=4, padx=20, pady=5, fill="x")

    # 👉 Password
    tk.Label(frame, text="Password", font=("Arial", 10), bg="white").pack(pady=(10, 0))
    password_entry = tk.Entry(frame, show="*", font=("Arial", 11))
    password_entry.pack(ipady=4, padx=20, pady=5, fill="x")

    # 👉 Login button function
    def login_action():
        username = username_entry.get().strip()
        password = password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Input Error", "Please enter both username and password.")
            return

        try:
            with open("users.txt", "r") as f:
                users = f.readlines()

            valid = any(user.strip() == f"{username},{password}" for user in users)

            if valid:
                messagebox.showinfo("Login Success", f"Welcome, {username}!")
                login_win.destroy()
                show_dashboard()
            else:
                messagebox.showerror("Login Failed", "Invalid username or password.")
        except FileNotFoundError:
            messagebox.showerror("Error", "No registered users found. Please register first.")

    # 👉 Login Button
    login_btn = tk.Button(frame, text="Login", command=login_action,
                          font=("Arial", 11, "bold"),
                          bg="#1e90ff", fg="white", bd=0,
                          activebackground="#1c86ee", cursor="hand2")
    login_btn.pack(pady=20, ipadx=10, ipady=5)

    login_win.mainloop()

# To run login screen directly
if __name__ == "__main__":
    show_login_screen()
