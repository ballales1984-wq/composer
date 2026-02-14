"""
Audio utilities for the Music Theory Engine.

This module provides functionality for playing musical notes and chords,
helping guitarists learn to recognize sounds by ear.
"""

import math
import threading
import time
from typing import List, Optional, Union
import sys

# Initialize audio availability at module level
AUDIO_AVAILABLE = False

# Try to import audio libraries, with fallbacks
try:
    import pyaudio
    import numpy as np
    AUDIO_AVAILABLE = True
    print("Using PyAudio for full audio support. - audio.py:22")
except ImportError:
    AUDIO_AVAILABLE = False

# Fallback to winsound if PyAudio not available
if not AUDIO_AVAILABLE:
    try:
        import winsound
        import time
        AUDIO_AVAILABLE = "winsound"
        print("Using Windows builtin audio (winsound) for simple sounds. - audio.py:32")
    except ImportError:
        AUDIO_AVAILABLE = False
        print("No audio libraries available. Audio features will be disabled. - audio.py:35")

from music_engine.models.note import Note


class AudioPlayer:
    """
    Simple audio player for musical notes and chords.

    Uses basic sine wave synthesis to generate musical tones.
    """

    # Standard concert pitch A4 = 440 Hz
    A4_FREQUENCY = 440.0

    # Sample rate for audio
    SAMPLE_RATE = 44100

    # Note frequencies relative to A4
    NOTE_FREQUENCIES = {
        'C': 261.63, 'C#': 277.18, 'Db': 277.18, 'D': 293.66, 'D#': 311.13, 'Eb': 311.13,
        'E': 329.63, 'F': 349.23, 'F#': 369.99, 'Gb': 369.99, 'G': 392.00, 'G#': 415.30,
        'Ab': 415.30, 'A': 440.00, 'A#': 466.16, 'Bb': 466.16, 'B': 493.88
    }

    def __init__(self):
        """Initialize the audio player."""
        global AUDIO_AVAILABLE  # Declare global to allow modification
        self.audio = None
        self.stream = None
        self.is_playing = False
        self.current_thread = None

        if AUDIO_AVAILABLE == "winsound":
            # winsound is available, no initialization needed
            pass
        elif AUDIO_AVAILABLE:
            try:
                self.audio = pyaudio.PyAudio()
                self.stream = self.audio.open(
                    format=pyaudio.paFloat32,
                    channels=1,
                    rate=self.SAMPLE_RATE,
                    output=True
                )
            except Exception as e:
                print(f"Audio initialization failed: {e} - audio.py:81")
                AUDIO_AVAILABLE = False

    def __del__(self):
        """Clean up audio resources."""
        self.stop()
        if self.stream:
            self.stream.close()
        if self.audio:
            self.audio.terminate()

    def get_frequency(self, note: Union[str, Note], octave: int = 4) -> float:
        """
        Get the frequency of a note.

        Args:
            note: Note name (str) or Note object
            octave: Octave number (if note is str)

        Returns:
            Frequency in Hz
        """
        if isinstance(note, Note):
            note_name = note.note_name
            octave = note.octave
        else:
            note_name = str(note).upper()

        # Get base frequency
        if note_name in self.NOTE_FREQUENCIES:
            frequency = self.NOTE_FREQUENCIES[note_name]
        else:
            # Try to parse note with octave
            if len(note_name) >= 2 and note_name[-1].isdigit():
                base_note = note_name[:-1]
                octave = int(note_name[-1])
                frequency = self.NOTE_FREQUENCIES.get(base_note, 440.0)
            else:
                frequency = 440.0  # Default to A4

        # Adjust for octave (A4 = 440Hz, each octave doubles frequency)
        octave_offset = octave - 4
        frequency *= (2 ** octave_offset)

        return frequency

    def generate_sine_wave(self, frequency: float, duration: float,
                          amplitude: float = 0.3) -> np.ndarray:
        """
        Generate a sine wave for a given frequency and duration.

        Args:
            frequency: Frequency in Hz
            duration: Duration in seconds
            amplitude: Wave amplitude (0.0 to 1.0)

        Returns:
            Numpy array of audio samples
        """
        if not AUDIO_AVAILABLE:
            return np.array([])

        t = np.linspace(0, duration, int(self.SAMPLE_RATE * duration), False)
        wave = amplitude * np.sin(frequency * 2 * np.pi * t)

        # Add a simple envelope to avoid clicks
        fade_samples = int(0.01 * self.SAMPLE_RATE)  # 10ms fade
        if len(wave) > fade_samples * 2:
            # Fade in
            fade_in = np.linspace(0, 1, fade_samples)
            wave[:fade_samples] *= fade_in

            # Fade out
            fade_out = np.linspace(1, 0, fade_samples)
            wave[-fade_samples:] *= fade_out

        return wave

    def play_note(self, note: Union[str, Note], duration: float = 1.0,
                  octave: int = 4, async_play: bool = True):
        """
        Play a single note.

        Args:
            note: Note to play
            duration: Duration in seconds
            octave: Octave (if note is str)
            async_play: Whether to play asynchronously
        """
        if not AUDIO_AVAILABLE:
            print(f"Audio not available  would play note: {note} - audio.py:171")
            return

        def play():
            try:
                frequency = self.get_frequency(note, octave)
                if AUDIO_AVAILABLE == "winsound":
                    # Use winsound for simple beep
                    duration_ms = int(duration * 1000)
                    winsound.Beep(int(frequency), duration_ms)
                else:
                    # Use pyaudio for complex sound
                    wave = self.generate_sine_wave(frequency, duration)
                    self.stream.write(wave.astype(np.float32).tobytes())
            except Exception as e:
                print(f"Error playing note: {e} - audio.py:186")

        if async_play:
            if self.current_thread and self.current_thread.is_alive():
                self.stop()
            self.current_thread = threading.Thread(target=play, daemon=True)
            self.current_thread.start()
        else:
            play()

    def play_chord(self, notes: List[Union[str, Note]], duration: float = 2.0,
                   async_play: bool = True):
        """
        Play a chord (multiple notes simultaneously).

        Args:
            notes: List of notes to play
            duration: Duration in seconds
            async_play: Whether to play asynchronously
        """
        if not AUDIO_AVAILABLE:
            print(f"Audio not available  would play chord: {notes} - audio.py:207")
            return

        def play():
            try:
                if AUDIO_AVAILABLE == "winsound":
                    # Play notes sequentially with winsound
                    print(f"Playing chord with {len(notes)} notes - audio.py:214")
                    for i, note in enumerate(notes):
                        frequency = self.get_frequency(note)
                        freq = max(200, min(10000, int(frequency)))
                        duration_ms = 400  # 400ms per note in chord
                        print(f"Chord note {i+1}: {freq}Hz - audio.py:219")
                        winsound.Beep(freq, duration_ms)
                        time.sleep(0.1)  # Gap between chord notes
                else:
                    # Generate combined wave for pyaudio
                    combined_wave = None
                    for note in notes:
                        frequency = self.get_frequency(note)
                        wave = self.generate_sine_wave(frequency, duration, amplitude=0.2)
                        if combined_wave is None:
                            combined_wave = wave
                        else:
                            combined_wave += wave

                    # Normalize to avoid clipping
                    if np.max(np.abs(combined_wave)) > 1.0:
                        combined_wave /= np.max(np.abs(combined_wave))

                    self.stream.write(combined_wave.astype(np.float32).tobytes())

            except Exception as e:
                print(f"Error playing chord: {e} - audio.py:240")

        if async_play:
            if self.current_thread and self.current_thread.is_alive():
                self.stop()
            self.current_thread = threading.Thread(target=play, daemon=True)
            self.current_thread.start()
        else:
            play()

    def play_arpeggio(self, notes: List[Union[str, Note]], note_duration: float = 0.5,
                     async_play: bool = True):
        """
        Play notes in sequence (arpeggio).

        Args:
            notes: List of notes to play in sequence
            note_duration: Duration of each note
            async_play: Whether to play asynchronously
        """
        if not AUDIO_AVAILABLE:
            print(f"Audio not available  would play arpeggio: {notes} - audio.py:261")
            return

        def play():
            try:
                for note in notes:
                    frequency = self.get_frequency(note)
                    if AUDIO_AVAILABLE == "winsound":
                        # Use winsound for simple beep
                        duration_ms = max(200, min(1000, int(note_duration * 1000)))
                        freq = max(200, min(10000, int(frequency)))
                        print(f"Arpeggio note: {freq}Hz for {duration_ms}ms - audio.py:272")
                        winsound.Beep(freq, duration_ms)
                        time.sleep(0.08)  # Gap between arpeggio notes
                    else:
                        # Use pyaudio for complex sound
                        wave = self.generate_sine_wave(frequency, note_duration)
                        self.stream.write(wave.astype(np.float32).tobytes())
                        time.sleep(0.05)  # Small gap between notes
            except Exception as e:
                print(f"Error playing arpeggio: {e} - audio.py:281")

        if async_play:
            if self.current_thread and self.current_thread.is_alive():
                self.stop()
            self.current_thread = threading.Thread(target=play, daemon=True)
            self.current_thread.start()
        else:
            play()

    def stop(self):
        """Stop current playback."""
        self.is_playing = False
        # Note: We can't actually stop pyaudio stream playback,
        # but we can prevent new playback from starting

    @staticmethod
    def is_audio_available() -> bool:
        """Check if audio playback is available."""
        return AUDIO_AVAILABLE != False


