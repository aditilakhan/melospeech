import tkinter as tk
from tkinter import messagebox
import random
import sys
from datetime import datetime
from pymongo import MongoClient
import subprocess

username = sys.argv[1]  

client = MongoClient("mongodb://localhost:27017/")
db = client["melospeech_db"]
vocab_col = db["vocabulary_progress"]

quiz_data = [
    {
        "word": "eloquent",
        "meaning": "Fluent or persuasive in speaking or writing",
        "options": [
            "Rude in conversation",
            "Unable to speak clearly",
            "Fluent or persuasive in speaking or writing",
            "Speaking in foreign languages"
        ]
    },
    {
        "word": "benevolent",
        "meaning": "Well meaning and kindly",
        "options": [
            "Selfish and mean",
            "Well meaning and kindly",
            "Aggressive and hostile",
            "Shy and reserved"
        ]
    },
    {
        "word": "resilient",
        "meaning": "Able to withstand or recover quickly from difficulty",
        "options": [
            "Lazy and slow",
            "Quick to anger",
            "Able to withstand or recover quickly from difficulty",
            "Forgetful and distracted"
        ]
    },
    {
        "word": "serene",
        "meaning": "Calm, peaceful, and untroubled",
        "options": [
            "Loud and noisy",
            "Nervous and anxious",
            "Calm, peaceful, and untroubled",
            "Easily distracted"
        ]
    },
    {
        "word": "vivid",
        "meaning": "Producing powerful feelings or strong images in the mind",
        "options": [
            "Boring and dull",
            "Producing powerful feelings or strong images in the mind",
            "Forgetful and lazy",
            "Soft and gentle"
        ]
    }
]

def load_new_question():
    global current_question
    current_question = random.choice(quiz_data)
    word_label.config(text=f"What does '{current_question['word']}' mean?")
    answer_entry.delete(0, tk.END)
    result_label.config(text="")

    for idx, option in enumerate(current_question['options'], 1):
        option_labels[idx - 1].config(text=f"{idx}. {option}", anchor="w")

def check_answer():
    user_answer = answer_entry.get().strip().lower()

    if not user_answer:
        messagebox.showwarning("Input Required", "Please type your answer based on the options above.")
        return

    correct_answer = current_question['meaning'].lower()
    score = 1 if user_answer in correct_answer else 0

    if score == 1:
        messagebox.showinfo("Correct", "✅ Correct answer!")
    else:
        messagebox.showerror("Incorrect", f"❌ Incorrect\n\nCorrect answer: {current_question['meaning']}")

    vocab_col.insert_one({
        "username": username,
        "word": current_question['word'],
        "user_answer": user_answer,
        "correct_answer": current_question['meaning'],
        "is_correct": bool(score),
        "timestamp": datetime.now()
    })

def back_to_dashboard():
    window.destroy()
    subprocess.Popen([sys.executable, "dashboard.py", username])

window = tk.Tk()
window.title("Vocabulary Builder Quiz")
window.geometry("800x500")
window.configure(bg="#f8faff")
window.resizable(False, False)

header = tk.Frame(window, bg="#2c3e50")
header.pack(fill="x")
tk.Label(header, text="📚 Vocabulary Builder", font=("Georgia", 16, "bold"), bg="#2c3e50", fg="white").pack(side="left", padx=20, pady=10)

content = tk.Frame(window, bg="#f8faff")
content.pack(pady=20)

word_label = tk.Label(content, text="", font=("Georgia", 14, "bold"), bg="#f8faff", fg="#2c3e50")
word_label.pack(pady=10)

answer_entry = tk.Entry(content, font=("Georgia", 12), width=60)
answer_entry.pack(pady=5)

suggestion_label = tk.Label(content, text="Choose the correct meaning:", font=("Georgia", 12), bg="#f8faff", fg="#333")
suggestion_label.pack(pady=10)

option_labels = []
for _ in range(4):
    lbl = tk.Label(content, text="", font=("Georgia", 10), bg="#f8faff", fg="#2c3e50", anchor="w")
    lbl.pack(fill="x", padx=150, anchor="w")
    option_labels.append(lbl)

button_frame = tk.Frame(content, bg="#f8faff")
button_frame.pack(pady=20)

submit_btn = tk.Button(button_frame, text="Check Answer", font=("Georgia", 11, "bold"),
                       bg="#3498db", fg="white", width=18, height=2, relief="flat", command=check_answer)
submit_btn.grid(row=0, column=0, padx=10)

next_btn = tk.Button(button_frame, text="Next Word", font=("Georgia", 11, "bold"),
                     bg="#16a085", fg="white", width=15, height=2, relief="flat", command=load_new_question)
next_btn.grid(row=0, column=1, padx=10)

result_label = tk.Label(content, text="", font=("Georgia", 11), bg="#f8faff", fg="#2c3e50")
result_label.pack(pady=5)

back_btn = tk.Button(content, text="Back to Dashboard", font=("Georgia", 10, "bold"),
                     bg="#2c3e50", fg="white", relief="flat", padx=10, pady=5,
                     command=back_to_dashboard, cursor="hand2")
back_btn.pack(pady=(10, 20))

tk.Label(window, text="© MeloSpeech.",
         bg="#2c3e50", fg="white", font=("Georgia", 8)).pack(side="bottom", fill="x")

load_new_question()
window.mainloop()
