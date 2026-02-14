"""
MIDI Renderer for the Music Engine.

This module provides pure Python MIDI file generation without external dependencies.
It can create MIDI files from Chord, Scale, and Progression objects.

NOTE: This module is INDEPENDENT from the core. It imports from core
but core does NOT depend on this module.
"""

import struct
import os
from typing import List, Optional, Tuple, Union
from datetime import datetime


class MIDITrack:
    """
    Represents a MIDI track containing events.
    """
    
    def __init__(self):
        self.events = []
    
    def add_note_on(self, channel: int, note: int, velocity: int, delta_time: int = 0):
        """Add a note on event."""
        self.events.append({
            'type': 'note_on',
            'channel': channel,
            'note': note,
            'velocity': velocity,
            'delta': delta_time
        })
    
    def add_note_off(self, channel: int, note: int, velocity: int = 0, delta_time: int = 0):
        """Add a note off event."""
        self.events.append({
            'type': 'note_off',
            'channel': channel,
            'note': note,
            'velocity': velocity,
            'delta': delta_time
        })
    
    def add_tempo(self, microseconds_per_beat: int, delta_time: int = 0):
        """Add tempo change event (FF 51 03)."""
        self.events.append({
            'type': 'tempo',
            'microseconds': microseconds_per_beat,
            'delta': delta_time
        })
    
    def add_time_signature(self, numerator: int, denominator: int, 
                         clocks_per_click: int = 24, notes_per_quarter: int = 8,
                         delta_time: int = 0):
        """Add time signature event (FF 58 04)."""
        self.events.append({
            'type': 'time_signature',
            'numerator': numerator,
            'denominator': denominator,
            'clocks': clocks_per_click,
            'notes': notes_per_quarter,
            'delta': delta_time
        })
    
    def add_program_change(self, channel: int, program: int, delta_time: int = 0):
        """Add program change event."""
        self.events.append({
            'type': 'program',
            'channel': channel,
            'program': program,
            'delta': delta_time
        })
    
    def add_control_change(self, channel: int, control: int, value: int, delta_time: int = 0):
        """Add control change event."""
        self.events.append({
            'type': 'control',
            'channel': channel,
            'control': control,
            'value': value,
            'delta': delta_time
        })
    
    def add_end_of_track(self, delta_time: int = 0):
        """Add end of track event (FF 2F 00)."""
        self.events.append({
            'type': 'eot',
            'delta': delta_time
        })
    
    def to_bytes(self) -> bytes:
        """Convert track to MIDI bytes."""
        data = bytearray()
        
        for event in self.events:
            delta = event['delta']
            # Write variable-length quantity for delta time
            data.extend(self._write_vlq(delta))
            
            if event['type'] == 'note_on':
                status = 0x90 | (event['channel'] & 0x0F)
                data.extend([status, event['note'] & 0x7F, event['velocity'] & 0x7F])
            
            elif event['type'] == 'note_off':
                status = 0x80 | (event['channel'] & 0x0F)
                data.extend([status, event['note'] & 0x7F, event['velocity'] & 0x7F])
            
            elif event['type'] == 'tempo':
                data.extend([0xFF, 0x51, 0x03])
                microseconds = event['microseconds']
                data.extend([
                    (microseconds >> 16) & 0xFF,
                    (microseconds >> 8) & 0xFF,
                    microseconds & 0xFF
                ])
            
            elif event['type'] == 'time_signature':
                data.extend([0xFF, 0x58, 0x04])
                data.extend([
                    event['numerator'],
                    event['denominator'],
                    event['clocks'],
                    event['notes']
                ])
            
            elif event['type'] == 'program':
                status = 0xC0 | (event['channel'] & 0x0F)
                data.extend([status, event['program'] & 0x7F])
            
            elif event['type'] == 'control':
                status = 0xB0 | (event['channel'] & 0x0F)
                data.extend([status, event['control'] & 0x7F, event['value'] & 0x7F])
            
            elif event['type'] == 'eot':
                data.extend([0xFF, 0x2F, 0x00])
        
        return bytes(data)
    
    @staticmethod
    def _write_vlq(value: int) -> bytes:
        """Write a variable-length quantity."""
        result = bytearray()
        bytes_needed = []
        while True:
            bytes_needed.append(value & 0x7F)
            value >>= 7
            if value == 0:
                break
        bytes_needed.reverse()
        for i, b in enumerate(bytes_needed):
            if i < len(bytes_needed) - 1:
                result.append(b | 0x80)
            else:
                result.append(b)
        return bytes(result)


