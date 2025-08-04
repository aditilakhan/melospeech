import tkinter as tk
from tkinter import messagebox
import sys
import os
import librosa
import numpy as np
import joblib
import sounddevice as sd
import soundfile as sf
from datetime import datetime
from pymongo import MongoClient
import subprocess
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# --- Username Validation ---
if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    messagebox.showerror("Login Error", "Username not provided. Please log in first.")
    sys.exit()

# --- Load Model ---
model_path = os.path.join("model", "emotion_model.pkl")
if not os.path.exists(model_path):
    messagebox.showerror("Model Error", "Emotion model file not found.")
    sys.exit()

try:
    model = joblib.load(model_path)
except Exception as e:
    messagebox.showerror("Model Load Error", f"Failed to load emotion model: {e}")
    sys.exit()

# --- MongoDB Connection ---
try:
    client = MongoClient("mongodb://localhost:27017/")
    client.admin.command('ping')
    db = client["melospeech_db"]
    results_col = db["emotion_results"]
except Exception as e:
    messagebox.showwarning("MongoDB Error", f"Could not connect to MongoDB:\n{e}")
    results_col = None

# --- Tkinter Window ---
window = tk.Tk()
window.title("🎙️ MeloSpeech | Speech Emotion Recognition")
window.geometry("800x500")
window.configure(bg="#f0f4fc")
window.resizable(False, False)

# --- Header ---
header = tk.Frame(window, bg="#2c3e50", height=50)
header.pack(side="top", fill="x")
tk.Label(header, text="🎤 Speech Emotion Recognition", font=("Georgia", 16, "bold"),
         bg="#2c3e50", fg="white").pack(padx=20, pady=10, anchor="w")

# --- Content Frame ---
content = tk.Frame(window, bg="#f0f4fc")
content.pack(expand=True, fill="both", padx=30, pady=10)

tk.Label(content, text="Click below to record and analyze your voice emotion.",
         font=("Georgia", 12), bg="#f0f4fc", fg="#333").pack(pady=(5, 10))

# --- Graph Frame ---
graph_frame = tk.Frame(content, bg="#f0f4fc", bd=1, relief="solid")
graph_frame.pack(padx=10, pady=5, fill="both", expand=True)

fig, ax = plt.subplots(figsize=(6, 2))
ax.set_xlim(0, 3)
ax.set_ylim(-0.2, 0.2)
ax.set_title("Voice Waveform (Recording Not Started)")
ax.set_xlabel("Time (s)")
ax.set_ylabel("Amplitude")
ax.grid(True)

canvas = FigureCanvasTkAgg(fig, master=graph_frame)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(expand=True, fill="both")

# --- Record Audio ---
def record_audio(duration=3, sample_rate=22050, filename="temp.wav"):
    try:
        messagebox.showinfo("Recording", f"Recording for {duration} seconds...")
        recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)
        sd.wait()
        sf.write(filename, recording, sample_rate)

        time = np.linspace(0, duration, len(recording))
        ax.clear()
        ax.plot(time, recording.flatten(), color='teal')
        ax.set_title("Your Voice Waveform")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Amplitude")
        ax.set_xlim(0, duration)
        ax.grid(True)
        canvas.draw()

        return filename
    except Exception as e:
        messagebox.showerror("Recording Error", f"An error occurred during recording: {e}")
        return None

# --- Feature Extraction ---
def extract_features(file_path):
    try:
        audio, sr = librosa.load(file_path, res_type='kaiser_fast')
        mfccs = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=40)
        mfccs_scaled = np.mean(mfccs.T, axis=0)
        return mfccs_scaled.reshape(1, -1), mfccs.shape[1]
    except Exception as e:
        messagebox.showerror("Feature Error", f"Could not extract features: {e}")
        return None, None

# --- Predict Emotion ---
def predict_emotion():
    audio_file = record_audio()
    if audio_file:
        features, mfcc_dim = extract_features(audio_file)
        if features is not None:
            try:
                prediction = model.predict(features)[0]
                messagebox.showinfo("Emotion Detected", f"Detected Emotion: {prediction}")

                if results_col:
                    results_col.insert_one({
                        "username": username,
                        "predicted_emotion": prediction,
                        "timestamp": datetime.now(),
                        "model_used": "RandomForest (Speech)",
                        "feature_type": "MFCC",
                        "feature_count": 40,
                        "mfcc_shape": mfcc_dim,
                        "audio_duration_sec": 3
                    })
            except Exception as e:
                messagebox.showerror("Prediction Error", f"Prediction failed: {e}")

        if os.path.exists(audio_file):
            os.remove(audio_file)

# --- Buttons ---
tk.Button(content, text="🎙️ Record & Predict Emotion", font=("Georgia", 12, "bold"),
          bg="#298ebd", fg="white", width=30, height=2, command=predict_emotion).pack(pady=(10, 15))

# --- Back to Dashboard ---
def back_to_dashboard():
    window.destroy()
    subprocess.Popen([sys.executable, "dashboard.py", username])

tk.Button(content, text="⬅ Back to Dashboard", font=("Georgia", 10, "bold"),
          bg="#555", fg="white", padx=15, pady=8, command=back_to_dashboard).pack()

# --- Footer ---
footer = tk.Frame(window, bg="#2c3e50", height=30)
footer.pack(side="bottom", fill="x")
tk.Label(footer, text="© MeloSpeech.", bg="#2c3e50", fg="white", font=("Georgia", 8)).pack(side="right", padx=10)

# --- Exit Cleanup ---
def on_closing():
    if client:
        client.close()
    window.destroy()

window.protocol("WM_DELETE_WINDOW", on_closing)
window.mainloop()
