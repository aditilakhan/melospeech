import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os

# --- Function Definitions ---
def open_login():
    window.destroy()
    os.system("python login.py")

def open_register():
    window.destroy()
    os.system("python register.py")

def show_home():
    messagebox.showinfo("Home", "🎵 Welcome to MeloSpeech!\nAn intelligent language learning app powered by music and ML.")

def show_about():
    messagebox.showinfo("About Us", "MeloSpeech is a smart speech-powered app that enhances language learning through music.")

def show_help():
    messagebox.showinfo("Help", "Need help?\nReach us at: support@melospeech.com")

# --- GUI Setup ---
window = tk.Tk()
window.title("MeloSpeech | Welcome!")
window.geometry("800x500")
window.resizable(False, False)

# --- Background Image Setup ---
try:
    bg_image = Image.open("bg_welcome_logo.png")
    bg_image = bg_image.resize((800, 500))
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(window, image=bg_photo)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
except Exception as e:
    window.config(bg="#eaf6ff")
    print("Background image not loaded:", e)

# --- Bottom Frame ---
bottom_frame = tk.Frame(window, bg='white')
bottom_frame.pack(side="bottom", fill="x", pady=10)

# --- Left Side: Info Buttons ---
left_frame = tk.Frame(bottom_frame, bg='white')
left_frame.pack(side="left", padx=20)

tk.Button(left_frame, text="Home", command=show_home,
          bg="white", fg="#1976d2", font=("Arial", 9, "underline"),
          bd=0, cursor="hand2").pack(side="left", padx=5)

tk.Button(left_frame, text="About Us", command=show_about,
          bg="white", fg="#1976d2", font=("Arial", 9, "underline"),
          bd=0, cursor="hand2").pack(side="left", padx=5)

tk.Button(left_frame, text="Help", command=show_help,
          bg="white", fg="#1976d2", font=("Arial", 9, "underline"),
          bd=0, cursor="hand2").pack(side="left", padx=5)

# --- Right Side: Auth Buttons ---
right_frame = tk.Frame(bottom_frame, bg='white')
right_frame.pack(side="right", padx=20)

tk.Button(right_frame, text="Login", width=12, command=open_login,
          bg="#1561a0", fg="white", font=("Georgia", 10, "bold")).pack(side="left", padx=5)

tk.Button(right_frame, text="Register", width=12, command=open_register,
          bg="#18c41e", fg="white", font=("Georgia", 10, "bold")).pack(side="left", padx=5)

# --- Run the App ---
window.mainloop()
