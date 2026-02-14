#!/usr/bin/env python3
"""
Simple audio test that doesn't require package imports.
"""

import winsound
import time

def test_winsound():
    """Test winsound directly."""
    print("Testing Windows audio (winsound)...")

    # Test frequencies in a reasonable range
    test_notes = [
        ("C4", 261),
        ("E4", 329),
        ("G4", 392),
        ("C5", 523)
    ]

    print("Playing individual notes:")
    for note_name, freq in test_notes:
        print(f"  {note_name} ({freq}Hz)...")
        try:
            winsound.Beep(freq, 500)  # 500ms
            time.sleep(0.2)  # Short pause
        except Exception as e:
            print(f"    Error: {e}")

    print("\nPlaying chord (C major):")
    for note_name, freq in test_notes[:3]:  # C, E, G
        print(f"  {note_name} ({freq}Hz)")
        try:
            winsound.Beep(freq, 400)
            time.sleep(0.1)
        except Exception as e:
            print(f"    Error: {e}")

    print("\nWinsound test completed!")

def test_audio_range():
    """Test different frequency ranges."""
    print("\nTesting frequency ranges...")

    # Test different ranges
    ranges = [
        ("Low", [200, 300, 400]),
        ("Mid", [500, 600, 700]),
        ("High", [800, 900, 1000])
    ]

    for range_name, freqs in ranges:
        print(f"\n{range_name} frequencies:")
        for freq in freqs:
            print(f"  {freq}Hz...")
            try:
                winsound.Beep(freq, 300)
                time.sleep(0.1)
            except Exception as e:
                print(f"    Error: {e}")

if __name__ == "__main__":
    test_winsound()
    test_audio_range()
    print("\nIf you heard beeps, winsound is working!")
    print("If you didn't hear anything, check:")
    print("   - System volume")
    print("   - Audio drivers")
    print("   - Other audio applications")
    input("\nPress Enter to exit...")