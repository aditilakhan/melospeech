import tkinter as tk
from tkinter import messagebox
import sys
import subprocess
import os

print("\n--- Debugging profile_settings_gui.py path issue ---")
print(f"__file__ (current script path): {os.path.abspath(__file__)}")

script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)  
print(f"script_dir (directory of this script): {script_dir}")
print(f"parent_dir (expected MELOSPEECH/ directory): {parent_dir}")

print("\nsys.path BEFORE modification:")
for p in sys.path:
    print(f"  - {p}")

if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
    print("\nParent directory ADDED to sys.path.")
else:
    print("\nParent directory already in sys.path.")

print("\nsys.path AFTER modification:")
for p in sys.path:
    print(f"  - {p}")
print("--- Debugging profile_settings_gui.py path issue END ---\n")

from utils import load_profile_by_username  

if len(sys.argv) > 1:
    username = sys.argv[1]
    user_profile = load_profile_by_username(username)
    if not user_profile:
        messagebox.showerror("Profile Error", "User profile not found. Please log in again.")
        sys.exit()
else:
    messagebox.showerror("Access Error", "No username provided. Cannot access profile settings.")
    sys.exit()

def back_to_dashboard():
    current_window.destroy()
    dashboard_path = os.path.join(parent_dir, "dashboard.py")
    subprocess.Popen([sys.executable, dashboard_path, username])

current_window = tk.Tk()
current_window.title(f"MeloSpeech - Profile Settings ({username})")
current_window.geometry("800x500")
current_window.configure(bg="#e8f0fe")
current_window.resizable(False, False)

header = tk.Frame(current_window, bg="#2c3e50", height=50)
header.pack(fill="x")

app_title = tk.Label(header, text="MeloSpeech", font=("Georgia", 18, "bold"), fg="white", bg="#2c3e50")
app_title.pack(side="left", padx=20, pady=10)

back_btn = tk.Button(header, text="Back to Dashboard", command=back_to_dashboard,
                     bg="#1976d2", fg="white", font=("Georgia", 9, "bold"),
                     relief="flat", bd=0, activebackground="#1565c0", cursor="hand2")
back_btn.pack(side="right", padx=10, pady=10)

main_content_frame = tk.Frame(current_window, bg="#e8f0fe", padx=20, pady=20)
main_content_frame.pack(pady=20, padx=50, fill="both", expand=True)

profile_box = tk.Frame(main_content_frame, bg="white", padx=30, pady=30, bd=2, relief="groove")
profile_box.pack(fill="both", expand=True)

tk.Label(profile_box, text="Your Profile Information", font=("Georgia", 16, "bold"),
         fg="#2c3e50", bg="white").pack(pady=(0, 10))

separator = tk.Frame(profile_box, bg="#cfd8dc", height=2)
separator.pack(fill="x", pady=(0, 15))

data_font = ("Georgia", 12)
data_color = "#37474f"

if user_profile:
    tk.Label(profile_box, text=f"👤 Username: {user_profile.get('username', 'N/A')}",
             font=data_font, fg=data_color, bg="white", anchor="w").pack(fill="x", pady=5)
    tk.Label(profile_box, text=f"📧 Email: {user_profile.get('email', 'N/A')}",
             font=data_font, fg=data_color, bg="white", anchor="w").pack(fill="x", pady=5)
    tk.Label(profile_box, text=f"🕓 Registration Date: {user_profile.get('registration_date', 'N/A').strftime('%Y-%m-%d %H:%M') if user_profile.get('registration_date') else 'N/A'}",
             font=data_font, fg=data_color, bg="white", anchor="w").pack(fill="x", pady=5)
else:
    tk.Label(profile_box, text="Profile data could not be loaded.",
             font=data_font, fg="red", bg="white", anchor="w").pack(fill="x", pady=5)

tk.Label(profile_box, text="\nMore settings options coming soon!",
         font=("Georgia", 10, "italic"), fg="#888888", bg="white").pack(pady=(10, 0))

tk.Label(current_window, text="© MeloSpeech.",
         bg="#2c3e50", fg="white", font=("Georgia", 9)).pack(side="bottom", fill="x")

current_window.mainloop()
