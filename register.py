import tkinter as tk
from tkinter import messagebox
import re
import os
import datetime
from PIL import Image, ImageTk 

# --- MongoDB Connection Setup ---
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
                                  f"Could not connect to MongoDB server.\nPlease ensure MongoDB is running.\nError: {e}")
            return False
        except Exception as e:
            messagebox.showerror("Database Error", f"An unexpected error occurred during DB connection: {e}")
            return False

except ImportError:
    # Handle the case where pymongo is not installed
    messagebox.showerror("Module Error", "pymongo is not installed. Please run 'pip install pymongo'")
    connect_to_mongodb_for_app = None # Disable DB connection functionality
except Exception as e:
    # Catch any other errors during the initial import/setup of pymongo
    messagebox.showerror("Initialization Error", f"Error initializing MongoDB connection functions: {e}")
    connect_to_mongodb_for_app = None # Disable DB connection functionality

# --- Validation Functions ---
def validate_registration(username, email, password, confirm_password):
    """
    Validates the registration input fields.
    Returns an error message string if validation fails, otherwise "Valid".
    """
    if not username or not email or not password or not confirm_password:
        return "All fields are required."

    # Username validation: at least 3 characters, letters or numbers only
    if not re.match(r'^[A-Za-z0-9]{3,}$', username):
        return "Username must be at least 3 characters (letters or numbers)."

    # Email validation: basic regex pattern
    email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w{2,4}$'
    if not re.match(email_pattern, email):
        return "Enter a valid email address."

    # Password validation: at least 6 characters and contains at least one digit
    if len(password) < 6 or not any(char.isdigit() for char in password):
        return "Password must be at least 6 characters long and contain a number."

    # Confirm password validation
    if password != confirm_password:
        return "Passwords do not match."

    return "Valid"

# --- Registration Logic ---
def register_user():
    """
    Handles the user registration process.
    Validates input, checks for existing users, and saves to MongoDB.
    """
    username = username_entry.get().strip()
    email = email_entry.get().strip()
    password = password_entry.get().strip()
    confirm_password = confirm_password_entry.get().strip()

    result = validate_registration(username, email, password, confirm_password)
    if result == "Valid":
        if users_collection is not None:
            user_data = {
                "username": username,
                "email": email,
                "password": password, # In a real app, hash this password!
                "registration_date": datetime.datetime.now(),
                "active": True
            }
            try:
                # Check if username or email already exists in the database
                if users_collection.find_one({"username": username}):
                    messagebox.showerror("Registration Error", "Username already exists.")
                    return
                if users_collection.find_one({"email": email}):
                    messagebox.showerror("Registration Error", "Email already registered.")
                    return

                # Insert the new user data into the collection
                inserted_id = users_collection.insert_one(user_data).inserted_id
                messagebox.showinfo("Success", f"Registration Successful! User ID: {inserted_id}\nPlease login.")
                window.destroy()
                # Navigate to the login screen
                os.system('python login.py')
            except Exception as e:
                messagebox.showerror("Database Error", f"Error saving user to database: {e}")
        else:
            # If MongoDB connection was not established initially
            messagebox.showerror("Database Error", "MongoDB connection not established. Cannot register user.")
            # Attempt to reconnect and inform the user to try again
            if connect_to_mongodb_for_app():
                messagebox.showinfo("Reconnection", "Attempted to reconnect to MongoDB. Please try registering again.")
    else:
        # Display validation errors
        messagebox.showerror("Validation Error", result)

# --- Navigation Functions ---
def back_to_welcome():
    """Closes the current window and navigates back to the welcome screen."""
    if db_client:
        db_client.close()
        print("MongoDB connection closed on navigating back.")
    window.destroy()
    os.system('python main.py')

def open_login():
    """Closes the current window and navigates to the login screen."""
    if db_client:
        db_client.close()
        print("MongoDB connection closed on navigating to login.")
    window.destroy()
    os.system('python login.py')

# --- Main Tkinter Window Setup ---
window = tk.Tk()
window.title("MeloSpeech|Register")
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
          wraplength=220, justify='left').pack(pady=(60, 30), padx=20, anchor='nw')

# Container for feature list
features_container = tk.Frame(left_panel_frame, bg="#2c3e50")
features_container.pack(pady=15, padx=20, fill='x', anchor='center')

def create_feature_label(parent, icon, text):
    """Helper function to create a feature item with an icon and text."""
    frame = tk.Frame(parent, bg="#2c3e50")
    frame.pack(pady=10, fill='x', anchor='w') # Pack each feature frame
    tk.Label(frame, text=icon, font=("Georgia", 18), bg="#2c3e50", fg="white").pack(side='left', padx=(0, 8))
    tk.Label(frame, text=text, font=("Georgia", 11, "bold"), bg="#2c3e50", fg="#ecf0f1", wraplength=180, justify='left').pack(side='left', anchor='w')

