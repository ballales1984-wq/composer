#!/usr/bin/env python3
"""
Standalone launcher for Music Theory Engine.

This script properly sets up the Python path and launches the application.
"""

import sys
import os

def main():
    """Launch Music Theory Engine."""
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Add the music_engine directory to Python path
    music_engine_dir = os.path.join(script_dir, 'music_engine')
    if music_engine_dir not in sys.path:
        sys.path.insert(0, music_engine_dir)

    # Now import and run the main module
    try:
        from music_engine.main_gui import main
        main()
    except ImportError as e:
        print(f"Import error: {e}")
        print("Trying alternative import...")

        # Alternative: run as module
        try:
            import subprocess
            result = subprocess.run([sys.executable, "-m", "music_engine"],
                                  cwd=script_dir)
            return result.returncode
        except Exception as e2:
            print(f"Alternative import also failed: {e2}")
            return 1

    return 0

if __name__ == "__main__":
    exit(main())