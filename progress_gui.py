import tkinter as tk
from tkinter import messagebox
import sys
from datetime import datetime
from pymongo import MongoClient
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
import csv
import os
import subprocess

matplotlib.use("Agg")

if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    messagebox.showerror("Login Error", "Username not provided.")
    sys.exit()

try:
    client = MongoClient("mongodb://localhost:27017/")
    db = client["melospeech_db"]
    client.admin.command('ismaster')
except Exception as e:
    messagebox.showerror("Database Error", f"Could not connect to MongoDB: {e}")
    sys.exit()

try:
    db["progress_logs"].insert_one({
        "username": username,
        "viewed_on": datetime.now(),
        "module": "Progress Tracker"
    })
except Exception as e:
    print(f"Could not log visit: {e}")

def get_user_stats():
    stats = {
        "Speech Emotion": 0,
        "Lyrics Sentiment": 0,
        "Pronunciation": 0,
        "Vocab (Correct)": 0,
        "Vocab (Total)": 0
    }
    try:
        stats["Speech Emotion"] = db["emotion_results"].count_documents({"username": username})
        stats["Lyrics Sentiment"] = db["lyrics_sentiment"].count_documents({"username": username})
        stats["Pronunciation"] = db["pronunciation_results"].count_documents({"username": username})
        stats["Vocab (Correct)"] = db["vocabulary_progress"].count_documents({"username": username, "is_correct": True})
        stats["Vocab (Total)"] = db["vocabulary_progress"].count_documents({"username": username})
    except Exception as e:
        messagebox.showwarning("Database Warning", f"Could not fetch user stats: {e}")
    return stats

def export_progress():
    stats = get_user_stats()
    filename = f"progress_{username}.csv"
    filepath = os.path.join(os.getcwd(), filename)

    try:
        with open(filepath, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Module", "Completed Activities", "Exported On"])
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            for key, val in stats.items():
                writer.writerow([key, val, now])
        messagebox.showinfo("Export Success", f"Progress exported to:\n{filename}")
    except Exception as e:
        messagebox.showerror("Export Failed", f"Error exporting CSV:\n{e}")

# --- Back to Dashboard ---
def back_to_dashboard():
    window.destroy()
    try:
        subprocess.Popen([sys.executable, "dashboard.py", username])
    except Exception as e:
        messagebox.showerror("Error", f"Could not open dashboard: {e}")

window = tk.Tk()
window.title("Progress Tracker")
window.geometry("800x500")
window.configure(bg="#f0f4fc")
window.resizable(False, False)

header = tk.Frame(window, bg="#2c3e50")
header.pack(fill="x")
tk.Label(header, text="📊 Progress Tracker", font=("Georgia", 18, "bold"),
          bg="#2c3e50", fg="white", pady=10).pack(side="left", padx=20)

main_frame = tk.Frame(window, bg="#f0f4fc")
main_frame.pack(expand=True, fill="both")

stats = get_user_stats()
labels = list(stats.keys())
values = list(stats.values())

fig, ax = plt.subplots(figsize=(5.5, 3), facecolor="#f0f4fc")
bars = ax.bar(labels, values, color="#2980b9", edgecolor="black")
ax.set_title(f"{username}'s Learning Progress", fontsize=14, color="#2c3e50", pad=10)
ax.set_ylabel("Completed Activities", fontsize=11)
ax.set_ylim(0, max(values) + 2 if max(values) > 0 else 5)
plt.xticks(rotation=20, ha="right", fontsize=9)
plt.yticks(fontsize=9)
ax.tick_params(axis='x', colors='#2c3e50')
ax.tick_params(axis='y', colors='#2c3e50')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#ccc')
ax.spines['bottom'].set_color('#ccc')

for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, height + 0.2,
            f'{int(height)}', ha='center', va='bottom', fontsize=8, color="#2c3e50")

canvas = FigureCanvasTkAgg(fig, master=main_frame)
canvas.draw()
canvas.get_tk_widget().pack(pady=20)

btn_frame = tk.Frame(main_frame, bg="#f0f4fc")
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="⬅ Back to Dashboard", bg="#34495e", fg="white",
          font=("Georgia", 10, "bold"), width=20, pady=6, relief="flat",
          command=back_to_dashboard).grid(row=0, column=0, padx=10)

tk.Button(btn_frame, text="📥 Download Progress Report", bg="#27ae60", fg="white",
          font=("Georgia", 10, "bold"), width=25, pady=6, relief="flat",
          command=export_progress).grid(row=0, column=1, padx=10)

footer = tk.Frame(window, bg="#2c3e50")
footer.pack(fill="x", side="bottom")
tk.Label(footer, text="© MeloSpeech.",
          bg="#2c3e50", fg="white", font=("Georgia", 9), pady=8).pack()

window.mainloop()
