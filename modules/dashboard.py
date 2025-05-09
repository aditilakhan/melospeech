import tkinter as tk
from tkinter import messagebox

def show_dashboard():
    dashboard_win = tk.Tk()
    dashboard_win.title("Dashboard | MeloSpeech")
    dashboard_win.geometry("1000x650")
    dashboard_win.configure(bg="#F7F9FC")
    dashboard_win.resizable(False, False)

    # --- Top navbar ---
    navbar = tk.Frame(dashboard_win, bg="#0B60B0", height=50)
    navbar.pack(fill=tk.X, side=tk.TOP)

    nav_buttons = [
        ("🏠 Home", lambda: messagebox.showinfo("Home", "Go Home")),
        ("📊 Dashboard", lambda: messagebox.showinfo("Dashboard", "Already here")),
        ("📈 Progress", lambda: messagebox.showinfo("Progress", "See your progress")),
        ("🔓 Logout", dashboard_win.destroy),
    ]

    for text, command in nav_buttons:
        btn = tk.Button(navbar, text=text, font=("Segoe UI", 12, "bold"), bg="#0B60B0",
                        fg="white", bd=0, activebackground="#40A2D8", activeforeground="white",
                        padx=20, pady=10, command=command, cursor="hand2")
        btn.pack(side=tk.LEFT, padx=10)

    # --- Main Content ---
    main_frame = tk.Frame(dashboard_win, bg="#F7F9FC")
    main_frame.pack(expand=True)

    welcome_label = tk.Label(main_frame, text="Welcome to MeloSpeech Dashboard!",
                             font=("Segoe UI", 26, "bold"), bg="#F7F9FC", fg="#0B60B0")
    welcome_label.pack(pady=30)

    features_frame = tk.Frame(main_frame, bg="#F7F9FC")
    features_frame.pack(pady=10)

    feature_buttons = [
        ("🎙️ Speech Practice", lambda: messagebox.showinfo("Feature", "Practice your speech")),
        ("🎵 Music Learning", lambda: messagebox.showinfo("Feature", "Learn through music")),
        ("🧠 Cognitive Exercises", lambda: messagebox.showinfo("Feature", "Sharpen your skills")),
        ("🎯 Challenge Mode", lambda: messagebox.showinfo("Feature", "Daily Challenges")),
        ("📅 Training Schedule", lambda: messagebox.showinfo("Feature", "Manage your sessions")),
    ]

    button_widgets = []

    def on_enter(e):
        e.widget.config(bg="#40A2D8", relief="raised")

    def on_leave(e):
        e.widget.config(bg="#0B60B0", relief="flat")

    def animate_buttons(index=0):
        if index < len(button_widgets):
            button_widgets[index].pack(pady=12)
            dashboard_win.after(100, animate_buttons, index + 1)

    for text, command in feature_buttons:
        btn = tk.Button(features_frame, text=text, width=30, height=2, font=("Segoe UI", 14, "bold"),
                        bg="#0B60B0", fg="white", bd=0, activebackground="#40A2D8",
                        activeforeground="white", cursor="hand2", command=command)
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        btn.configure(highlightthickness=0, borderwidth=0)
        btn.configure(relief="flat")
        button_widgets.append(btn)

    dashboard_win.after(500, animate_buttons)

    # --- Bottom Links for Settings & Help ---
    bottom_frame = tk.Frame(dashboard_win, bg="#F7F9FC")
    bottom_frame.pack(side=tk.BOTTOM, pady=10)

    settings_btn = tk.Button(bottom_frame, text="⚙️ Settings", font=("Segoe UI", 10),
                              bg="#F7F9FC", fg="#0B60B0", bd=0, cursor="hand2",
                              activebackground="#F7F9FC", activeforeground="#40A2D8",
                              command=lambda: messagebox.showinfo("Settings", "App Settings"))
    settings_btn.pack(side=tk.LEFT, padx=10)

    help_btn = tk.Button(bottom_frame, text="❓ Help & Support", font=("Segoe UI", 10),
                         bg="#F7F9FC", fg="#0B60B0", bd=0, cursor="hand2",
                         activebackground="#F7F9FC", activeforeground="#40A2D8",
                         command=lambda: messagebox.showinfo("Help", "Get Help"))
    help_btn.pack(side=tk.LEFT, padx=10)

    dashboard_win.mainloop()
