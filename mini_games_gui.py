# import tkinter as tk
# from tkinter import messagebox
# import subprocess
# import sys
# import os

# # --- Get the logged-in username from arguments ---
# if len(sys.argv) > 1:
#     username = sys.argv[1]
# else:
#     messagebox.showerror("Error", "No user logged in.")
#     sys.exit()

# # --- Paths ---
# SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# ROOT_DIR = os.path.dirname(SCRIPT_DIR)
# DASHBOARD_PATH = os.path.join(ROOT_DIR, "dashboard_gui.py")
# MAIN_PATH = os.path.join(ROOT_DIR, "main.py")

# # --- Navigation Functions ---
# def go_back_to_dashboard():
#     root.destroy()
#     subprocess.Popen([sys.executable, DASHBOARD_PATH, username])

# def logout():
#     confirm = messagebox.askyesno("Logout", "Are you sure you want to logout from the app?")
#     if confirm:
#         root.destroy()
#         subprocess.Popen([sys.executable, MAIN_PATH])

# # --- GUI Setup ---
# root = tk.Tk()
# root.title("🎮 MeloSpeech - Mini Games")
# root.geometry("800x500")
# root.configure(bg="#fcf3cf")
# root.resizable(False, False)

# # --- Header ---
# header = tk.Frame(root, bg="#f39c12", height=50)
# header.pack(fill="x")

# tk.Label(header, text=f"Welcome {username}! Enjoy Mini Games 🎉", font=("Segoe UI", 14, "bold"),
#          bg="#f39c12", fg="white").pack(pady=10)

# # --- Buttons for Navigation ---
# nav_frame = tk.Frame(root, bg="#fcf3cf")
# nav_frame.pack(pady=10)

# tk.Button(nav_frame, text="⬅ Back to Dashboard", command=go_back_to_dashboard,
#           font=("Segoe UI", 10, "bold"), bg="#2980b9", fg="white", padx=10,
#           relief="flat", cursor="hand2").grid(row=0, column=0, padx=10)

# tk.Button(nav_frame, text="🚪 Logout from App", command=logout,
#           font=("Segoe UI", 10, "bold"), bg="#e74c3c", fg="white", padx=10,
#           relief="flat", cursor="hand2").grid(row=0, column=1, padx=10)

# # --- Mini Games Area ---
# games_frame = tk.Frame(root, bg="#fcf3cf")
# games_frame.pack(pady=30)

# tk.Label(games_frame, text="🎲 Mini Game Placeholder 1\nGuess the Word!", font=("Segoe UI", 12, "bold"),
#          bg="#fef9e7", fg="#34495e", width=50, height=4, relief="ridge").pack(pady=10)

# tk.Label(games_frame, text="🧠 Mini Game Placeholder 2\nMemory Match Coming Soon!", font=("Segoe UI", 12, "bold"),
#          bg="#fef9e7", fg="#34495e", width=50, height=4, relief="ridge").pack(pady=10)

# # --- Footer ---
# tk.Label(root, text="© 2025 MeloSpeech | Mini Games", bg="#f39c12", fg="white", font=("Segoe UI", 9)).pack(side="bottom", fill="x")

# root.mainloop()
