#!/usr/bin/env python3
"""
Build script for creating executable from the Music Theory Engine GUI.

This script uses PyInstaller to create a standalone executable (.exe) file
that can be run on Windows without requiring Python installation.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def build_exe(onefile=False):
    """Build the executable using PyInstaller.

    Args:
        onefile: If True, create single executable file. If False, create directory.
    """
    mode = "single file" if onefile else "directory"
    print(f"Building Music Theory Engine executable ({mode})...")
    print("=" * 60)

    # Check if we're in the right directory
    if not os.path.exists('main_gui.py'):
        print("ERROR: main_gui.py not found. Please run this script from the music_engine directory.")
        return False

    # Check if PyInstaller is installed
    try:
        import PyInstaller
        print("✓ PyInstaller found")
    except ImportError:
        print("ERROR: PyInstaller not found. Install with: pip install pyinstaller")
        return False

    # Create dist directory if it doesn't exist
    dist_dir = Path("dist")
    dist_dir.mkdir(exist_ok=True)

    # Base PyInstaller command with optimizations
    cmd = [
        "pyinstaller",
        "--windowed",  # No console window (for GUI apps)
        "--name=MusicTheoryEngine",
        "--icon=icon.ico" if os.path.exists("icon.ico") else None,
        "--add-data=README.md;.",  # Include documentation
        "--hidden-import=tkinter",  # Hidden import for tkinter
        "--hidden-import=customtkinter",  # Hidden import for CustomTkinter
        "--hidden-import=numpy",  # Hidden import for numpy
        "--hidden-import=PIL",  # Hidden import for Pillow
        "--hidden-import=mido",  # Hidden import for MIDI
        "--exclude-module=matplotlib",  # Exclude unused modules
        "--exclude-module=pandas",  # Exclude unused modules
        "--exclude-module=jupyter",  # Exclude unused modules
        "--exclude-module=notebook",  # Exclude unused modules
        "--exclude-module=ipykernel",  # Exclude unused modules
        "--optimize=1",  # Basic optimization
        "--upx-dir=",  # Try to use UPX for compression
        "app_standalone.py"  # Use standalone app
    ]

    # Add onefile or onedir option
    if onefile:
        cmd.insert(1, "--onefile")  # Single executable file
        print("Mode: Single executable file (slower build, larger size)")
    else:
        cmd.insert(1, "--onedir")   # Directory with executable
        print("Mode: Directory with executable (faster build, smaller size)")

    # Remove None values
    cmd = [arg for arg in cmd if arg is not None]

    print(f"Running command: {' '.join(cmd)}")

    try:
        # Run PyInstaller
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            print("✓ PyInstaller completed successfully")

            # Check if executable directory was created
            exe_dir = dist_dir / "MusicTheoryEngine"
            exe_path = exe_dir / "MusicTheoryEngine.exe"
            if exe_path.exists():
                print(f"✓ Executable created: {exe_path.absolute()}")
                print(f"✓ Executable directory: {exe_dir.absolute()}")

                # Copy additional files
                copy_additional_files(exe_dir)

                # Show file size information
                exe_size = exe_path.stat().st_size
                exe_size_mb = exe_size / (1024 * 1024)
                print(f"Executable size: {exe_size_mb:.1f} MB")

                if not onefile:
                    # Calculate total directory size
                    total_size = sum(f.stat().st_size for f in exe_dir.rglob('*') if f.is_file())
                    total_size_mb = total_size / (1024 * 1024)
                    print(f"Total directory size: {total_size_mb:.1f} MB")

                print("\n" + "=" * 60)
                print("BUILD SUCCESSFUL!")
                print(f"Executable location: {exe_path.absolute()}")
                print("\nYou can now distribute the executable to users.")
                print("They can run it without installing Python or dependencies.")
                print("\nOptimizations applied:")
                print("✓ Excluded unused modules (matplotlib, pandas, jupyter)")
                print("✓ Added hidden imports for better compatibility")
                print("✓ Basic code optimization (--optimize=1)")
                print("✓ UPX compression enabled")
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

def copy_additional_files(dist_dir: Path):
    """Copy additional files to the dist directory."""
    try:
        # Copy README
        if os.path.exists("README.md"):
            shutil.copy("README.md", dist_dir)
            print("✓ README.md copied")

        # Copy examples
        if os.path.exists("examples"):
            examples_dir = dist_dir / "examples"
            if examples_dir.exists():
                shutil.rmtree(examples_dir)
            shutil.copytree("examples", examples_dir)
            print("✓ Examples directory copied")

        # Create a simple batch file for easy launching
        batch_content = '@echo off\nstart "" "%~dp0MusicTheoryEngine.exe"\n'
        batch_path = dist_dir / "Run_Music_Theory_Engine.bat"
        with open(batch_path, 'w') as f:
            f.write(batch_content)
        print("✓ Batch launcher created")

    except Exception as e:
        print(f"Warning: Could not copy additional files: {e}")

def clean_build():
    """Clean up build artifacts."""
    print("\nCleaning up build artifacts...")

    dirs_to_remove = ['build', 'dist']
    files_to_remove = ['MusicTheoryEngine.spec']

    for dir_name in dirs_to_remove:
        if os.path.exists(dir_name):
            try:
                shutil.rmtree(dir_name)
                print(f"✓ Removed {dir_name}/")
            except Exception as e:
                print(f"Warning: Could not remove {dir_name}: {e}")

    for file_name in files_to_remove:
        if os.path.exists(file_name):
            try:
                os.remove(file_name)
                print(f"✓ Removed {file_name}")
            except Exception as e:
                print(f"Warning: Could not remove {file_name}: {e}")

def main():
    """Main build function."""
    print("Music Theory Engine - Executable Builder")
    print("========================================")

    # Ask user for build mode
    print("Choose build mode:")
    print("1. Directory mode (recommended - faster build, smaller size)")
    print("2. Single file mode (slower build, larger size)")
    print()

    while True:
        choice = input("Enter your choice (1 or 2) [default: 1]: ").strip()
        if choice == "" or choice == "1":
            onefile = False
            break
        elif choice == "2":
            onefile = True
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")

    # Automatically clean previous builds
    print("\nCleaning previous builds...")
    clean_build()

    print()

    # Build the executable
    success = build_exe(onefile=onefile)

    if success:
        mode_desc = "single executable" if onefile else "executable directory"
        print(f"\nBuild completed successfully!")
        print(f"Your {mode_desc} is ready in the 'dist' folder.")
        if not onefile:
            print("Run the executable from: dist/MusicTheoryEngine/MusicTheoryEngine.exe")
    else:
        print("\nBuild failed. Check the error messages above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
