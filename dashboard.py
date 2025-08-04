import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import os
import random

# Mock load_profile_by_username function for demonstration
# In a real application, this would load user data from a database or file
def load_profile_by_username(username):
    """
    Mocks loading a user profile.
    In a real application, this would fetch data from MongoDB.
    """
    if username:
        # Simulate a successful profile load
        return {"username": username, "email": f"{username}@example.com"}
    return None

# --- User Profile Loading ---
# This part assumes the username is passed as a command-line argument from login.py
if len(sys.argv) > 1:
    username = sys.argv[1]
    profile = load_profile_by_username(username)
    if not profile:
        messagebox.showerror("Login Error", "User profile not found.")
        sys.exit() # Exit if user profile cannot be loaded
else:
    messagebox.showerror("Login Error", "Username not passed. Please log in again.")
    sys.exit() # Exit if username is not provided

# --- Paths Configuration ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MODULES_DIR = os.path.join(SCRIPT_DIR, "modules")
MAIN_PATH = os.path.join(SCRIPT_DIR, "main.py") # Path to your main welcome screen

# --- Dashboard Quotes ---
quotes = [
    "Make your voice heard through learning.",
    "Speak with rhythm, learn with passion.",
    "Express emotion. Enhance communication.",
    "Your voice is your power. Train it!",
    "Tune your speech like music."
]
selected_quote = random.choice(quotes) # Select a random quote for the top bar

# --- Module Navigation Function ---
def open_module_screen(filename):
    """
    Opens a specific module screen by running its Python file as a subprocess.
    Passes the current username to the new module.
    """
    path = os.path.join(MODULES_DIR, filename)
    if not os.path.exists(path):
        messagebox.showerror("Error", f"Module not found: {filename}")
        return
    root.destroy() # Close the current dashboard window
    subprocess.Popen([sys.executable, path, username]) # Open the new module

# --- Logout Function ---
def logout():
    """
    Handles the logout process. Confirms with the user and returns to the main screen.
    """
    if messagebox.askyesno("Logout", "Are you sure you want to logout from the app?"):
        root.destroy() # Close the dashboard window
        subprocess.Popen([sys.executable, MAIN_PATH]) # Go back to the main welcome screen

# --- Main Tkinter Window Setup ---
root = tk.Tk()
root.title("MeloSpeech|Dashboard")
root.geometry("800x500")
root.configure(bg="#f4f6f9") # Light grey background
root.resizable(False, False) # Fixed window size

# --- Sidebar (Left Panel) ---
sidebar = tk.Frame(root, bg="#2c3e50", width=180) # Dark blue sidebar
sidebar.pack(side="left", fill="y")

# MeloSpeech Title in Sidebar
tk.Label(sidebar, text="MeloSpeech", font=("Segoe UI", 16, "bold"),
         fg="white", bg="#2c3e50", pady=20).pack()

def sidebar_button(text, icon, command):
    """Helper function to create a styled sidebar button."""
    frame = tk.Frame(sidebar, bg="#2c3e50")
    frame.pack(fill="x", pady=3)

    btn = tk.Button(
        frame, text=f"{icon}  {text}", font=("Segoe UI", 11),
        bg="#2c3e50", fg="white", activebackground="#34495e", # Darker blue on hover
        relief="flat", anchor="w", padx=20, pady=10,
        width=20, bd=0, cursor="hand2", command=command
    )
    btn.pack(fill="x")
    # Add hover effects
    btn.bind("<Enter>", lambda e: btn.config(bg="#34495e"))
    btn.bind("<Leave>", lambda e: btn.config(bg="#2c3e50"))

# Sidebar Buttons with Icons
sidebar_button("Profile", "👤", lambda: open_module_screen("profile_settings_gui.py"))
sidebar_button("Notifications", "🔔", lambda: open_module_screen("notifications_gui.py"))
sidebar_button("Help & FAQs", "❓", lambda: open_module_screen("help_faqs_gui.py"))

