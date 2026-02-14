#!/usr/bin/env python3
"""
Test script for the fretboard viewer component.
"""

import sys
import os

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import required modules
from models.fretboard import GuitarFretboard
from models.note import Note
from gui.fretboard_viewer import FretboardViewer

# Test the fretboard viewer
def test_fretboard():
    """Test the fretboard viewer component."""
    print("Testing Fretboard Viewer...")

    # Create a simple fretboard viewer instance
    try:
        viewer = FretboardViewer(None, width=800, height=400)
        print("[OK] FretboardViewer created successfully")

        # Test C Major scale
        c_notes = [
            Note("C", octave=4), Note("D", octave=4), Note("E", octave=4),
            Note("F", octave=4), Note("G", octave=4), Note("A", octave=4), Note("B", octave=4)
        ]

        print("Testing C Major scale highlighting...")
        viewer.highlight_scale(c_notes, Note("C", octave=4))
        print("[OK] Scale highlighting completed")

        # Test chord
        c_major_chord = [Note("C", octave=4), Note("E", octave=4), Note("G", octave=4)]
        print("Testing C Major chord highlighting...")
        viewer.highlight_chord(c_major_chord, Note("C", octave=4))
        print("[OK] Chord highlighting completed")

        print("All tests passed!")

    except Exception as e:
        print(f"[ERROR] {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_fretboard()