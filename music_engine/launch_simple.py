#!/usr/bin/env python3
"""
Simple launcher for Music Theory Engine that avoids import issues.
"""

import sys
import os

# Add the music_engine directory to path
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

# Set environment to avoid import issues
os.environ['PYTHONPATH'] = script_dir

# Import and run
try:
    from main_gui import main
    main()
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()