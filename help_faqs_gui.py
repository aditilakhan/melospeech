import tkinter as tk
from tkinter import messagebox
import sys
import subprocess
import os

if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    messagebox.showerror("Access Error", "No username provided. Cannot access Help/FAQs.")
    sys.exit()

def back_to_dashboard():
    """Destroys current screen and returns to the dashboard."""
    current_window.destroy()
    dashboard_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "dashboard.py")
    subprocess.Popen([sys.executable, dashboard_path, username])

current_window = tk.Tk()
current_window.title(f"MeloSpeech|Help & FAQs ({username})")
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

tk.Label(main_content_frame, text="Help & Frequently Asked Questions", font=("Georgia", 16, "bold"),
         fg="#333333", bg="#ffffff").pack(pady=(0, 20))

faqs = [
    {"q": "What is MeloSpeech?", "a": "MeloSpeech is an innovative language learning app that uses AI feedback and engaging music exercises to improve your pronunciation, expand vocabulary, and track your progress."},
    {"q": "How does pronunciation practice work?", "a": "Our AI analyzes your speech and provides instant feedback on your accuracy, helping you refine your pronunciation. Just speak into your microphone and get real-time scores and suggestions."},
    {"q": "Can I track my learning progress?", "a": "Yes! The Progress Tracker module allows you to view your learning history, identify areas for improvement, and stay motivated by seeing your achievements over time."},
    {"q": "Is internet connection required?", "a": "Some features, especially those involving AI analysis and real-time updates (like lyrics sentiment), require an internet connection. Offline features are limited."},
    {"q": "How do I contact support?", "a": "If you have any further questions or encounter issues, please visit our website at melospeech.com/support or email us at support@melospeech.com."}
]

canvas = tk.Canvas(main_content_frame, bg="#ffffff", highlightthickness=0)
canvas.pack(side="left", fill="both", expand=True)

scrollbar = tk.Scrollbar(main_content_frame, orient="vertical", command=canvas.yview)
scrollbar.pack(side="right", fill="y")

canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion = canvas.bbox("all")))

scrollable_frame = tk.Frame(canvas, bg="#ffffff")
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=640) 

for faq in faqs:
    faq_frame = tk.Frame(scrollable_frame, bg="#f8f8f8", bd=1, relief="solid", padx=10, pady=10)
    faq_frame.pack(fill="x", pady=5)
    
    tk.Label(faq_frame, text=f"Q: {faq['q']}", font=("Georgia", 11, "bold"), fg="#2c3e50", bg="#f8f8f8", anchor="w", wraplength=600, justify="left").pack(fill="x")
    tk.Label(faq_frame, text=f"A: {faq['a']}", font=("Georgia", 9), fg="#666666", bg="#f8f8f8", wraplength=600, justify="left", anchor="w").pack(fill="x")

tk.Label(current_window, text="© MeloSpeech.",
         bg="#2c3e50", fg="white", font=("Georgia", 8)).pack(side="bottom", fill="x")

current_window.mainloop()
