import tkinter as tk
from tkinter import messagebox
import subprocess
import sys

if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    messagebox.showerror("Navigation Error", "Username not provided.")
    sys.exit()

window = tk.Tk()
window.title("About|MeloSpeech")
window.geometry("800x500")
window.configure(bg="#f0f4fc")
window.resizable(False, False)


tk.Label(window, text="{About MeloSpeech}", font=("Georgia", 16, "bold"),
         bg="#2c3e50", fg="white", pady=10).pack(fill="x")


about_text = """
MeloSpeech is an AI-powered desktop application designed to enhance language learning 
through interactive features like speech emotion recognition, lyric sentiment analysis,
pronunciation drills, vocabulary quizzes, and a personalized progress tracker.

It helps users develop fluency by blending rhythm, emotion, and expression.
"""
tk.Label(window, text=about_text, font=("Georgia", 11),
         bg="#f0f4fc", justify="left", anchor="w").pack(pady=10, padx=30)

facts = """
🔍 Unique Highlights:
- Music-based learning modules
- Emotion-aware speech interaction
- Progress visualized with radar charts
- Game-like vocabulary builder
"""
tk.Label(window, text=facts, font=("Georgia", 11),
         bg="#f0f4fc", fg="#2c3e50", justify="left", anchor="w").pack(pady=10, padx=30)

future = """
🚀 Future Enhancements:
- Real-time speech-to-text feedback
- AI tutor suggestions for weak areas
- Multiplayer speaking challenges
- Mobile app version
"""
tk.Label(window, text=future, font=("Georgia", 11),
         bg="#f0f4fc", fg="#34495e", justify="left", anchor="w").pack(pady=10, padx=30)

def back_to_dashboard():
    window.destroy()
    subprocess.Popen([sys.executable, "dashboard.py", username])

def logout():
    if messagebox.askyesno("Logout", "Do you really want to logout?"):
        window.destroy()
        subprocess.Popen([sys.executable, "main.py"])

btn_frame = tk.Frame(window, bg="#f0f4fc")
btn_frame.pack(pady=20)

tk.Button(btn_frame, text="Back to Dashboard", bg="#2980b9", fg="white",
          font=("Georgia", 10, "bold"), padx=15, command=back_to_dashboard).pack(side="left", padx=10)

tk.Button(btn_frame, text="🔒 Logout", bg="#e74c3c", fg="white",
          font=("Georgia", 10, "bold"), padx=15, command=logout).pack(side="left", padx=10)

tk.Label(window, text="© MeloSpeech.",
         bg="#2c3e50", fg="white", font=("Georgia", 8)).pack(side="bottom", fill="x")

window.mainloop()

