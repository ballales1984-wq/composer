#!/usr/bin/env python3
"""
Basic test script for the Music Theory Engine.

This script tests the fundamental functionality of the music engine
to ensure everything is working correctly.
"""

def test_music_engine():
    """Test basic music engine functionality."""
    print("Music Theory Engine - Basic Tests")
    print("=" * 40)

    try:
        # Test 1: Direct execution of model files
        print("Testing model imports...")

        # Execute the note model
        with open('models/note.py', 'r') as f:
            note_code = f.read()
        exec(note_code, globals())

        # Execute the chord model
        with open('models/chord.py', 'r') as f:
            chord_code = f.read()
        exec(chord_code, globals())

        # Execute the scale model
        with open('models/scale.py', 'r') as f:
            scale_code = f.read()
        exec(scale_code, globals())

        print("Model imports successful!")

        # Test 2: Create basic objects
        print("Testing object creation...")

        # Create a note
        c_note = Note('C')
        print(f"Created note: {c_note}")
        print(f"Note semitone: {c_note.semitone}")

        # Create a chord
        c_chord = Chord('C', 'maj')
        print(f"Created chord: {c_chord}")
        chord_notes = [n.name for n in c_chord.notes]
        print(f"Chord notes: {chord_notes}")

        # Create a scale
        c_scale = Scale('C', 'major')
        print(f"Created scale: {c_scale}")
        scale_notes = [n.name for n in c_scale.notes]
        print(f"Scale notes: {scale_notes}")

        print("Object creation successful!")

        # Test 3: Basic operations
        print("Testing basic operations...")

        # Transpose note
        d_note = c_note.transpose(2)
        print(f"Transposed C up 2 semitones: {d_note}")

        # Test scale degree
        third_degree = c_scale.get_degree(3)
        print(f"3rd degree of C major: {third_degree}")

        print("Basic operations successful!")

        print("=" * 40)
        print("SUCCESS: Music engine core is working!")
        print("All basic functionality tests passed.")
        return True

    except Exception as e:
        print(f"FAILED: Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_music_engine()
    exit(0 if success else 1)
