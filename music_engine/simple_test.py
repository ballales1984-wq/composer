#!/usr/bin/env python3
"""
Simple test to launch the GUI application.
"""

def main():
    """Launch the GUI."""
    print("Launching Music Theory Engine GUI...")
    print("If the GUI doesn't open, check the error messages above.")

    try:
        from gui.main_window import main as gui_main
        gui_main()
    except ImportError as e:
        print(f"Import error: {e}")
        print("Make sure all dependencies are installed:")
        print("pip install customtkinter pillow")
    except Exception as e:
        print(f"Error launching GUI: {e}")

if __name__ == "__main__":
    main()
