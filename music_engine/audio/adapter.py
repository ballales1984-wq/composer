"""
Audio Adapter for the Music Engine.

This module provides the bridge between core models (Chord, Scale, Progression)
and audio functionality (synthesis, MIDI, playback).

This is the main interface for playing musical data.

NOTE: This module IMPORTS from core but core does NOT depend on this module.
The core remains pure - audio is completely optional.
"""

from typing import List, Optional, Union, TYPE_CHECKING

# Import core models for type hints (don't import at runtime to avoid circular deps)
if TYPE_CHECKING:
    from music_engine.models.note import Note
    from music_engine.models.chord import Chord
    from music_engine.models.scale import Scale
    from music_engine.models.progression import Progression

# Import our audio modules
from music_engine.audio.synthesizer import (
    Synthesizer, 
    WaveformType,
    note_to_frequency,
    generate_tone
)
from music_engine.audio.midi_renderer import (
    MIDIRenderer,
    create_midi_from_notes,
    create_midi_from_chord,
    create_midi_from_scale,
    create_midi_from_progression
)
from music_engine.audio.player import (
    Player,
    get_player,
    play_samples,
    stop_playback,
    get_backend_info
)


class AudioAdapter:
    """
    Main adapter for audio playback and MIDI generation.
    
    This class provides easy-to-use methods for playing Chord, Scale,
    and Progression objects directly.
    
    Example usage:
        >>> from music_engine.models import Chord, Scale
        >>> from music_engine.audio import AudioAdapter
        >>> 
        >>> adapter = AudioAdapter()
        >>> 
        >>> # Play a chord
        >>> chord = Chord('C', 'maj')
        >>> adapter.play_chord(chord)
        >>> 
        >>> # Play a scale
        >>> scale = Scale('C', 'major')
        >>> adapter.play_scale(scale)
        >>> 
        >>> # Generate MIDI
        >>> midi_bytes = adapter.chord_to_midi(chord)
    """
    
    def __init__(self, sample_rate: int = 44100, waveform: str = 'sine'):
        """
        Initialize the audio adapter.
        
        Args:
            sample_rate: Audio sample rate in Hz
            waveform: Default waveform type ('sine', 'square', 'sawtooth', 'triangle')
        """
        self.sample_rate = sample_rate
        self.synthesizer = Synthesizer(sample_rate)
        self.player = Player(sample_rate)
        
        # Map waveform string to enum
        self.waveform = self._get_waveform(waveform)
    
    def _get_waveform(self, waveform: str) -> WaveformType:
        """Convert waveform string to enum."""
        waveform_map = {
            'sine': WaveformType.SINE,
            'square': WaveformType.SQUARE,
            'sawtooth': WaveformType.SAWTOOTH,
            'triangle': WaveformType.TRIANGLE,
            'pulse': WaveformType.PULSE,
        }
        return waveform_map.get(waveform.lower(), WaveformType.SINE)
    
    # ==================== Note Playback ====================
    
    def play_note(self, note: 'Note', duration: float = 1.0, 
                  waveform: Optional[str] = None, amplitude: float = 0.5,
                  async_play: bool = True):
        """
        Play a single note.
        
        Args:
            note: Note object from music_engine.models
            duration: Duration in seconds
            waveform: Waveform type (uses default if None)
            amplitude: Volume (0.0 to 1.0)
            async_play: Play asynchronously
        """
        wf = self._get_waveform(waveform) if waveform else self.waveform
        samples = self.synthesizer.generate_note(note, duration, wf, amplitude)
        self.player.play(samples, async_play)
    
    def note_to_audio(self, note: 'Note', duration: float = 1.0,
                     waveform: Optional[str] = None, amplitude: float = 0.5):
        """
        Generate audio samples for a single note.
        
        Returns:
            Numpy array of audio samples
        """
        wf = self._get_waveform(waveform) if waveform else self.waveform
        return self.synthesizer.generate_note(note, duration, wf, amplitude)
    
    def note_to_midi(self, note: 'Note', filepath: Optional[str] = None,
                    duration: float = 1.0, tempo: int = 500000):
        """
        Generate MIDI file for a single note.
        
        Args:
            note: Note object
            filepath: Optional path to save MIDI file
            duration: Note duration in beats
            tempo: Tempo in microseconds per beat
            
        Returns:
            MIDI file bytes
        """
        midi_note = note.midi  # Get MIDI number from Note
        return create_midi_from_notes([midi_note], filepath, duration, tempo)
    
    # ==================== Chord Playback ====================
    
    def play_chord(self, chord: 'Chord', duration: float = 2.0,
                  waveform: Optional[str] = None, amplitude: float = 0.3,
                  async_play: bool = True):
        """
        Play a chord (simultaneous notes).
        
        Args:
            chord: Chord object from music_engine.models
            duration: Duration in seconds
            waveform: Waveform type
            amplitude: Volume per note
            async_play: Play asynchronously
        """
        wf = self._get_waveform(waveform) if waveform else self.waveform
        samples = self.synthesizer.generate_chord(chord.notes, duration, wf, amplitude)
        self.player.play(samples, async_play)
    
    def play_chord_arpeggio(self, chord: 'Chord', note_duration: float = 0.3,
                           waveform: Optional[str] = None, amplitude: float = 0.5,
                           async_play: bool = True):
        """
        Play a chord as an arpeggio (sequential notes).
        
        Args:
            chord: Chord object
            note_duration: Duration of each note
            waveform: Waveform type
            amplitude: Volume per note
            async_play: Play asynchronously
        """
        wf = self._get_waveform(waveform) if waveform else self.waveform
        samples = self.synthesizer.generate_arpeggio(chord.notes, note_duration, wf, amplitude)
        self.player.play(samples, async_play)
    
    def chord_to_audio(self, chord: 'Chord', duration: float = 2.0,
                      waveform: Optional[str] = None, amplitude: float = 0.3):
        """
        Generate audio samples for a chord.
        
        Returns:
            Numpy array of audio samples
        """
        wf = self._get_waveform(waveform) if waveform else self.waveform
        return self.synthesizer.generate_chord(chord.notes, duration, wf, amplitude)
    
    def chord_to_midi(self, chord: 'Chord', filepath: Optional[str] = None,
                     duration: float = 2.0, tempo: int = 500000):
        """
        Generate MIDI file for a chord.
        
        Args:
            chord: Chord object
            filepath: Optional path to save MIDI file
            duration: Chord duration in beats
            tempo: Tempo in microseconds per beat
            
        Returns:
            MIDI file bytes
        """
        # Get MIDI numbers for all notes in chord
        midi_notes = [note.midi for note in chord.notes]
        return create_midi_from_chord(midi_notes, filepath, duration, tempo)
    
    # ==================== Scale Playback ====================
    
    def play_scale(self, scale: 'Scale', note_duration: float = 0.5,
                  waveform: Optional[str] = None, amplitude: float = 0.5,
                  async_play: bool = True):
        """
        Play a scale (sequential notes).
        
        Args:
            scale: Scale object from music_engine.models
            note_duration: Duration of each note in seconds
            waveform: Waveform type
            amplitude: Volume per note
            async_play: Play asynchronously
        """
        wf = self._get_waveform(waveform) if waveform else self.waveform
        samples = self.synthesizer.generate_scale(scale.notes, note_duration, wf, amplitude)
        self.player.play(samples, async_play)
    
    def play_scale_ascending(self, scale: 'Scale', note_duration: float = 0.5,
                            waveform: Optional[str] = None, amplitude: float = 0.5,
                            async_play: bool = True):
        """Play scale ascending (alias for play_scale)."""
        self.play_scale(scale, note_duration, waveform, amplitude, async_play)
    
    def play_scale_descending(self, scale: 'Scale', note_duration: float = 0.5,
                             waveform: Optional[str] = None, amplitude: float = 0.5,
                             async_play: bool = True):
        """
        Play a scale descending.
        
        Args:
            scale: Scale object
            note_duration: Duration of each note
            waveform: Waveform type
            amplitude: Volume per note
            async_play: Play asynchronously
        """
        wf = self._get_waveform(waveform) if waveform else self.waveform
        # Reverse the notes for descending
        descending_notes = list(scale.notes)
        descending_notes.reverse()
        samples = self.synthesizer.generate_scale(descending_notes, note_duration, wf, amplitude)
        self.player.play(samples, async_play)
    
    def scale_to_audio(self, scale: 'Scale', note_duration: float = 0.5,
                      waveform: Optional[str] = None, amplitude: float = 0.5):
        """
        Generate audio samples for a scale.
        
        Returns:
            Numpy array of audio samples
        """
        wf = self._get_waveform(waveform) if waveform else self.waveform
        return self.synthesizer.generate_scale(scale.notes, note_duration, wf, amplitude)
    
    def scale_to_midi(self, scale: 'Scale', filepath: Optional[str] = None,
                     note_duration: float = 1.0, tempo: int = 500000):
        """
        Generate MIDI file for a scale.
        
        Args:
            scale: Scale object
            filepath: Optional path to save MIDI file
            note_duration: Duration of each note in beats
            tempo: Tempo in microseconds per beat
            
        Returns:
            MIDI file bytes
        """
        midi_notes = [note.midi for note in scale.notes]
        return create_midi_from_scale(midi_notes, filepath, note_duration, tempo)
    
    # ==================== Progression Playback ====================
    
    def play_progression(self, progression: 'Progression', chord_duration: float = 2.0,
                        waveform: Optional[str] = None, amplitude: float = 0.3,
                        async_play: bool = True):
        """
        Play a chord progression.
        
        Args:
            progression: Progression object from music_engine.models
            chord_duration: Duration of each chord in seconds
            waveform: Waveform type
            amplitude: Volume per chord
            async_play: Play asynchronously
        """
        wf = self._get_waveform(waveform) if waveform else self.waveform
        
        # Generate audio for each chord
        progression_audio = None
        gap_samples = int(0.05 * self.sample_rate)  # Small gap between chords
        
        for chord in progression.chords:
            chord_audio = self.synthesizer.generate_chord(
                chord.notes, chord_duration, wf, amplitude
            )
            if progression_audio is None:
                progression_audio = chord_audio
            else:
                # Add gap
                progression_audio = np.concatenate([
                    progression_audio, 
                    np.zeros(gap_samples),
                    chord_audio
                ])
        
        if progression_audio is not None:
            self.player.play(progression_audio, async_play)
    
    def play_progression_arpeggiated(self, progression: 'Progression', 
                                    note_duration: float = 0.3,
                                    waveform: Optional[str] = None, amplitude: float = 0.5,
                                    async_play: bool = True):
        """
        Play a progression as arpeggios.
        
        Args:
            progression: Progression object
            note_duration: Duration of each note
            waveform: Waveform type
            amplitude: Volume per note
            async_play: Play asynchronously
        """
        wf = self._get_waveform(waveform) if waveform else self.waveform
        
        # Collect all notes from all chords
        all_notes = []
        for chord in progression.chords:
            all_notes.extend(chord.notes)
        
        # Play as arpeggio
        samples = self.synthesizer.generate_arpeggio(all_notes, note_duration, wf, amplitude)
        self.player.play(samples, async_play)
    
    def progression_to_midi(self, progression: 'Progression', 
                           filepath: Optional[str] = None,
                           chord_duration: float = 4.0, 
                           tempo: int = 500000):
        """
        Generate MIDI file for a chord progression.
        
        Args:
            progression: Progression object
            filepath: Optional path to save MIDI file
            chord_duration: Duration of each chord in beats
            tempo: Tempo in microseconds per beat
            
        Returns:
            MIDI file bytes
        """
        # Get MIDI notes for each chord
        chord_lists = []
        for chord in progression.chords:
            chord_midi = [note.midi for note in chord.notes]
            chord_lists.append(chord_midi)
        
        return create_midi_from_progression(chord_lists, filepath, chord_duration, tempo)
    
    # ==================== Utility Methods ====================
    
    def stop(self):
        """Stop any ongoing playback."""
        self.player.stop()
    
    def wait(self):
        """Wait for playback to finish."""
        self.player.wait()
    
    @property
    def is_playing(self) -> bool:
        """Check if audio is currently playing."""
        return self.player.is_playing
    
    @property
    def backend(self) -> str:
        """Get the current audio backend name."""
        return self.player.backend_name
    
    @property
    def available_backends(self) -> List[str]:
        """Get list of available audio backends."""
        return self.player.available_backends


