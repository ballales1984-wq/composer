#!/usr/bin/env python3
"""
Audio test script for Music Theory Engine.

This script tests if audio functionality is working.
"""

def main():
    """Test audio functionality."""
    print("🎵 Music Theory Engine - Audio Test")
    print("=" * 40)

    try:
        from utils.audio import test_audio, get_audio_status, play_note

        print(f"Audio status: {get_audio_status()}")
        print()

        print("Testing audio playback...")
        result = test_audio()

        if "working" in result.lower():
            print("✅ Audio test successful!")
            print("You should have heard a test note (C4).")

            # Test a few more notes
            print("\nTesting different notes...")
            notes_to_test = ["C4", "E4", "G4", "C5"]
            for note in notes_to_test:
                print(f"Playing {note}...")
                play_note(note, 0.3, async_play=False)

        elif "not available" in result.lower():
            print("⚠️ Audio is not available.")
            print("To enable audio:")
            print("1. Install numpy: pip install numpy")
            print("2. Install pyaudio: pip install pyaudio  (may not work on Windows)")
            print("3. Or use the basic Windows beep sounds (already working)")

        else:
            print(f"❌ Audio test failed: {result}")

    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure you're running this from the music_engine directory.")

    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()

    print("\nPress Enter to exit...")
    input()

if __name__ == "__main__":
    main()