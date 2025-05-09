import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.welcome_screen import show_welcome_screen

# 👉 Correct call without passing anything
show_welcome_screen()