# Global audio player instance
_audio_player = None

def get_audio_player() -> AudioPlayer:
    """Get the global audio player instance."""
    global _audio_player
    if _audio_player is None:
        _audio_player = AudioPlayer()
    return _audio_player

def play_note(note: Union[str, Note], duration: float = 1.0, octave: int = 4):
    """Play a single note using the global audio player."""
    player = get_audio_player()
    player.play_note(note, duration, octave)

def play_chord(notes: List[Union[str, Note]], duration: float = 2.0):
    """Play a chord using the global audio player."""
    player = get_audio_player()
    player.play_chord(notes, duration)

def play_arpeggio(notes: List[Union[str, Note]], note_duration: float = 0.5):
    """Play an arpeggio using the global audio player."""
    player = get_audio_player()
    player.play_arpeggio(notes, note_duration)

def test_audio():
    """Test audio functionality and return status."""
    player = get_audio_player()
    if not player.is_audio_available():
        return "No audio available"

    try:
        # Play a simple test note
        player.play_note("C4", 0.3, async_play=False)
        return "Audio working"
    except Exception as e:
        return f"Audio error: {e}"

def get_audio_status():
    """Get audio system status."""
    player = get_audio_player()
    if not player.is_audio_available():
        return "Audio not available - install pyaudio and numpy for full audio, or winsound for basic beeps"

    if AUDIO_AVAILABLE == "winsound":
        return "Basic audio available (Windows beeps)"

    return "Full audio available"