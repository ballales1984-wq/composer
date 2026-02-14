"""
Audio Module for the Music Engine.

This module provides audio synthesis, MIDI generation, and playback capabilities.

Structure:
- synthesizer: Waveform generation with ADSR envelope
- midi_renderer: Pure Python MIDI file generation
- player: Cross-platform audio playback
- adapter: Bridge between core models and audio

Usage:
    from music_engine.audio import AudioAdapter
    
    adapter = AudioAdapter()
    adapter.play_chord(chord)
    adapter.scale_to_midi(scale, 'scale.mid')

NOTE: This module is COMPLETELY INDEPENDENT from the core.
The core (models/chord.py, models/scale.py, etc.) does NOT depend on this module.
Users can use the core without installing audio dependencies.
"""

# Import components for easy access
from music_engine.audio.synthesizer import (
    Synthesizer,
    WaveformType,
    Envelope,
    note_to_frequency,
    generate_tone,
)

from music_engine.audio.midi_renderer import (
    MIDIRenderer,
    MIDITrack,
    create_midi_from_notes,
    create_midi_from_chord,
    create_midi_from_scale,
    create_midi_from_progression,
)

from music_engine.audio.player import (
    Player,
    get_player,
    play_samples,
    stop_playback,
    get_backend_info,
)

from music_engine.audio.adapter import (
    AudioAdapter,
    get_adapter,
    play_note,
    play_chord,
    play_scale,
    play_progression,
    chord_to_midi,
    scale_to_midi,
    progression_to_midi,
    stop,
    get_audio_status,
)

# Module version
__version__ = '1.0.0'

# Module description
__all__ = [
    # Synthesizer
    'Synthesizer',
    'WaveformType', 
    'Envelope',
    'note_to_frequency',
    'generate_tone',
    
    # MIDI Renderer
    'MIDIRenderer',
    'MIDITrack',
    'create_midi_from_notes',
    'create_midi_from_chord',
    'create_midi_from_scale',
    'create_midi_from_progression',
    
    # Player
    'Player',
    'get_player',
    'play_samples',
    'stop_playback',
    'get_backend_info',
    
    # Adapter
    'AudioAdapter',
    'get_adapter',
    'play_note',
    'play_chord',
    'play_scale',
    'play_progression',
    'chord_to_midi',
    'scale_to_midi',
    'progression_to_midi',
    'stop',
    'get_audio_status',
]