# Create feature labels
create_feature_label(features_container, "🎤", "Improve pronunciation with AI feedback.")
create_feature_label(features_container, "🎵", "Boost vocabulary with engaging music exercises.")
create_feature_label(features_container, "📈", "Track your progress and stay motivated.")

# --- Right Panel (White background, registration form) ---
right_panel_frame = tk.Frame(window, bg="#ffffff") # White background
right_panel_frame.grid(row=0, column=1, sticky="nsew") # Fills its grid cell

# Configure grid for right panel content (top, middle, bottom sections)
right_panel_frame.grid_rowconfigure(0, weight=0) # For "Already have an account?"
right_panel_frame.grid_rowconfigure(1, weight=1) # For the main form (to allow vertical centering)
right_panel_frame.grid_rowconfigure(2, weight=0) # For potential bottom padding/elements
right_panel_frame.grid_columnconfigure(0, weight=1) # Center content horizontally

# "Already have an account?" section
already_account_frame = tk.Frame(right_panel_frame, bg="white")
already_account_frame.grid(row=0, column=0, sticky='ne', padx=15, pady=15) # Top-right alignment

tk.Label(already_account_frame, text="Already have an account?", font=("Georgia", 9), bg="white", fg="#666666").pack(side="left")
tk.Button(already_account_frame, text="Sign in", font=("Georgia", 9, "bold", "underline"), fg="#1976d2", bg="white", bd=0, cursor="hand2", command=open_login).pack(side="left", padx=3)

# "Register Now" Title
tk.Label(right_panel_frame, text="Register Now", font=("Georgia", 24, "bold"), bg="white", fg="#333333").grid(row=1, column=0, pady=(20, 20), sticky='n') # Placed in row 1, top

def create_input(label_text, parent_frame, row_num, column_num, show_char=None):
    """Helper function to create a label-entry pair using grid for better alignment."""
    tk.Label(parent_frame, text=label_text, bg='white', font=("Georgia", 9), anchor='e').grid(row=row_num, column=column_num, padx=(0, 5), pady=5, sticky='e')
    entry = tk.Entry(parent_frame, show=show_char, font=("Georgia", 9), relief=tk.SOLID, bd=1)
    entry.grid(row=row_num, column=column_num + 1, padx=(5, 0), pady=5, sticky='ew') # 'ew' makes it expand horizontally
    return entry

# Container for all form fields (inputs and buttons)
form_fields_container = tk.Frame(right_panel_frame, bg='white')
form_fields_container.grid(row=1, column=0, sticky='nsew', pady=(90, 5), padx=50) 

# Center the content within form_fields_container and make entries expand
form_fields_container.grid_columnconfigure(0, weight=1) # Column for labels
form_fields_container.grid_columnconfigure(1, weight=3) # Column for entries (given more weight to expand)

# Create input fields using the helper function with specific row/column
username_entry = create_input("Username:", form_fields_container, 0, 0)
email_entry = create_input("Email:", form_fields_container, 1, 0)
password_entry = create_input("Password:", form_fields_container, 2, 0, show_char="*")
confirm_password_entry = create_input("Confirm Pass:", form_fields_container, 3, 0, show_char="*")

# Create Account Button (placed in a new row after input fields)
tk.Button(form_fields_container, text="Create Account", bg="#1976d2", fg="white",
           font=("Georgia", 11, "bold"), width=25, height=1, relief=tk.FLAT, bd=0,
           activebackground="#1565c0", command=register_user).grid(row=4, column=0, columnspan=2, pady=(15, 5))

# Back Button (placed in a new row)
tk.Button(form_fields_container, text="Back", bg="#190E41", fg="white",
           font=("Georgia", 10), width=20, height=1, relief=tk.FLAT, bd=0,
           activebackground="#888888", command=back_to_welcome).grid(row=5, column=0, columnspan=2, pady=(5, 15))


# --- Initial MongoDB Connection Check ---
if connect_to_mongodb_for_app():
    print("Application successfully connected to MongoDB on startup.")
else:
    print("Application failed to connect to MongoDB on startup. Register functionality may be limited.")

# --- Window Closing Protocol ---
def on_closing():
    """
    Handles actions to perform when the Tkinter window is closed,
    such as closing the MongoDB connection.
    """
    if db_client:
        db_client.close()
        print("MongoDB connection closed on application exit.")
    window.destroy()

# Set the protocol for when the window's close button is clicked
window.protocol("WM_DELETE_WINDOW", on_closing)

# Start the Tkinter event loop
window.mainloop()