class MIDIRenderer:
    """
    MIDI file renderer for generating MIDI files from musical data.
    
    Supports:
    - Single notes
    - Chords (simultaneous notes)
    - Scales (sequential notes)
    - Progressions (chord sequences)
    """
    
    # Default tempo: 120 BPM = 500000 microseconds per beat
    DEFAULT_TEMPO = 500000
    DEFAULT_TIME_SIGNATURE = (4, 4)
    DEFAULT_VELOCITY = 100
    DEFAULT_CHANNEL = 0
    
    def __init__(self, tempo: int = DEFAULT_TEMPO, 
                 time_signature: Tuple[int, int] = DEFAULT_TIME_SIGNATURE):
        """
        Initialize MIDI renderer.
        
        Args:
            tempo: Microseconds per beat (default: 500000 = 120 BPM)
            time_signature: (numerator, denominator) tuple
        """
        self.tempo = tempo
        self.time_signature = time_signature
        self.tracks: List[MIDITrack] = []
    
    def _beats_to_ticks(self, beats: float, ticks_per_beat: int = 480) -> int:
        """Convert beats to MIDI ticks."""
        return int(beats * ticks_per_beat)
    
    def add_track(self, track: MIDITrack):
        """Add a track to the MIDI file."""
        self.tracks.append(track)
    
    def create_track(self) -> MIDITrack:
        """Create and add a new track."""
        track = MIDITrack()
        self.tracks.append(track)
        return track
    
    def add_note(self, track: MIDITrack, note: int, velocity: int = DEFAULT_VELOCITY,
                start_beat: float = 0, duration: float = 1.0,
                channel: int = DEFAULT_CHANNEL, ticks_per_beat: int = 480):
        """
        Add a single note to a track.
        
        Args:
            track: MIDITrack to add note to
            note: MIDI note number (0-127)
            velocity: Note velocity (0-127)
            start_beat: Start time in beats
            duration: Note duration in beats
            channel: MIDI channel (0-15)
            ticks_per_beat: Resolution
        """
        delta_on = self._beats_to_ticks(start_beat, ticks_per_beat)
        delta_off = self._beats_to_ticks(start_beat + duration, ticks_per_beat)
        
        track.add_note_on(channel, note, velocity, delta_on)
        track.add_note_off(channel, note, 0, delta_off)
    
    def add_chord(self, track: MIDITrack, notes: List[int], 
                 velocity: int = DEFAULT_VELOCITY,
                 start_beat: float = 0, duration: float = 2.0,
                 channel: int = DEFAULT_CHANNEL, ticks_per_beat: int = 480):
        """
        Add a chord (multiple notes simultaneously) to a track.
        
        Args:
            track: MIDITrack to add chord to
            notes: List of MIDI note numbers
            velocity: Note velocity
            start_beat: Start time in beats
            duration: Chord duration in beats
            channel: MIDI channel
            ticks_per_beat: Resolution
        """
        delta_on = self._beats_to_ticks(start_beat, ticks_per_beat)
        delta_off = self._beats_to_ticks(start_beat + duration, ticks_per_beat)
        
        # Add note on for all notes
        for i, note in enumerate(notes):
            delta = delta_on if i == 0 else 0
            track.add_note_on(channel, note, velocity, delta)
        
        # Add note off for all notes
        for i, note in enumerate(notes):
            delta = delta_off if i == len(notes) - 1 else 0
            track.add_note_off(channel, note, 0, delta)
    
    def add_scale(self, track: MIDITrack, notes: List[int],
                 velocity: int = DEFAULT_VELOCITY,
                 note_duration: float = 1.0,
                 channel: int = DEFAULT_CHANNEL, ticks_per_beat: int = 480):
        """
        Add a scale (sequential notes) to a track.
        
        Args:
            track: MIDITrack to add scale to
            notes: List of MIDI note numbers
            velocity: Note velocity
            note_duration: Duration of each note in beats
            channel: MIDI channel
            ticks_per_beat: Resolution
        """
        for i, note in enumerate(notes):
            start_beat = i * note_duration
            self.add_note(track, note, velocity, start_beat, note_duration, 
                         channel, ticks_per_beat)
    
    def add_arpeggio(self, track: MIDITrack, notes: List[int],
                    velocity: int = DEFAULT_VELOCITY,
                    note_duration: float = 0.5,
                    channel: int = DEFAULT_CHANNEL, ticks_per_beat: int = 480):
        """Add an arpeggio (rapid sequential notes) to a track."""
        # Same as scale but typically faster
        self.add_scale(track, notes, velocity, note_duration, channel, ticks_per_beat)
    
    def add_progression(self, track: MIDITrack, chords: List[List[int]],
                       velocity: int = DEFAULT_VELOCITY,
                       chord_duration: float = 4.0,
                       channel: int = DEFAULT_CHANNEL, ticks_per_beat: int = 480):
        """
        Add a chord progression to a track.
        
        Args:
            track: MIDITrack to add progression to
            chords: List of chord note lists (each chord is [root, third, fifth, ...])
            velocity: Note velocity
            chord_duration: Duration of each chord in beats
            channel: MIDI channel
            ticks_per_beat: Resolution
        """
        for i, chord_notes in enumerate(chords):
            start_beat = i * chord_duration
            self.add_chord(track, chord_notes, velocity, start_beat, 
                          chord_duration, channel, ticks_per_beat)
    
    def to_bytes(self, ticks_per_beat: int = 480) -> bytes:
        """
        Generate MIDI file bytes.
        
        Args:
            ticks_per_beat: Resolution (default: 480)
            
        Returns:
            Complete MIDI file as bytes
        """
        # MIDI header chunk
        header = b'MThd'
        header += struct.pack('>HHH', 0, 1, len(self.tracks))  # Format 1, tracks, ticks
        header += struct.pack('>H', ticks_per_beat)
        
        # Track chunks
        track_data = bytearray()
        for track in self.tracks:
            track_bytes = track.to_bytes()
            track_data.extend(b'MTrk')
            track_data.extend(struct.pack('>I', len(track_bytes)))
            track_data.extend(track_bytes)
        
        return header + bytes(track_data)
    
    def save(self, filepath: str, ticks_per_beat: int = 480):
        """
        Save MIDI file to disk.
        
        Args:
            filepath: Path to save MIDI file
            ticks_per_beat: Resolution
        """
        data = self.to_bytes(ticks_per_beat)
        with open(filepath, 'wb') as f:
            f.write(data)
    
    def get_bytes(self, ticks_per_beat: int = 480) -> bytes:
        """Get MIDI file as bytes (alias for to_bytes)."""
        return self.to_bytes(ticks_per_beat)


