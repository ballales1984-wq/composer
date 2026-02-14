#!/usr/bin/env python3
"""
Check if GUI components can be imported successfully.
"""

import sys
import os

# Setup path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

def check_imports():
    """Check all GUI imports."""
    print("Checking GUI imports...")

    try:
        import customtkinter as ctk
        print("+ CustomTkinter available")
    except ImportError:
        print("X CustomTkinter not available")
        return False

    try:
        from gui.main_window import MusicTheoryGUI
        print("+ Main window import successful")
    except ImportError as e:
        print(f"X Main window import failed: {e}")
        return False

    try:
        # Test creating a simple instance (without showing window)
        app = MusicTheoryGUI()
        print("+ GUI instance created successfully")
        app.destroy()  # Close immediately
        return True
    except Exception as e:
        print(f"X GUI creation failed: {e}")
        return False

if __name__ == "__main__":
    success = check_imports()
    if success:
        print("\nSUCCESS: GUI is working! The application should open correctly.")
        print("Try running: python main_gui.py")
    else:
        print("\nFAILED: GUI has issues. Check the error messages above.")
    sys.exit(0 if success else 1)
