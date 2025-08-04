import subprocess
import sys
import os

# This file launches the main Streamlit application
# which is located in the ui folder.

# Get the directory of the current script (root of the project)
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to main_ui.py in the ui subdirectory
main_ui_path = os.path.join(script_dir, "ui", "main_ui.py")

# Run the main_ui.py script
subprocess.run([sys.executable, "-m", "streamlit", "run", main_ui_path])