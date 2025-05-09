import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
from modules.login_screen import show_login_screen
from modules.register_screen import show_register_screen


def show_welcome_screen():
    root = tk.Tk()
    root.title("MeloSpeech")
    root.geometry("800x500")
    root.resizable(False, False)

    # 👉 Canvas for background image
    canvas = tk.Canvas(root, width=800, height=500, highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    # 👉 Load and display background image
    bg_path = os.path.join("assets", "logoapp.png")
    bg_img = Image.open(bg_path)
    bg_img = bg_img.resize((800, 450), Image.LANCZOS)
    bg_tk = ImageTk.PhotoImage(bg_img)
    canvas.create_image(0, 0, anchor="nw", image=bg_tk)

    # ⭐ Keep a reference to avoid garbage collection
    canvas.bg_image = bg_tk

    # 👉 Bottom Frame for Tabs (aligned left)
    bottom_frame = tk.Frame(root, bg="#f9f9f9")
    bottom_frame.place(x=0, y=450, width=800, height=50)

    # 👉 Navigation Functions
    def show_home():
        messagebox.showinfo("Home", "Welcome to MeloSpeech!")

    def show_about():
        messagebox.showinfo("About", "MeloSpeech enhances speech through music-based learning.")

    def show_help():
        messagebox.showinfo("Help", "For help, contact: support@melospeech.ai")

    def go_to_login():
        root.destroy()
        show_login_screen()

    def go_to_register():
        root.destroy()
        show_register_screen()

    # 👉 Navigation Buttons
    home_btn = tk.Button(bottom_frame, text="Home", command=show_home, bg="white", fg="black", relief="flat")
    home_btn.place(x=10, y=10, width=60, height=30)

    about_btn = tk.Button(bottom_frame, text="About", command=show_about, bg="white", fg="black", relief="flat")
    about_btn.place(x=80, y=10, width=60, height=30)

    help_btn = tk.Button(bottom_frame, text="Help", command=show_help, bg="white", fg="black", relief="flat")
    help_btn.place(x=150, y=10, width=60, height=30)

    # 👉 Login/Register Buttons
    login_btn = tk.Button(root, text="Login", command=go_to_login, bg="#1e90ff", fg="white", font=("Arial", 12, "bold"))
    login_btn.place(x=550, y=460, width=100, height=30)

    register_btn = tk.Button(root, text="Register", command=go_to_register, bg="#28a745", fg="white", font=("Arial", 12, "bold"))
    register_btn.place(x=660, y=460, width=100, height=30)

    root.mainloop()
