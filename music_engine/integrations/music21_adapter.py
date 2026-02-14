"""
Music21 adapter for the music theory engine.

This module provides conversion between the internal music engine models
and music21 objects for advanced analysis, MIDI, and notation capabilities.
"""

from typing import Optional, List, Union, TYPE_CHECKING

# Only import music21 when needed (lazy import)
_music21 = None

def _get_music21():
    """Lazy import of music21 module."""
    global _music21
    if _music21 is None:
        try:
            import music21
            _music21 = music21
        except ImportError:
            raise ImportError("music21 is required for this functionality. Install with: pip install music21")
    return _music21


class Music21Converter:
    """
    Converter class for transforming between music engine models and music21 objects.
    
    This allows using music21's extensive capabilities for:
    - MIDI import/export
    - Music notation (Score, Part, Measure)
    - Harmonic analysis
    - Stream processing
    - Music theory analysis
    """
    
    # Mapping from internal quality to music21 chord building
    QUALITY_TO_M21 = {
        'maj': '',
        'min': 'm',
        'dim': 'dim',
        'aug': 'aug',
        'sus2': 'sus2',
        'sus4': 'sus4',
        'maj7': 'maj7',
        'dom7': '7',
        'min7': 'm7',
        'dim7': 'dim7',
        'min7b5': 'm7b5',
        '7sus4': '7sus4',
        '9': '9',
        'min9': 'm9',
        'maj9': 'maj9',
        '11': '11',
        'min11': 'm11',
        'maj11': 'maj11',
        '13': '13',
        'min13': 'm13',
        'maj13': 'maj13',
        '6': '6',
        'min6': 'm6',
        '6/9': '6/9',
    }
    
    # Mapping from music21 chord building to internal quality
    M21_QUALITY_TO_INTERNAL = {
        '': 'maj',
        'major': 'maj',
        'm': 'min',
        'minor': 'min',
        'dim': 'dim',
        'diminished': 'dim',
        'aug': 'aug',
        'augmented': 'aug',
        'sus2': 'sus2',
        'sus4': 'sus4',
        'sus': 'sus4',
        'maj7': 'maj7',
        'major7': 'maj7',
        '7': 'dom7',
        'dominant7': 'dom7',
        'm7': 'min7',
        'minor7': 'min7',
        'dim7': 'dim7',
        'm7b5': 'min7b5',
        'halfDiminished': 'min7b5',
        '9': '9',
        'maj9': 'maj9',
        'm9': 'min9',
        '11': '11',
        'maj11': 'maj11',
        'm11': 'min11',
        '13': '13',
        'maj13': 'maj13',
        'm13': 'min13',
        '6': '6',
        'm6': 'min6',
        '6/9': '6/9',
    }

    @staticmethod
    def note_to_music21(note) -> 'music21.note.Note':
        """
        Convert a Note object to a music21 note.
        
        Args:
            note: Note object from music_engine
            
        Returns:
            music21.note.Note object
        """
        m21 = _get_music21()
        
        # Create music21 note with pitch
        m21_note = m21.note.Note()
        m21_note.pitch = note.name
        
        return m21_note
    
    @staticmethod
    def music21_to_note(m21_note) -> 'music_engine.models.Note':
        """
        Convert a music21 note to a Note object.
        
        Args:
            m21_note: music21.note.Note object
            
        Returns:
            Note object from music_engine
        """
        from music_engine.models import Note as EngineNote
        
        # Get pitch name with octave
        pitch_name = m21_note.nameWithOctave
        
        return EngineNote(pitch_name)
    
    @staticmethod
    def chord_to_music21(chord) -> 'music21.chord.Chord':
        """
        Convert a Chord object to a music21 chord.
        
        Args:
            chord: Chord object from music_engine
            
        Returns:
            music21.chord.Chord object
        """
        m21 = _get_music21()
        
        # Create music21 chord with pitch names
        pitch_names = [note.name for note in chord.notes]
        m21_chord = m21.chord.Chord(pitch_names)
        
        # Set bass note if inverted
        if chord.bass:
            m21_chord.bass()  # This sets bass to lowest note
        
        return m21_chord
    
    @staticmethod
    def music21_to_chord(m21_chord, quality: Optional[str] = None) -> 'music_engine.models.Chord':
        """
        Convert a music21 chord to a Chord object.
        
        Args:
            m21_chord: music21.chord.Chord object
            quality: Optional quality string (auto-detected if not provided)
            
        Returns:
            Chord object from music_engine
        """
        from music_engine.models import Note as EngineNote, Chord as EngineChord
        
        # Get root note from the chord
        root = m21_chord.root()
        if root:
            root_name = root.nameWithOctave
            root_note = EngineNote(root_name)
        else:
            # Fallback: use first note as root
            root_note = EngineNote(m21_chord.pitches[0].nameWithOctave)
        
        # Determine quality if not provided
        if quality is None:
            quality = Music21Converter._detect_quality(m21_chord)
        
        # Get bass note if present
        bass_note = None
        bass = m21_chord.bass()
        if bass:
            bass_note = EngineNote(bass.nameWithOctave)
        
        return EngineChord(root_note, quality, bass_note)
    
    @staticmethod
    def _detect_quality(m21_chord) -> str:
        """Detect chord quality from music21 chord."""
        # Try to determine quality from music21's figure
        figure = m21_chord.figure
        if figure:
            # Map music21 figure to internal quality
            for m21_q, internal_q in Music21Converter.M21_QUALITY_TO_INTERNAL.items():
                if m21_q.lower() in figure.lower() or figure.lower() in m21_q.lower():
                    return internal_q
        
        # Fallback: use number of notes to guess quality
        num_notes = len(m21_chord.pitches)
        if num_notes == 3:
            return 'maj'
        elif num_notes == 4:
            return 'maj7'
        elif num_notes >= 5:
            return '9'
        
        return 'maj'
    
    @staticmethod
    def scale_to_music21(scale) -> 'music21.scale.Scale':
        """
        Convert a Scale object to a music21 scale.
        
        Args:
            scale: Scale object from music_engine
            
        Returns:
            music21.scale.Scale object
        """
        m21 = _get_music21()
        
        # Map internal scale type to music21 scale
        scale_type_map = {
            'major': 'major',
            'minor_natural': 'naturalMinor',
            'minor_harmonic': 'harmonicMinor',
            'minor_melodic': 'melodicMinor',
            'dorian': 'dorian',
            'phrygian': 'phrygian',
            'lydian': 'lydian',
            'mixolydian': 'mixolydian',
            'locrian': 'locrian',
        }
        
        m21_scale_type = scale_type_map.get(scale.scale_type, 'major')
        
        # Create music21 scale
        m21_scale = m21.scale.ConcreteScale()
        m21_scale.type = m21_scale_type
        m21_scale.tonic = scale.root.name
        
        return m21_scale
    
    @staticmethod
    def music21_to_scale(m21_scale, scale_type: str = 'major') -> 'music_engine.models.Scale':
        """
        Convert a music21 scale to a Scale object.
        
        Args:
            m21_scale: music21.scale.Scale object
            scale_type: Scale type string for the engine
            
        Returns:
            Scale object from music_engine
        """
        from music_engine.models import Note as EngineNote, Scale as EngineScale
        
        # Get tonic from the scale
        if hasattr(m21_scale, 'tonic'):
            root = EngineNote(str(m21_scale.tonic))
        else:
            root = EngineNote('C')  # Default
        
        return EngineScale(root, scale_type)
    
    @staticmethod
    def stream_to_progression(m21_stream) -> 'music_engine.models.Progression':
        """
        Convert a music21 stream (chord sequence) to a Progression object.
        
        Args:
            m21_stream: music21.stream.Stream containing chords
            
        Returns:
            Progression object from music_engine
        """
        from music_engine.models import Chord as EngineChord, Progression as EngineProgression
        
        chords = []
        
        for element in m21_stream:
            # Check if element is a chord
            if hasattr(element, 'pitches'):  # It's a chord
                chord = Music21Converter.music21_to_chord(element)
                chords.append(chord)
        
        return EngineProgression(chords)
    
    @staticmethod
    def progression_to_music21_stream(progression) -> 'music21.stream.Stream':
        """
        Convert a Progression object to a music21 stream.
        
        Args:
            progression: Progression object from music_engine
            
        Returns:
            music21.stream.Stream object
        """
        m21 = _get_music21()
        
        stream = m21.stream.Stream()
        
        for chord in progression.chords:
            m21_chord = Music21Converter.chord_to_music21(chord)
            stream.append(m21_chord)
        
        return stream
    
    @staticmethod
    def analyze_harmony(m21_stream) -> dict:
        """
        Analyze harmony using music21's analysis capabilities.
        
        Args:
            m21_stream: music21.stream.Stream with chords
            
        Returns:
            Dictionary with harmonic analysis results
        """
        m21 = _get_music21()
        
        analysis = {
            'key': None,
            'key_confidence': 0.0,
            'chord_functions': [],
        }
        
        try:
            # Key detection
            key = m21.stream.analyze('key')
            analysis['key'] = str(key)
            analysis['key_confidence'] = key.correlationCoefficient
        except Exception:
            pass
        
        return analysis
    
    @staticmethod
    def midi_to_notes(midi_file: str) -> List['music_engine.models.Note']:
        """
        Import notes from a MIDI file.
        
        Args:
            midi_file: Path to MIDI file
            
        Returns:
            List of Note objects
        """
        m21 = _get_music21()
        
        # Parse MIDI file
        score = m21.converter.parse(midi_file)
        
        notes = []
        for element in score.flat.notes:
            if hasattr(element, 'pitch'):  # It's a note
                note = Music21Converter.music21_to_note(element)
                notes.append(note)
        
        return notes
    
    @staticmethod
    def midi_to_chords(midi_file: str) -> List['music_engine.models.Chord']:
        """
        Import chords from a MIDI file.
        
        Args:
            midi_file: Path to MIDI file
            
        Returns:
            List of Chord objects
        """
        m21 = _get_music21()
        
        # Parse MIDI file
        score = m21.converter.parse(midi_file)
        
        # Extract chords from the score
        chords = []
        for element in score.flat:
            if hasattr(element, 'pitches') and len(element.pitches) > 1:
                chord = Music21Converter.music21_to_chord(element)
                chords.append(chord)
        
        return chords
    
    @staticmethod
    def notes_to_midi(notes: List, output_file: str, tempo: int = 120):
        """
        Export notes to a MIDI file.
        
        Args:
            notes: List of Note or Chord objects
            output_file: Path to output MIDI file
            tempo: Tempo in BPM
        """
        m21 = _get_music21()
        
        stream = m21.stream.Stream()
        
        # Set tempo
        stream.insert(0, m21.tempo.MetronomeMark(number=tempo))
        
        for note in notes:
            if hasattr(note, 'notes'):  # It's a chord
                m21_element = Music21Converter.chord_to_music21(note)
            else:  # It's a note
                m21_element = Music21Converter.note_to_music21(note)
            stream.append(m21_element)
        
        # Write to MIDI
        stream.write('midi', fp=output_file)
    
    @staticmethod
    def stream_to_notation(m21_stream, output_file: str, format: str = 'musicxml'):
        """
        Export a stream to a notation file.
        
        Args:
            m21_stream: music21.stream.Stream object
            output_file: Path to output file
            format: Output format ('musicxml', 'pdf', 'png', 'svg')
        """
        m21_stream.write(format, fp=output_file)


# Convenience functions for easy conversion
def note_to_music21(note):
    """Convert Note to music21 note."""
    return Music21Converter.note_to_music21(note)


def music21_to_note(m21_note):
    """Convert music21 note to Note."""
    return Music21Converter.music21_to_note(m21_note)


def chord_to_music21(chord):
    """Convert Chord to music21 chord."""
    return Music21Converter.chord_to_music21(chord)


def music21_to_chord(m21_chord, quality: Optional[str] = None):
    """Convert music21 chord to Chord."""
    return Music21Converter.music21_to_chord(m21_chord, quality)


def scale_to_music21(scale):
    """Convert Scale to music21 scale."""
    return Music21Converter.scale_to_music21(scale)


def progression_to_music21_stream(progression):
    """Convert Progression to music21 stream."""
    return Music21Converter.progression_to_music21_stream(progression)


def stream_to_progression(m21_stream):
    """Convert music21 stream to Progression."""
    return Music21Converter.stream_to_progression(m21_stream)

