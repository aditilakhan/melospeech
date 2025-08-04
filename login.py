import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk # Keep this if you plan to use images later, though not used in the current GUI
import os
import subprocess
import sys

# --- MongoDB Integration ---
try:
    import pymongo
    from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

    db_client = None
    users_collection = None
    DATABASE_NAME = "melospeech_db"
    USERS_COLLECTION_NAME = "users"

    def connect_to_mongodb_for_app():
        """
        Attempts to establish a connection to MongoDB.
        Displays error messages if connection fails.
        """
        global db_client, users_collection
        try:
            # Attempt to connect to MongoDB with a timeout
            client = pymongo.MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=5000)
            # The ping command is a lightweight way to check if the server is available
            client.admin.command('ping')
            print("MongoDB connection successful for Tkinter app!")
            db_client = client
            db = client[DATABASE_NAME]
            users_collection = db[USERS_COLLECTION_NAME]
            return True
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            messagebox.showerror("Database Connection Error",
                                 f"Could not connect to MongoDB.\nError: {e}")
            return False
        except Exception as e:
            messagebox.showerror("Database Error", f"Unexpected DB error: {e}")
            return False

except ImportError:
    # Handle the case where pymongo is not installed
    messagebox.showerror("Module Error", "pymongo is not installed. Run: pip install pymongo")
    connect_to_mongodb_for_app = None # Disable DB connection functionality
except Exception as e:
    # Catch any other errors during the initial import/setup of pymongo
    messagebox.showerror("Initialization Error", f"Error loading MongoDB functions: {e}")
    connect_to_mongodb_for_app = None # Disable DB connection functionality

def login_user():
    """
    Handles the user login process.
    Authenticates user against MongoDB and navigates to dashboard on success.
    """
    username = username_entry.get().strip()
    password = password_entry.get().strip()

    if not username or not password:
        messagebox.showerror("Error", "Please fill in both Username and Password.")
        return

    if users_collection is not None:
        try:
            user = users_collection.find_one({"username": username})

            if user:
                # In a real app, you would hash the password and compare hashes
                if user["password"] == password:
                    messagebox.showinfo("Login Success", "Welcome to MeloSpeech!")
                    if db_client:
                        db_client.close()
                        print("MongoDB connection closed on successful login.")

                    window.destroy()
                    try:
                        # Construct the path to dashboard.py relative to the current script
                        script_dir = os.path.dirname(os.path.abspath(__file__))
                        dashboard_script_path = os.path.join(script_dir, "dashboard.py")
                        # Use subprocess.Popen to run the dashboard script in a new process
                        subprocess.Popen([sys.executable, dashboard_script_path, username])
                    except Exception as e:
                        messagebox.showerror("Launch Error", f"Could not launch dashboard.py: {e}")
                else:
                    messagebox.showerror("Login Failed", "Password does not match!")
                    password_entry.delete(0, tk.END) # Clear password field
            else:
                # Username not found
                response = messagebox.askyesno("Login Failed", "Username not found! Would you like to create a new account?")
                if response:
                    if db_client:
                        db_client.close()
                    window.destroy()
                    os.system("python register.py") # Navigate to registration screen
                else:
                    username_entry.delete(0, tk.END)
                    password_entry.delete(0, tk.END)

        except Exception as e:
            messagebox.showerror("Database Error", f"An error occurred during login: {e}")
            # Attempt to reconnect if a database error occurs
            if connect_to_mongodb_for_app():
                messagebox.showinfo("Reconnection", "Reconnected to MongoDB. Try again.")
    else:
        # If MongoDB connection was not established initially
        messagebox.showerror("Database Error", "MongoDB is not connected.")
        # Attempt to reconnect and inform the user to try again
        if connect_to_mongodb_for_app():
            messagebox.showinfo("Reconnection", "Reconnected to MongoDB. Try again.")


# --- Navigation Functions ---
def back_to_welcome():
    """Closes the current window and navigates back to the welcome screen."""
    if db_client:
        db_client.close()
        print("MongoDB connection closed on navigating back.")
    window.destroy()
    os.system('python main.py')

def open_register():
    """Closes the current window and navigates to the registration screen."""
    if db_client:
        db_client.close()
        print("MongoDB connection closed on navigating to register.")
    window.destroy()
    os.system('python register.py')

# --- Main Tkinter Window Setup ---
window = tk.Tk()
window.title("MeloSpeech|Login")
window.geometry("800x500")
window.configure(bg="#f0f2f5") # Light grey background for the main window
window.resizable(False, False) # Fixed window size

# Configure grid weights for responsive panel sizing
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1, minsize=260) # Left panel
window.grid_columnconfigure(1, weight=2, minsize=540) # Right panel

# --- Left Panel (Dark background, features) ---
left_panel_frame = tk.Frame(window, bg="#2c3e50") # Dark blue background
left_panel_frame.grid(row=0, column=0, sticky="nsew") # Fills its grid cell

# "Get started" text label
tk.Label(left_panel_frame, text="Get started with personalized\nlanguage learning!",
         font=("Georgia", 14), fg="#ecf0f1", bg="#2c3e50",
         wraplength=220, justify='left'
).pack(pady=(60, 30), padx=20, anchor='nw')

feature_font = ("Georgia", 11, "bold")
feature_text_color = "#ecf0f1"

features_container = tk.Frame(left_panel_frame, bg="#2c3e50")
features_container.pack(pady=15, padx=20, fill='x', anchor='center')

