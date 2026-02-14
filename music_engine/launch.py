#!/usr/bin/env python3
"""
Launcher script for Music Theory Engine.

This script properly sets up the Python path and launches the GUI application.
"""

import sys
import os

def main():
    """Launch the Music Theory Engine GUI."""
    # Try to run the GUI
    try:
        from main_gui import main as gui_main
        gui_main()
    except ImportError as e:
        print(f"Error importing GUI modules: {e}")
        print("Please make sure all required packages are installed:")
        print("pip install customtkinter pillow")
        print("Optional: pip install numpy pyaudio  # For audio playback")
        sys.exit(1)
    except Exception as e:
        print(f"Error launching GUI: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()