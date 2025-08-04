import tkinter as tk
from tkinter import messagebox
import sys
import subprocess
import os

if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    messagebox.showerror("Access Error", "No username provided. Cannot access notifications.")
    sys.exit()

def back_to_dashboard():
    """Destroys current screen and returns to the dashboard."""
    current_window.destroy()
    dashboard_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "dashboard.py")
    subprocess.Popen([sys.executable, dashboard_path, username])

current_window = tk.Tk()
current_window.title(f"MeloSpeech - Notifications ({username})")
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


main_content_frame = tk.Frame(current_window, bg="#ffffff", padx=20, pady=20)
main_content_frame.pack(pady=30, padx=50, fill="both", expand=True)

tk.Label(main_content_frame, text="App Updates & Notifications", font=("Georgia", 16, "bold"),
         fg="#333333", bg="#ffffff").pack(pady=(0, 20))


notifications = [
    {"title": "Welcome Bonus!", "details": "Enjoy 10 bonus points for completing your first pronunciation exercise!"},
    {"title": "New Feature: Lyric Mood Analysis!", "details": "Understand the emotional tone of your favorite songs' lyrics with our new AI-powered tool."},
    {"title": "MeloSpeech v1.1 Update", "details": "Improved AI feedback for speech and expanded vocabulary sets. Check it out!"},
    {"title": "Daily Goal Reminder", "details": "Don't forget your daily practice to improve your fluency!"},
    {"title": "Did you know?", "details": "Learning a new language can boost your cognitive skills and memory!"}
]

for notif in notifications:
    notif_frame = tk.Frame(main_content_frame, bg="#f8f8f8", bd=1, relief="solid", padx=10, pady=10)
    notif_frame.pack(fill="x", pady=5)
    
    tk.Label(notif_frame, text=notif["title"], font=("Georgia", 11, "bold"), fg="#2c3e50", bg="#f8f8f8", anchor="w").pack(fill="x")
    tk.Label(notif_frame, text=notif["details"], font=("Georgia", 9), fg="#666666", bg="#f8f8f8", wraplength=600, justify="left", anchor="w").pack(fill="x")


tk.Label(current_window, text="© MeloSpeech.",
         bg="#2c3e50", fg="white", font=("Georgia", 8)).pack(side="bottom", fill="x")

current_window.mainloop()