# Helper functions for easy MIDI generation

def create_midi_from_notes(notes: List[int], filepath: Optional[str] = None,
                           duration: float = 1.0, tempo: int = 500000) -> bytes:
    """
    Create a simple MIDI file from a list of note numbers.
    
    Args:
        notes: List of MIDI note numbers
        filepath: Optional path to save file
        duration: Duration of each note in beats
        tempo: Tempo in microseconds per beat
        
    Returns:
        MIDI file bytes
    """
    renderer = MIDIRenderer(tempo=tempo)
    track = renderer.create_track()
    track.add_tempo(tempo)
    track.add_time_signature(4, 4)
    
    for i, note in enumerate(notes):
        start = i * duration
        renderer.add_note(track, note, start_beat=start, duration=duration)
    
    track.add_end_of_track()
    
    if filepath:
        renderer.save(filepath)
    
    return renderer.to_bytes()


def create_midi_from_chord(chord_notes: List[int], filepath: Optional[str] = None,
                           duration: float = 2.0, tempo: int = 500000) -> bytes:
    """
    Create a MIDI file from chord notes (played simultaneously).
    
    Args:
        chord_notes: List of MIDI note numbers for the chord
        filepath: Optional path to save file
        duration: Duration of the chord in beats
        tempo: Tempo in microseconds per beat
        
    Returns:
        MIDI file bytes
    """
    renderer = MIDIRenderer(tempo=tempo)
    track = renderer.create_track()
    track.add_tempo(tempo)
    track.add_time_signature(4, 4)
    
    renderer.add_chord(track, chord_notes, duration=duration)
    track.add_end_of_track()
    
    if filepath:
        renderer.save(filepath)
    
    return renderer.to_bytes()


def create_midi_from_scale(scale_notes: List[int], filepath: Optional[str] = None,
                          note_duration: float = 1.0, tempo: int = 500000) -> bytes:
    """
    Create a MIDI file from scale notes (played sequentially).
    
    Args:
        scale_notes: List of MIDI note numbers for the scale
        filepath: Optional path to save file
        note_duration: Duration of each note in beats
        tempo: Tempo in microseconds per beat
        
    Returns:
        MIDI file bytes
    """
    renderer = MIDIRenderer(tempo=tempo)
    track = renderer.create_track()
    track.add_tempo(tempo)
    track.add_time_signature(4, 4)
    
    renderer.add_scale(track, scale_notes, note_duration=note_duration)
    track.add_end_of_track()
    
    if filepath:
        renderer.save(filepath)
    
    return renderer.to_bytes()


def create_midi_from_progression(chord_lists: List[List[int]], 
                                 filepath: Optional[str] = None,
                                 chord_duration: float = 4.0, 
                                 tempo: int = 500000) -> bytes:
    """
    Create a MIDI file from a chord progression.
    
    Args:
        chord_lists: List of chord note lists
        filepath: Optional path to save file
        chord_duration: Duration of each chord in beats
        tempo: Tempo in microseconds per beat
        
    Returns:
        MIDI file bytes
    """
    renderer = MIDIRenderer(tempo=tempo)
    track = renderer.create_track()
    track.add_tempo(tempo)
    track.add_time_signature(4, 4)
    
    renderer.add_progression(track, chord_lists, chord_duration=chord_duration)
    track.add_end_of_track()
    
    if filepath:
        renderer.save(filepath)
    
    return renderer.to_bytes()

