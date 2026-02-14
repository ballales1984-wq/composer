"""
Audio synthesizer for the Music Engine.

This module provides waveform generation and synthesis capabilities,
converting musical notes to audio waveforms.

NOTE: This module is INDEPENDENT from the core. It imports from core
but core does NOT depend on this module.
"""

import math
from typing import List, Optional, Tuple, Union
from enum import Enum

import numpy as np

# Try to import numpy - if not available, we'll use a fallback
try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    # Fallback will be limited


class WaveformType(Enum):
    """Available waveform types for synthesis."""
    SINE = "sine"
    SQUARE = "square"
    SAWTOOTH = "sawtooth"
    TRIANGLE = "triangle"
    PULSE = "pulse"


class Envelope:
    """
    ADSR Envelope for amplitude control.
    
    Attributes:
        attack: Attack time in seconds
        decay: Decay time in seconds
        sustain: Sustain level (0.0 to 1.0)
        release: Release time in seconds
    """
    
    def __init__(self, attack: float = 0.01, decay: float = 0.1, 
                 sustain: float = 0.7, release: float = 0.3):
        self.attack = attack
        self.decay = decay
        self.sustain = sustain
        self.release = release
    
    def apply(self, samples: np.ndarray, sample_rate: int, 
              duration: float) -> np.ndarray:
        """
        Apply ADSR envelope to audio samples.
        
        Args:
            samples: Audio samples
            sample_rate: Sample rate in Hz
            duration: Total duration in seconds
            
        Returns:
            Envelope-modified samples
        """
        n_samples = len(samples)
        attack_samples = int(self.attack * sample_rate)
        decay_samples = int(self.decay * sample_rate)
        release_samples = int(self.release * sample_rate)
        
        # Ensure we have enough samples
        if n_samples < attack_samples + decay_samples + release_samples:
            return samples  # Too short for envelope
        
        # Create envelope
        envelope = np.ones(n_samples)
        
        # Attack phase (0 -> 1)
        if attack_samples > 0:
            envelope[:attack_samples] = np.linspace(0, 1, attack_samples)
        
        # Decay phase (1 -> sustain)
        if decay_samples > 0:
            decay_end = attack_samples + decay_samples
            envelope[attack_samples:decay_end] = np.linspace(1, self.sustain, decay_samples)
        
        # Sustain phase (constant at sustain level)
        sustain_start = attack_samples + decay_samples
        sustain_end = n_samples - release_samples
        envelope[sustain_start:sustain_end] = self.sustain
        
        # Release phase (sustain -> 0)
        if release_samples > 0:
            envelope[-release_samples:] = np.linspace(self.sustain, 0, release_samples)
        
        return samples * envelope


