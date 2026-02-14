#!/usr/bin/env python3
"""
Simple build script to create executable.
"""

import os
import subprocess
import sys

def build_exe():
    """Build the executable using PyInstaller."""
    print("Building Music Theory Engine executable...")
    print("=" * 50)

    # Check if we're in the right directory
    if not os.path.exists('standalone_demo.py'):
        print("ERROR: standalone_demo.py not found.")
        return False

    # Check if PyInstaller is installed
    try:
        import PyInstaller
        print("PyInstaller found")
    except ImportError:
        print("ERROR: PyInstaller not found. Install with: pip install pyinstaller")
        return False

    # Clean previous builds
    import shutil
    for dir_name in ['build', 'dist']:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"Cleaned {dir_name}/")

    # PyInstaller command for standalone demo with fretboard
    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--name=MusicTheoryEngine_Fretboard",
        "standalone_demo.py"
    ]

    print(f"Running: {' '.join(cmd)}")

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            print("PyInstaller completed successfully")

            # Check if executable was created
            exe_path = os.path.join("dist", "MusicTheoryEngine.exe")
            if os.path.exists(exe_path):
                print(f"Executable created: {exe_path}")
                print("\nBuild successful!")
                print("You can find the executable in the 'dist' folder.")
                return True
            else:
                print("ERROR: Executable not found after build")
                return False
        else:
            print("ERROR: PyInstaller failed")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            return False

    except Exception as e:
        print(f"ERROR: Build failed with exception: {e}")
        return False

if __name__ == "__main__":
    success = build_exe()
    sys.exit(0 if success else 1)