def create_feature_label(parent, icon, text):
    """Helper function to create a feature item with an icon and text."""
    frame = tk.Frame(parent, bg="#2c3e50")
    frame.pack(pady=10, fill='x', anchor='w')
    tk.Label(frame, text=icon, font=("Georgia", 18), bg="#2c3e50", fg="white").pack(side='left', padx=(0, 8))
    tk.Label(frame, text=text, font=feature_font,
             bg="#2c3e50", fg=feature_text_color, wraplength=180,
             justify='left').pack(side='left', anchor='w')

# Create feature labels (corrected to include icons)
create_feature_label(features_container, "🎤", "Improve pronunciation with AI feedback.")
create_feature_label(features_container, "🎵", "Boost vocabulary with engaging music exercises.")
create_feature_label(features_container, "📈", "Track your progress and stay motivated.")

# --- Right Panel (White background, login form) ---
right_panel_frame = tk.Frame(window, bg="white") # White background
right_panel_frame.grid(row=0, column=1, sticky="nsew") # Fills its grid cell

# Configure grid for right panel content (top, middle, bottom sections)
right_panel_frame.grid_rowconfigure(0, weight=0) # For "Don't have an account?"
right_panel_frame.grid_rowconfigure(1, weight=1) # For the main form (to allow vertical centering)
right_panel_frame.grid_rowconfigure(2, weight=0) # For potential bottom padding/elements
right_panel_frame.grid_columnconfigure(0, weight=1) # Center content horizontally

# "Don't have an account?" section
dont_have_account_frame = tk.Frame(right_panel_frame, bg="white")
dont_have_account_frame.grid(row=0, column=0, sticky='ne', padx=15, pady=15) # Top-right alignment

tk.Label(dont_have_account_frame, text="Don't have an account?", font=("Georgia", 9), bg="white",
         fg="#666666").pack(side="left")
tk.Button(dont_have_account_frame, text="Sign up",
          font=("Georgia", 9, "bold", "underline"),
          fg="#1976d2", bg="white", bd=0, cursor="hand2",
          command=open_register).pack(side="left", padx=3)


def create_input(label_text, parent_frame, show_char=None):
    """Helper function to create a label-entry pair."""
    input_pair_frame = tk.Frame(parent_frame, bg='white')
    input_pair_frame.pack(pady=5, fill='x', anchor='center') # Pack the input pair frame itself
    
    # Configure grid for label and entry within the input_pair_frame
    # Use column weights to push label and entry towards the center
    input_pair_frame.grid_columnconfigure(0, weight=1) # Left spacer
    input_pair_frame.grid_columnconfigure(1, weight=0) # Label column
    input_pair_frame.grid_columnconfigure(2, weight=0) # Entry column
    input_pair_frame.grid_columnconfigure(3, weight=1) # Right spacer

    tk.Label(input_pair_frame, text=label_text, bg='white',
             font=("Georgia", 9), anchor='e' # Right-align text in label
    ).grid(row=0, column=1, sticky='e', padx=(0, 5)) # Place label in column 1, stick to east

    entry = tk.Entry(input_pair_frame, show=show_char,
                     font=("Georgia", 9),
                     relief=tk.SOLID, bd=1,
                     highlightbackground="#d0d0d0",
                     highlightcolor="#1976d2",
                     highlightthickness=1, width=30)
    entry.grid(row=0, column=2, sticky='w', padx=(5, 0)) # Place entry in column 2, stick to west

    return entry

# Container for all form fields (inputs and buttons)
form_fields_container = tk.Frame(right_panel_frame, bg='white')
# This frame will contain the "Welcome user" label, input fields and buttons.
# It's placed in row 1 of the right_panel_frame, allowing it to be vertically centered.
form_fields_container.grid(row=1, column=0, sticky='nsew', pady=(15, 5), padx=50)
form_fields_container.grid_rowconfigure(0, weight=1) # Top padding
form_fields_container.grid_columnconfigure(0, weight=1) # Left/right padding for centering

# "Welcome user you can Login now!" Title
tk.Label(form_fields_container, text="Welcome user you can Login now!",
         font=("Georgia", 18, "bold"), fg="#333333",
         bg='white').pack(pady=(50, 10)) # Adjusted pady to push content down

# Create input fields using the helper function
username_entry = create_input("Username:", form_fields_container)
password_entry = create_input("Password:", form_fields_container, show_char="*")

# Login Button
tk.Button(form_fields_container, text="Login", bg="#1976d2", fg="white",
          font=("Georgia", 11, "bold"), width=25, height=1, relief=tk.FLAT, bd=0,
          activebackground="#1565c0", command=login_user).pack(pady=(15, 5))

# Back Button
tk.Button(form_fields_container, text="Back", bg="#190E41", fg="white",
          font=("Georgia", 10), width=20, height=1, relief=tk.FLAT, bd=0,
          activebackground="#888888", command=back_to_welcome).pack(pady=(5, 15))

# --- Initial MongoDB Connection Check ---
if connect_to_mongodb_for_app():
    print("Connected to MongoDB at startup.")
else:
    print("Failed to connect to MongoDB.")

# --- Window Closing Protocol ---
def on_closing():
    """
    Handles actions to perform when the Tkinter window is closed,
    such as closing the MongoDB connection.
    """
    if db_client:
        db_client.close()
        print("MongoDB connection closed on exit.")
    window.destroy()

# Set the protocol for when the window's close button is clicked
window.protocol("WM_DELETE_WINDOW", on_closing)

# Start the Tkinter event loop
window.mainloop()
