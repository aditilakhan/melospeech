import tkinter as tk
from tkinter import messagebox
from textblob import TextBlob
import sys
from pymongo import MongoClient
from datetime import datetime
import subprocess

if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    messagebox.showerror("Login Error", "Username not provided.")
    sys.exit()


client = MongoClient("mongodb://localhost:27017/")
db = client["melospeech_db"]
sentiment_col = db["lyrics_sentiment"]


def get_music_recommendation(mood):
    recommendations = {
        "Positive": "Try listening to: 'Happy - Pharrell Williams 🎶'",
        "Negative": "Try listening to: 'Someone Like You - Adele 🎧'",
        "Neutral":  "Try listening to: 'Weightless - Marconi Union 🎵'"
    }
    return recommendations.get(mood, "Explore some music that suits your mood!")

def analyze_sentiment():
    lyrics = lyrics_input.get("1.0", tk.END).strip()
    if not lyrics:
        messagebox.showwarning("Input Error", "Please enter some lyrics to analyze.")
        return

    blob = TextBlob(lyrics)
    polarity = blob.sentiment.polarity
    mood = "Positive" if polarity > 0 else "Negative" if polarity < 0 else "Neutral"
    recommendation = get_music_recommendation(mood)

    popup = f"""
🎯 Polarity: {polarity:.2f}
🧠 Mood: {mood}
🎵 {recommendation}
""".strip()

    messagebox.showinfo("Sentiment Analysis Result", popup)

    sentiment_col.insert_one({
        "username": username,
        "lyrics": lyrics,
        "polarity": polarity,
        "mood": mood,
        "recommendation": recommendation,
        "timestamp": datetime.now()
    })

def back_to_dashboard():
    window.destroy()
    subprocess.Popen([sys.executable, "dashboard.py", username])


window = tk.Tk()
window.title("Lyrics Sentiment Analysis")
window.geometry("800x500")
window.configure(bg="#f7f9fb")
window.resizable(False, False)


header = tk.Frame(window, bg="#2c3e50", height=50)
header.pack(fill="x")
tk.Label(header, text="🎵 Lyrics Sentiment Analysis", font=("Georgia", 16, "bold"),
         bg="#2c3e50", fg="white", pady=10).pack(side="left", padx=20)

content = tk.Frame(window, bg="#f7f9fb")
content.pack(pady=30)

instruction = tk.Label(content, text="Paste your lyrics below and analyze their sentiment.",
                       font=("Georgia", 12), bg="#f7f9fb", fg="#333")
instruction.pack(pady=(0, 10))

lyrics_input = tk.Text(content, width=70, height=8, font=("Georgia", 10), bd=1, relief="solid")
lyrics_input.pack(pady=10)

analyze_btn = tk.Button(content, text="🧠 Analyze Sentiment", font=("Georgia", 11, "bold"),
                        bg="#3498db", fg="white", width=30, height=2, relief="flat",
                        command=analyze_sentiment)
analyze_btn.pack(pady=10)


tk.Button(window, text=" Back to Dashboard", bg="#555", fg="white",
          font=("Georgia", 10, "bold"), command=back_to_dashboard).pack(pady=10)


tk.Label(window, text="© MeloSpeech.",
         bg="#2c3e50", fg="white", font=("Georgia", 8)).pack(side="bottom", fill="x")

window.mainloop()
