#!/usr/bin/env python3
"""
Main GUI application launcher for the Music Theory Engine.

This script launches the graphical user interface for the music theory engine.
"""

import sys
import os

def main():
    """Launch the GUI application."""
    # Setup logging first
    try:
        from utils.logging_config import setup_logging
        setup_logging()
    except ImportError:
        # Fallback if logging setup fails
        print("Warning: Could not setup logging system")

    try:
        # Ensure proper path setup
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)

        # Add both current and parent directories to path
        for path_dir in [current_dir, parent_dir]:
            if path_dir not in sys.path:
                sys.path.insert(0, path_dir)

        import gui.main_window as main_window_module
        main_window_module.main()
    except ImportError as e:
        print(f"Error importing GUI modules: {e}")
        print("Trying alternative import method...")

        # Alternative: try importing as package
        try:
            import music_engine.gui.main_window as main_window_module
            main_window_module.main()
        except ImportError as e2:
            print(f"Alternative import also failed: {e2}")
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
