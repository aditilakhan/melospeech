# modules/speech_practice.py

import tkinter as tk
from tkinter import messagebox
import threading
import time

def show_speech_practice(root, show_dashboard):
    # Clear previous widgets
    for widget in root.winfo_children():
        widget.destroy()

    root.title("Speech Practice | MeloSpeech")

    title_label = tk.Label(root, text="Speech Practice", font=("Helvetica", 20, "bold"), fg="#0056b3")
    title_label.pack(pady=15)

    desc_label = tk.Label(root, text="This module helps improve pronunciation, articulation,\nand fluency with guided speech exercises.", font=("Helvetica", 12), justify="center")
    desc_label.pack(pady=10)

    # Progress Counter
    counter = tk.IntVar(value=0)

    progress_label = tk.Label(root, text="Progress: 0 practices done!", font=("Helvetica", 12), fg="green")
    progress_label.pack(pady=5)

    # Animated feedback text
    feedback_label = tk.Label(root, text="", font=("Helvetica", 12, "italic"), fg="#FF5733")
    feedback_label.pack(pady=10)

    def animate_feedback():
        messages = ["Repeat after me: Hello!", "Great job! Let's try again.", "Now say: Welcome!", "You're improving!"]
        while True:
            for msg in messages:
                feedback_label.config(text=msg)
                time.sleep(2)

    # Start animation thread
    threading.Thread(target=animate_feedback, daemon=True).start()

    # Dummy pronunciation action
    def practice_action():
        counter.set(counter.get() + 1)
        progress_label.config(text=f"Progress: {counter.get()} practices done!")
        messagebox.showinfo("Great!", "Nice pronunciation! Keep going 👏")

    practice_btn = tk.Button(root, text="Pronounce After Me 🎤", command=practice_action, bg="#0056b3", fg="white", font=("Helvetica", 12, "bold"), width=20)
    practice_btn.pack(pady=10)

    back_btn = tk.Button(root, text="Back to Dashboard", command=lambda: show_dashboard(root), bg="#0056b3", fg="white", font=("Helvetica", 12, "bold"), width=20)
    back_btn.pack(pady=10)
