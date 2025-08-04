import tkinter as tk
from tkinter import messagebox
import sounddevice as sd
import soundfile as sf
import librosa
import numpy as np
import difflib
import os
import sys
from datetime import datetime
from pymongo import MongoClient
import subprocess
import speech_recognition as sr

username = sys.argv[1] 

client = MongoClient("mongodb://localhost:27017/")
db = client["melospeech_db"]
pronounce_col = db["pronunciation_results"]

if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    messagebox.showerror("Login Error", "Username not provided.")
    sys.exit()

def record_audio(duration=4, sample_rate=16000, filename="user_audio.wav"): 
    try:
        messagebox.showinfo("Recording", f"Recording for {duration} seconds. Please speak clearly after clicking OK.")
        audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16') 
        sd.wait()
        sf.write(filename, audio, sample_rate)
        return filename
    except Exception as e:
        messagebox.showerror("Recording Error", f"Failed to record audio: {str(e)}")
        return None

def evaluate_pronunciation():
    expected_text = sentence_entry.get().strip().lower()
    if not expected_text:
        messagebox.showwarning("Input Error", "Please enter a sentence to practice.")
        return

    audio_path = record_audio()
    if not audio_path:
        return

    transcribed_text = ""
    try:
        r = sr.Recognizer()
        with sr.AudioFile(audio_path) as source:
            audio_data = r.record(source)  
      
        transcribed_text = r.recognize_google(audio_data, language="en-US").lower()
        
        # Option 2: Sphinx (offline, but less accurate than Google/Whisper)
        # transcribed_text = r.recognize_sphinx(audio_data).lower()

        # Option 3: Whisper (local model, requires separate setup like 'transformers' or 'openai-whisper')
        # This would involve loading a Whisper model and processing audio with it.
        # Example (conceptual):
        # import whisper
        # model = whisper.load_model("base") # or "small", "medium", etc.
        # result = model.transcribe(audio_path)
        # transcribed_text = result["text"].lower()

    except sr.UnknownValueError:
        messagebox.showerror("Speech Recognition Error", "Could not understand audio. Please try again.")
        result_label.config(text="Spoken: (No speech detected or understood)")
        
        return
    except sr.RequestError as e:
        messagebox.showerror("Speech Recognition Error", f"Could not request results from speech recognition service; {e}")
        return
    except Exception as e:
        messagebox.showerror("General Error", f"An unexpected error occurred during speech recognition: {str(e)}")
        return
    finally:
       
        if os.path.exists(audio_path):
            os.remove(audio_path)

   
    similarity = difflib.SequenceMatcher(None, expected_text, transcribed_text).ratio()
    score = round(similarity * 100, 2)

    result = f"Expected: {expected_text}\nSpoken: {transcribed_text}\nMatch Score: {score}%"
    result_label.config(text=result)

    if score >= 80: 
        messagebox.showinfo("Pronunciation Result", f"Great job! Your pronunciation matched {score}%!")
    elif score >= 50:
        messagebox.showwarning("Pronunciation Result", f"Good effort! Your pronunciation matched {score}%. Try to speak more clearly.")
    else:
        messagebox.showerror("Pronunciation Result", f"Needs improvement. Your pronunciation matched {score}%. Please practice more.")

    try:
        pronounce_col.insert_one({
            "username": username,
            "expected_text": expected_text,
            "transcribed_text": transcribed_text,
            "score_percent": score,
            "timestamp": datetime.now()
        })
        print("Pronunciation result saved to database.") 
    except Exception as e:
        messagebox.showerror("Database Error", f"Failed to save result to database: {str(e)}")

window = tk.Tk()
window.title("Pronunciation Practice")
window.geometry("800x500")
window.configure(bg="#f0f4fc")
window.resizable(False, False)

header = tk.Frame(window, bg="#2c3e50", height=50)
header.pack(fill="x")
tk.Label(header, text="🗣️ Pronunciation Practice", font=("Georgia", 16, "bold"), bg="#2c3e50", fg="white").pack(side="left", padx=20, pady=10)


content = tk.Frame(window, bg="#f0f4fc")
content.pack(pady=20)

tk.Label(content, text="Enter a sentence and record your voice to check pronunciation.",
             font=("Georgia", 12), bg="#f0f4fc").pack(pady=10)

sentence_entry = tk.Entry(content, font=("Georgia", 11), width=60)
sentence_entry.pack(pady=10)

evaluate_btn = tk.Button(content, text="🎙️ Evaluate Pronunciation", font=("Georgia", 11, "bold"),
                             bg="#f39c12", fg="white", width=30, height=2,
                             relief="flat", command=evaluate_pronunciation)
evaluate_btn.pack(pady=10)

result_label = tk.Label(content, text="", font=("Georgia", 11), bg="#f0f4fc", fg="#2c3e50")
result_label.pack(pady=10)

def back_to_dashboard():
    window.destroy()
    subprocess.Popen([sys.executable, "dashboard.py", username])

tk.Button(window, text="Back to Dashboard", bg="#555", fg="white",
             font=("Georgia", 10, "bold"), command=back_to_dashboard).pack(pady=10)


tk.Label(window, text="\u00a9 MeloSpeech", bg="#2c3e50", fg="white", font=("Georgia", 8)).pack(side="bottom", fill="x")

window.mainloop()
