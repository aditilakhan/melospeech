# import tkinter as tk
# from tkinter import messagebox
# import subprocess
# import os
# import sys

# if len(sys.argv) > 1:
#     username = sys.argv[1]
# else:
#     username = "Guest"

# SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# DASHBOARD_PATH = os.path.join(SCRIPT_DIR, "..", "dashboard.py")
# MAIN_PATH = os.path.join(SCRIPT_DIR, "..", "main.py")

# def back_to_dashboard():
#     root.destroy()
#     subprocess.Popen([sys.executable, DASHBOARD_PATH, username])

# def logout():
#     if messagebox.askyesno("Logout", "Are you sure you want to logout from the app?"):
#         root.destroy()
#         subprocess.Popen([sys.executable, MAIN_PATH])

# root = tk.Tk()
# root.title("MeloSpeech|App Facts")
# root.geometry("800x500")
# root.configure(bg="#fefefe")
# root.resizable(False, False)

# tk.Label(root, text="📌 Interesting Facts About MeloSpeech", font=("Georgia", 16, "bold"),
#          bg="#fefefe", fg="#2c3e50").pack(pady=20)

# facts = [
#     "🎶 MeloSpeech uses real music and lyrics to boost language learning.",
#     "🧠 Speech Emotion Recognition helps analyze the user's voice tone.",
#     "📊 Your learning progress is saved using MongoDB.",
#     "💡 You can practice pronunciation just like singers do!",
#     "🌟 Fun modules are combined with real ML models for better learning."
# ]

# fact_frame = tk.Frame(root, bg="#fefefe")
# fact_frame.pack(pady=10)

# fact_labels = []

# def show_facts_with_animation(index=0):
#     if index < len(facts):
#         lbl = tk.Label(fact_frame, text=facts[index], font=("Georgia", 11), bg="#fefefe", fg="#34495e",
#                        anchor="w", justify="left")
#         lbl.pack(anchor="w", padx=40, pady=4)
#         fact_labels.append(lbl)
#         root.after(400, show_facts_with_animation, index + 1)

# show_facts_with_animation()

# btn_frame = tk.Frame(root, bg="#fefefe")
# btn_frame.pack(pady=30)

# tk.Button(btn_frame, text="Back to Dashboard", font=("Georgia", 10, "bold"),
#           command=back_to_dashboard, bg="#2980b9", fg="white", width=20,
#           relief="flat", cursor="hand2").grid(row=0, column=0, padx=10)

# tk.Button(btn_frame, text="Logout", font=("Georgia", 10, "bold"),
#           command=logout, bg="#e74c3c", fg="white", width=20,
#           relief="flat", cursor="hand2").grid(row=0, column=1, padx=10)

# tk.Label(root, text="© MeloSpeech.",
#          bg="#2c3e50", fg="white", font=("Georgia", 9)).pack(side="bottom", fill="x")

# root.mainloop()


import tkinter as tk
from tkinter import messagebox
import subprocess
import os
import sys

# Get username from command line arguments or default to "Guest"
if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    username = "Guest"

# Determine script directory and paths to other Python scripts
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DASHBOARD_PATH = os.path.join(SCRIPT_DIR, "..", "dashboard.py")
MAIN_PATH = os.path.join(SCRIPT_DIR, "..", "main.py")

# Function to go back to the dashboard
def back_to_dashboard():
    """
    Destroys the current window and opens the dashboard script.
    """
    root.destroy()
    # Using Popen to run the dashboard script in a new process
    subprocess.Popen([sys.executable, DASHBOARD_PATH, username])

# Function to handle logout
def logout():
    """
    Asks for confirmation before logging out and opening the main script.
    """
    if messagebox.askyesno("Logout", "Are you sure you want to logout from the app?"):
        root.destroy()
        # Using Popen to run the main login script in a new process
        subprocess.Popen([sys.executable, MAIN_PATH])

# Initialize the main Tkinter window
root = tk.Tk()
root.title("MeloSpeech | Facts")
root.geometry("800x500")
root.configure(bg="#fefefe")  # Light background
root.resizable(False, False)  # Disable resizing

# Header Label
tk.Label(root, text="📌 Interesting Facts About Music & Speech", font=("Georgia", 16, "bold"),
         bg="#fefefe", fg="#2c3e50").pack(pady=20)

# Updated facts about Music & Speech
facts = [
    "🎶 Music engages nearly all areas of the brain, including those involved in emotion, memory, and motor control.",
    "🗣️ Speech is a complex motor skill, involving over 100 muscles from the diaphragm to the lips and tongue.",
    "👂 Both music and speech rely on our ability to perceive subtle variations in pitch, rhythm, and timbre.",
    "🌍 While language itself is universal, the specific sounds (phonemes) used in speech vary greatly across cultures.",
    "🧠 Learning to play a musical instrument can enhance cognitive skills, including memory, problem-solving, and spatial reasoning.",
    "👶 Infants develop a preference for their native language's rhythm and intonation patterns even before they understand words.",
    "🎤 Singing in a choir can synchronize heart rates among participants, fostering a sense of community and well-being."
]

# Frame to hold the animated facts
fact_frame = tk.Frame(root, bg="#fefefe")
fact_frame.pack(pady=10, padx=40, fill="x") # Added padx and fill for better layout

fact_labels = [] # List to keep track of fact labels

# Function to display facts with a staggered animation
def show_facts_with_animation(index=0):
    """
    Displays each fact sequentially with a delay, creating an animation effect.
    """
    if index < len(facts):
        lbl = tk.Label(fact_frame, text=f"▪ {facts[index]}", font=("Georgia", 11), bg="#fefefe", fg="#34495e",
                       anchor="w", justify="left", wraplength=700) # Added bullet point and wraplength
        lbl.pack(anchor="w", pady=4)
        fact_labels.append(lbl)
        root.after(600, show_facts_with_animation, index + 1) # Adjust delay as needed

# Start the fact animation
show_facts_with_animation()

# Frame for buttons
btn_frame = tk.Frame(root, bg="#fefefe")
btn_frame.pack(pady=30)

# Back to Dashboard Button
tk.Button(btn_frame, text="Back to Dashboard", font=("Georgia", 10, "bold"),
          command=back_to_dashboard, bg="#2980b9", fg="white", width=20,
          relief="flat", cursor="hand2", bd=0, highlightthickness=0).grid(row=0, column=0, padx=10)

# Logout Button
tk.Button(btn_frame, text="Logout", font=("Georgia", 10, "bold"),
          command=logout, bg="#e74c3c", fg="white", width=20,
          relief="flat", cursor="hand2", bd=0, highlightthickness=0).grid(row=0, column=1, padx=10)

# Footer Label
tk.Label(root, text="© MeloSpeech.",
         bg="#2c3e50", fg="white", font=("Georgia", 9)).pack(side="bottom", fill="x")

# Start the Tkinter event loop
root.mainloop()