# Import numpy for internal use
import numpy as np


# ==================== Convenience Functions ====================

# Global adapter instance
_adapter = None

def get_adapter(sample_rate: int = 44100, waveform: str = 'sine') -> AudioAdapter:
    """
    Get the global audio adapter instance.
    
    Args:
        sample_rate: Sample rate
        waveform: Default waveform type
        
    Returns:
        AudioAdapter instance
    """
    global _adapter
    if _adapter is None:
        _adapter = AudioAdapter(sample_rate, waveform)
    return _adapter


# Convenience functions that use the global adapter

def play_note(note: 'Note', duration: float = 1.0, **kwargs):
    """Play a single note."""
    adapter = get_adapter()
    adapter.play_note(note, duration, **kwargs)

def play_chord(chord: 'Chord', duration: float = 2.0, **kwargs):
    """Play a chord."""
    adapter = get_adapter()
    adapter.play_chord(chord, duration, **kwargs)

def play_scale(scale: 'Scale', note_duration: float = 0.5, **kwargs):
    """Play a scale."""
    adapter = get_adapter()
    adapter.play_scale(scale, note_duration, **kwargs)

def play_progression(progression: 'Progression', chord_duration: float = 2.0, **kwargs):
    """Play a chord progression."""
    adapter = get_adapter()
    adapter.play_progression(progression, chord_duration, **kwargs)

def chord_to_midi(chord: 'Chord', filepath: Optional[str] = None, **kwargs):
    """Generate MIDI from a chord."""
    adapter = get_adapter()
    return adapter.chord_to_midi(chord, filepath, **kwargs)

def scale_to_midi(scale: 'Scale', filepath: Optional[str] = None, **kwargs):
    """Generate MIDI from a scale."""
    adapter = get_adapter()
    return adapter.scale_to_midi(scale, filepath, **kwargs)

def progression_to_midi(progression: 'Progression', filepath: Optional[str] = None, **kwargs):
    """Generate MIDI from a progression."""
    adapter = get_adapter()
    return adapter.progression_to_midi(progression, filepath, **kwargs)

def stop():
    """Stop playback."""
    adapter = get_adapter()
    adapter.stop()

def get_audio_status() -> dict:
    """Get audio system status."""
    return get_backend_info()