# Logout Button in Sidebar (placed at the bottom of the sidebar)
tk.Button(sidebar, text=" ➡️ Logout", command=logout,
          font=("Segoe UI", 11), bg="#e74c3c", fg="white", # Red background for logout
          relief="flat", cursor="hand2", anchor="w", padx=20, pady=10,
          width=20, bd=0, activebackground="#c0392b" # Darker red on hover
).pack(side="bottom", fill="x", pady=(20, 10)) # Padded from top and bottom within sidebar

# --- Top Frame (Quote) ---
top_frame = tk.Frame(root, bg="#e8eff8", height=50) # Light blue-grey top bar
top_frame.pack(fill="x")
top_frame.pack_propagate(False) # Prevent frame from resizing to fit content

tk.Label(top_frame, text=selected_quote, font=("Segoe UI", 10, "italic"),
         fg="#2c3e50", bg="#e8eff8").pack(pady=12) # Centered quote

# --- Main Content Frame (Feature Grid) ---
main_frame = tk.Frame(root, bg="#f4f6f9") # Light grey background for main content
main_frame.pack(expand=True, fill="both")

def feature_button(parent, text, icon, bg, command):
    """Helper function to create a styled feature button with an icon."""
    btn = tk.Button(
        parent,
        text=f"{icon}\n{text}", # Icon on top, text below
        font=("Segoe UI", 11, "bold"),
        bg=bg, fg="white", activebackground=bg,
        width=30, height=4, wraplength=260, # Wraplength for multi-line text
        relief="flat", bd=0, cursor="hand2", command=command,
        compound="top", # Place image/icon on top of text
        padx=10, pady=10 # Internal padding for content
    )
    # Add hover effects
    btn.bind("<Enter>", lambda e: btn.config(bg=lighten_color(bg, 20))) # Lighten on hover
    btn.bind("<Leave>", lambda e: btn.config(bg=bg))
    return btn

def lighten_color(hex_color, percent):
    """Lightens a hex color by a given percentage."""
    hex_color = hex_color.lstrip('#')
    rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    lightened_rgb = [min(255, int(c * (1 + percent / 100.0))) for c in rgb]
    return '#%02x%02x%02x' % tuple(lightened_rgb)


grid = tk.Frame(main_frame, bg="#f4f6f9")
grid.pack(pady=20) # Padding around the entire grid of buttons

# Configure grid columns for even distribution
grid.grid_columnconfigure((0, 1), weight=1, pad=20) # Pad between columns

# Feature Buttons with Icons and specific colors
feature_button(grid, "Speech Emotion Recognition\nAnalyze Emotional Tone", "🗣️", "#27ae60", # Green
               lambda: open_module_screen("speech_emotion_gui.py")).grid(row=0, column=0, padx=10, pady=10)

feature_button(grid, "Lyrics Sentiment Analysis\nUnderstand Mood of Lyrics", "🎶", "#2980b9", # Blue
               lambda: open_module_screen("lyric_sentiment_gui.py")).grid(row=0, column=1, padx=10, pady=10)

feature_button(grid, "Pronunciation Practice\nVoice Accuracy Check", "🎤", "#f1c40f", # Yellow
               lambda: open_module_screen("pronunciation_gui.py")).grid(row=1, column=0, padx=10, pady=10)

feature_button(grid, "Vocabulary Builder\nLearn and Track Words", "📚", "#8e44ad", # Purple
               lambda: open_module_screen("vocabulary_gui.py")).grid(row=1, column=1, padx=10, pady=10)

feature_button(grid, "Progress Tracker\nTrack Your Learning", "📈", "#16a085", # Teal
               lambda: open_module_screen("progress_gui.py")).grid(row=2, column=0, padx=10, pady=10)

feature_button(grid, "Facts About the App\nLearn Interesting Insights", "💡", "#e67e22", # Orange
               lambda: open_module_screen("facts_gui.py")).grid(row=2, column=1, padx=10, pady=10)

# --- Copyright Label (Bottom) ---
# This label is packed directly into the root window to span its full width
tk.Label(root, text="© MeloSpeech.",
         bg="#2c3e50", fg="white", font=("Segoe UI", 9)).pack(side="bottom", fill="x")

# Start the Tkinter event loop
root.mainloop()
