# speech_practice.py

import tkinter as tk
from tkinter import messagebox
import speech_recognition as sr

def open_speech_practice():
    window = tk.Tk()
    window.title("Speech Practice - MeloSpeech")
    window.geometry("500x400")
    window.configure(bg="#f0f8ff")  # Light background

    title = tk.Label(window, text="Speech Practice", font=("Arial", 18, "bold"), bg="#f0f8ff", fg="#0b5394")
    title.pack(pady=20)

    output_text = tk.Text(window, height=10, width=50, wrap='word')
    output_text.pack(pady=20)

    def recognize_speech():
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            messagebox.showinfo("Info", "Please speak now...")
            try:
                audio = recognizer.listen(source, timeout=5)
                text = recognizer.recognize_google(audio)
                output_text.delete(1.0, tk.END)
                output_text.insert(tk.END, text)
            except sr.UnknownValueError:
                messagebox.showerror("Error", "Could not understand audio.")
            except sr.RequestError:
                messagebox.showerror("Error", "Could not request results, check Internet.")
            except sr.WaitTimeoutError:
                messagebox.showerror("Error", "Listening timed out, try again.")

    record_btn = tk.Button(window, text="🎙️ Start Recording", command=recognize_speech, font=("Arial", 12), bg="#0b5394", fg="white", padx=10, pady=5)
    record_btn.pack()

    window.mainloop()

# For testing standalone
if __name__ == "__main__":
    open_speech_practice()