class Synthesizer:
    """
    Audio synthesizer for generating waveforms from musical notes.
    
    This class handles:
    - Note to frequency conversion
    - Waveform generation (sine, square, sawtooth, triangle)
    - ADSR envelope application
    - Multi-voice synthesis
    """
    
    # Standard concert pitch A4 = 440 Hz
    A4_FREQUENCY = 440.0
    A4_MIDI = 69
    
    # Sample rate for audio synthesis
    DEFAULT_SAMPLE_RATE = 44100
    
    def __init__(self, sample_rate: int = DEFAULT_SAMPLE_RATE):
        """
        Initialize the synthesizer.
        
        Args:
            sample_rate: Audio sample rate in Hz (default: 44100)
        """
        self.sample_rate = sample_rate
        self.envelope = Envelope()
    
    def note_to_frequency(self, note: 'Note') -> float:
        """
        Convert a Note to its frequency in Hz.
        
        Args:
            note: Note object from music_engine.models
            
        Returns:
            Frequency in Hz
        """
        # Use the Note's built-in frequency property
        return note.frequency
    
    def midi_to_frequency(self, midi_number: int) -> float:
        """
        Convert MIDI note number to frequency.
        
        Args:
            midi_number: MIDI note number (0-127)
            
        Returns:
            Frequency in Hz
        """
        return self.A4_FREQUENCY * (2 ** ((midi_number - self.A4_MIDI) / 12))
    
    def frequency_to_midi(self, frequency: float) -> int:
        """
        Convert frequency to MIDI note number.
        
        Args:
            frequency: Frequency in Hz
            
        Returns:
            MIDI note number (0-127)
        """
        return int(round(12 * math.log2(frequency / self.A4_FREQUENCY) + self.A4_MIDI))
    
    def generate_waveform(self, frequency: float, duration: float,
                         waveform: WaveformType = WaveformType.SINE,
                         amplitude: float = 0.5) -> np.ndarray:
        """
        Generate a waveform for a given frequency and duration.
        
        Args:
            frequency: Frequency in Hz
            duration: Duration in seconds
            waveform: Type of waveform to generate
            amplitude: Amplitude (0.0 to 1.0)
            
        Returns:
            Numpy array of audio samples
        """
        if not NUMPY_AVAILABLE:
            return np.array([])  # Return empty if numpy not available
        
        n_samples = int(self.sample_rate * duration)
        t = np.linspace(0, duration, n_samples, False)
        
        if waveform == WaveformType.SINE:
            wave = amplitude * np.sin(2 * np.pi * frequency * t)
        elif waveform == WaveformType.SQUARE:
            wave = amplitude * np.sign(np.sin(2 * np.pi * frequency * t))
        elif waveform == WaveformType.SAWTOOTH:
            wave = amplitude * (2 * (t * frequency - np.floor(0.5 + t * frequency)))
        elif waveform == WaveformType.TRIANGLE:
            wave = amplitude * (2 * np.abs(2 * (t * frequency - np.floor(0.5 + t * frequency))) - 1)
        elif waveform == WaveformType.PULSE:
            # Pulse wave (narrow square)
            duty_cycle = 0.25
            wave = amplitude * np.sign(np.sin(2 * np.pi * frequency * t) - (1 - 2 * duty_cycle))
        else:
            wave = amplitude * np.sin(2 * np.pi * frequency * t)
        
        # Apply envelope
        wave = self.envelope.apply(wave, self.sample_rate, duration)
        
        return wave
    
    def generate_note(self, note: 'Note', duration: float,
                     waveform: WaveformType = WaveformType.SINE,
                     amplitude: float = 0.5) -> np.ndarray:
        """
        Generate audio for a single note.
        
        Args:
            note: Note object from music_engine.models
            duration: Duration in seconds
            waveform: Type of waveform to generate
            amplitude: Amplitude (0.0 to 1.0)
            
        Returns:
            Numpy array of audio samples
        """
        frequency = self.note_to_frequency(note)
        return self.generate_waveform(frequency, duration, waveform, amplitude)
    
    def generate_chord(self, notes: List['Note'], duration: float,
                      waveform: WaveformType = WaveformType.SINE,
                      amplitude: float = 0.3) -> np.ndarray:
        """
        Generate audio for multiple notes played simultaneously (chord).
        
        Args:
            notes: List of Note objects
            duration: Duration in seconds
            waveform: Type of waveform to generate
            amplitude: Amplitude per note (will be normalized)
            
        Returns:
            Numpy array of audio samples (combined)
        """
        if not notes:
            return np.array([])
        
        # Reduce amplitude for chords to avoid clipping
        note_amplitude = amplitude / len(notes)
        
        # Generate waveform for each note and combine
        combined = None
        for note in notes:
            wave = self.generate_note(note, duration, waveform, note_amplitude)
            if combined is None:
                combined = wave
            else:
                combined += wave
        
        # Normalize to prevent clipping
        if combined is not None and np.max(np.abs(combined)) > 1.0:
            combined = combined / np.max(np.abs(combined))
        
        return combined
    
    def generate_scale(self, notes: List['Note'], note_duration: float = 0.5,
                      waveform: WaveformType = WaveformType.SINE,
                      amplitude: float = 0.5,
                      gap: float = 0.05) -> np.ndarray:
        """
        Generate audio for a scale played sequentially.
        
        Args:
            notes: List of Note objects (scale notes)
            note_duration: Duration of each note in seconds
            waveform: Type of waveform to generate
            amplitude: Amplitude per note
            gap: Gap between notes in seconds
            
        Returns:
            Numpy array of audio samples
        """
        if not notes:
            return np.array([])
        
        # Calculate gap samples
        gap_samples = int(gap * self.sample_rate)
        
        # Generate each note with envelope (shorter release for scale)
        original_release = self.envelope.release
        self.envelope.release = 0.1  # Shorter release for scales
        
        scale_audio = []
        for note in notes:
            wave = self.generate_note(note, note_duration, waveform, amplitude)
            scale_audio.append(wave)
            # Add silence for gap
            if gap_samples > 0:
                scale_audio.append(np.zeros(gap_samples))
        
        # Restore original envelope
        self.envelope.release = original_release
        
        return np.concatenate(scale_audio) if scale_audio else np.array([])
    
    def generate_arpeggio(self, notes: List['Note'], note_duration: float = 0.3,
                         waveform: WaveformType = WaveformType.SINE,
                         amplitude: float = 0.5) -> np.ndarray:
        """
        Generate audio for an arpeggio (notes played in sequence).
        
        Args:
            notes: List of Note objects
            note_duration: Duration of each note
            waveform: Type of waveform
            amplitude: Amplitude per note
            
        Returns:
            Numpy array of audio samples
        """
        # Arpeggio is similar to scale but with specific note durations
        return self.generate_scale(notes, note_duration, waveform, amplitude, gap=0.02)


# Convenience function for basic usage
def note_to_frequency(note: 'Note') -> float:
    """
    Convert a Note to frequency (convenience function).
    
    Args:
        note: Note object
        
    Returns:
        Frequency in Hz
    """
    synth = Synthesizer()
    return synth.note_to_frequency(note)


def generate_tone(frequency: float, duration: float, 
                 sample_rate: int = 44100) -> np.ndarray:
    """
    Generate a simple sine wave tone.
    
    Args:
        frequency: Frequency in Hz
        duration: Duration in seconds
        sample_rate: Sample rate in Hz
        
    Returns:
        Audio samples as numpy array
    """
    synth = Synthesizer(sample_rate)
    return synth.generate_waveform(frequency, duration)

