import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import re

def show_register_screen():
    register_win = tk.Tk()
    register_win.title("Register | MeloSpeech")
    register_win.geometry("800x500")
    register_win.resizable(False, False)

    bg_path = os.path.join("assets", "backgroundsimple.png")
    try:
        bg_image = Image.open(bg_path)
        bg_image = bg_image.resize((800, 500), Image.LANCZOS)
        bg_photo = ImageTk.PhotoImage(bg_image)
    except Exception as e:
        messagebox.showerror("Image Error", f"Background image load failed:\n{e}")
        return

    bg_label = tk.Label(register_win, image=bg_photo)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    frame = tk.Frame(register_win, bg="white", bd=2, relief="ridge")
    frame.place(x=250, y=50, width=300, height=400)

    tk.Label(frame, text="Create an Account", font=("Arial", 16, "bold"), bg="white", fg="#1e90ff").pack(pady=10)

    # Full Name
    tk.Label(frame, text="Full Name", font=("Arial", 10), bg="white", anchor="w").pack(padx=20, fill="x")
    entry_fullname = tk.Entry(frame, font=("Arial", 11))
    entry_fullname.pack(ipady=4, padx=20, pady=(0, 10), fill="x")

    # Email
    tk.Label(frame, text="Email Address", font=("Arial", 10), bg="white", anchor="w").pack(padx=20, fill="x")
    entry_email = tk.Entry(frame, font=("Arial", 11))
    entry_email.pack(ipady=4, padx=20, pady=(0, 10), fill="x")

    # Username
    tk.Label(frame, text="Username", font=("Arial", 10), bg="white", anchor="w").pack(padx=20, fill="x")
    entry_username = tk.Entry(frame, font=("Arial", 11))
    entry_username.pack(ipady=4, padx=20, pady=(0, 10), fill="x")

    # Password
    tk.Label(frame, text="Password", font=("Arial", 10), bg="white", anchor="w").pack(padx=20, fill="x")
    entry_password = tk.Entry(frame, font=("Arial", 11), show="*")
    entry_password.pack(ipady=4, padx=20, pady=(0, 10), fill="x")

    # Confirm Password
    tk.Label(frame, text="Confirm Password", font=("Arial", 10), bg="white", anchor="w").pack(padx=20, fill="x")
    entry_confirm_password = tk.Entry(frame, font=("Arial", 11), show="*")
    entry_confirm_password.pack(ipady=4, padx=20, pady=(0, 10), fill="x")

    def validate_registration():
        fullname = entry_fullname.get().strip()
        email = entry_email.get().strip()
        username = entry_username.get().strip()
        password = entry_password.get().strip()
        confirm_password = entry_confirm_password.get().strip()

        # Full Name Validation
        if fullname == "":
            messagebox.showerror("Input Error", "Please enter your full name.")
            return

        # Email Validation
        email_regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not re.match(email_regex, email):
            messagebox.showerror("Input Error", "Please enter a valid email address.")
            return

        # Username Validation
        if username == "":
            messagebox.showerror("Input Error", "Please enter a username.")
            return
        if not username.isalnum():
            messagebox.showerror("Input Error", "Username must be alphanumeric without spaces.")
            return

        # Password Validation
        if password == "":
            messagebox.showerror("Input Error", "Please enter a password.")
            return
        if len(password) < 6:
            messagebox.showerror("Input Error", "Password must be at least 6 characters long.")
            return

        # Confirm Password
        if confirm_password == "":
            messagebox.showerror("Input Error", "Please confirm your password.")
            return
        if password != confirm_password:
            messagebox.showerror("Input Error", "Passwords do not match.")
            return

        # Save the user details
        try:
            with open("users.txt", "a") as f:
                f.write(f"{username},{password}\n")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save user: {e}")
            return

        messagebox.showinfo("Success", "Account Created Successfully!")

        # CLOSE REGISTER SCREEN and OPEN LOGIN SCREEN
        register_win.destroy()
        from modules.login_screen import show_login_screen
        show_login_screen()

    def go_to_login():
        register_win.destroy()
        from modules.login_screen import show_login_screen
        show_login_screen()

    # Register Button
    register_button = tk.Button(frame, text="Register", command=validate_registration,
                                font=("Arial", 11, "bold"),
                                bg="#1e90ff", fg="white", bd=0,
                                activebackground="#1c86ee", cursor="hand2")
    register_button.pack(pady=(10, 5), ipadx=10, ipady=5)

    # Go to Login Button
    login_redirect_button = tk.Button(frame, text="Already have an account? Login", command=go_to_login,
                                      font=("Arial", 9, "bold"),
                                      bg="#28a745", fg="white", bd=0,
                                      activebackground="#218838", cursor="hand2")
    login_redirect_button.pack(pady=(5, 10), ipadx=5, ipady=3)

    register_win.mainloop()

if __name__ == "__main__":
    show_register_screen()