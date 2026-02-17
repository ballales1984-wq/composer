"""
Note model for the music theory engine.

This module defines the Note class, which represents a musical note
with its name, accidental, and semitone value.
"""

from typing import Optional, Union, List

# Import custom exceptions
from music_engine.exceptions import InvalidNoteError, ValidationError

# Constants (copied to avoid circular imports)
NATURAL_NOTES = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
NOTE_TO_SEMITONE = {
    'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3,
    'E': 4, 'F': 5, 'F#': 6, 'Gb': 6, 'G': 7, 'G#': 8,
    'Ab': 8, 'A': 9, 'A#': 10, 'Bb': 10, 'B': 11,
    # Enharmonic equivalents (rare but valid)
    'Cb': 11,  # B
    'Fb': 4,   # E
    'E#': 5,   # F
    'B#': 0,   # C
}
SEMITONE_TO_NOTES = {
    0: ['C'], 1: ['C#', 'Db'], 2: ['D'], 3: ['D#', 'Eb'],
    4: ['E'], 5: ['F'], 6: ['F#', 'Gb'], 7: ['G'], 8: ['G#', 'Ab'],
    9: ['A'], 10: ['A#', 'Bb'], 11: ['B']
}
ENHARMONIC_EQUIVALENTS = {
    'C#': 'Db', 'Db': 'C#', 'D#': 'Eb', 'Eb': 'D#',
    'F#': 'Gb', 'Gb': 'F#', 'G#': 'Ab', 'Ab': 'G#',
    'A#': 'Bb', 'Bb': 'A#'
}

class Note:
    """
    Represents a musical note with name, accidental, octave, and semitone value.

    A Note can be created from:
    - A note name string with octave (e.g., 'C4', 'F#3', 'Bb2')
    - A note name string without octave (defaults to octave 4)
    - A semitone value (0-11) with octave
    - Another Note object

    Examples:
        >>> c4 = Note('C4')
        >>> c_sharp3 = Note('C#3')
        >>> c_default = Note('C')  # Defaults to C4
        >>> note_from_semitone = Note.from_semitone(3, 4)  # D#4/Eb4
    """

    def __init__(self, note: Union[str, int, 'Note'], accidental: Optional[str] = None, octave: int = 4):
        """
        Initialize a Note.

        Args:
            note: Note name (str), semitone value (int), or Note object
            accidental: Accidental ('#', 'b', '##', 'bb') - only used if note is str without accidental
            octave: Octave number (0-8)

        Raises:
            ValueError: If note name is invalid, semitone value is out of range, or octave is invalid
        """
        if isinstance(note, Note):
            self._name = note._name
            self._semitone = note._semitone
            self._octave = note._octave
        elif isinstance(note, str):
            self._from_string(note, accidental, octave)
        elif isinstance(note, int):
            self._from_semitone(note, octave)
        else:
            raise InvalidNoteError(f"Invalid note input: {note}", details={'input': str(note), 'type': type(note).__name__})

        # Validate octave
        if not (0 <= self._octave <= 8):
            raise InvalidNoteError(f"Octave must be between 0 and 8, got {self._octave}", details={'octave': self._octave})

    def _from_string(self, note_name: str, accidental: Optional[str] = None, octave: int = 4):
        """Parse note from string representation."""
        # Extract octave from note name if present (e.g., "C4" -> "C", 4)
        import re
        match = re.match(r'^([A-Ga-g][#b]?)([0-8])?$', note_name)
        if match:
            note_part = match.group(1)
            octave_part = match.group(2)
            if octave_part:
                octave = int(octave_part)
        else:
            # Fallback to old parsing
            note_part = note_name

        # Handle case where accidental is passed separately
        if accidental and not any(acc in note_part for acc in ['#', 'b']):
            note_part = note_part + accidental

        # Normalize the note name
        normalized = self._normalize_note_name(note_part)

        if normalized not in NOTE_TO_SEMITONE:
            raise InvalidNoteError(f"Invalid note name: {note_name}", details={'note_name': note_name})

        self._name = normalized
        self._semitone = NOTE_TO_SEMITONE[normalized]
        self._octave = octave

    def _from_semitone(self, semitone: int, octave: int = 4):
        """Create note from semitone value."""
        if not (0 <= semitone <= 11):
            raise InvalidNoteError(f"Semitone value must be between 0 and 11, got {semitone}", details={'semitone': semitone})

        self._semitone = semitone
        self._octave = octave
        # Use sharp notation by default for black keys
        self._name = SEMITONE_TO_NOTES[semitone][0]

    @staticmethod
    def _normalize_note_name(note_name: str) -> str:
        """Normalize note name to standard format."""
        note_name = note_name.strip().upper()

        # Handle double accidentals
        if note_name.startswith(('C##', 'D##', 'F##', 'G##', 'A##')):
            base = note_name[0]
            return base + '##'
        elif note_name.startswith(('CBB', 'DBB', 'EBB', 'FBB', 'GBB', 'ABB', 'BBB')):
            base = note_name[0]
            return base + 'bb'

        # Handle single accidentals
        if len(note_name) == 2:
            base, acc = note_name[0], note_name[1]
            if acc in ['#', 'B']:
                return base + ('#' if acc == '#' else 'b')
        elif len(note_name) == 3:
            base, acc1, acc2 = note_name[0], note_name[1], note_name[2]
            if acc1 == acc2 and acc1 in ['#', 'B']:
                return base + (acc1 + acc1)

        # Natural notes
        if len(note_name) == 1 and note_name in NATURAL_NOTES:
            return note_name

        return note_name  # Return as-is if can't normalize

    @classmethod
    def from_semitone(cls, semitone: int, octave: int = 4, use_sharps: bool = True) -> 'Note':
        """
        Create a Note from a semitone value.

        Args:
            semitone: Semitone value (0-11)
            octave: Octave number (0-8)
            use_sharps: Whether to use sharp notation for black keys

        Returns:
            Note object

        Raises:
            InvalidNoteError: If semitone value is out of range
        """
        if not (0 <= semitone <= 11):
            raise InvalidNoteError(f"Semitone value must be between 0 and 11, got {semitone}", 
                                  details={'semitone': semitone, 'valid_range': '0-11'})

        names = SEMITONE_TO_NOTES[semitone]
        if len(names) == 1:
            name = names[0]
        else:
            name = names[0] if use_sharps else names[1]

        return cls(name, octave=octave)
    
    @classmethod
    def from_midi(cls, midi_number: int) -> 'Note':
        """
        Create a Note from a MIDI note number.
        
        MIDI note numbers:
        - 0 = C-1 (or C0 depending on convention)
        - 60 = C4 (middle C)
        - 127 = G8

        Args:
            midi_number: MIDI note number (0-127)

        Returns:
            Note object

        Raises:
            InvalidNoteError: If MIDI number is out of range
        """
        if not (0 <= midi_number <= 127):
            raise InvalidNoteError(f"MIDI note number must be between 0 and 127, got {midi_number}", 
                                  details={'midi_number': midi_number, 'valid_range': '0-127'})
        
        # Calculate octave and semitone
        # MIDI 60 = C4, so octave = midi // 12 - 1
        octave = midi_number // 12 - 1
        semitone = midi_number % 12
        
        return cls.from_semitone(semitone, octave, use_sharps=True)

    @property
    def name(self) -> str:
        """Get the note name with octave (e.g., 'C4', 'F#3', 'Bb2')."""
        return f"{self._name}{self._octave}"

    @property
    def note_name(self) -> str:
        """Get the note name without octave (e.g., 'C', 'F#', 'Bb')."""
        return self._name

    @property
    def octave(self) -> int:
        """Get the octave number."""
        return self._octave

    @property
    def semitone(self) -> int:
        """Get the MIDI semitone value (0-127).
        
        Note: This returns the absolute MIDI value (C4 = 60).
        For the chromatic index (0-11), use the 'chroma' property.
        """
        return self.midi
    
    @property
    def chroma(self) -> int:
        """Get the chromatic index (0-11), independent of octave.
        
        C any octave = 0, C# = 1, ..., B = 11
        """
        return self._semitone
    
    @property
    def midi(self) -> int:
        """Get the MIDI note number (0-127).
        
        MIDI note numbers:
        - 0 = C-1 (or C0)
        - 60 = C4 (middle C)
        - 127 = G8
        """
        return (self._octave + 1) * 12 + self._semitone
    
    @property
    def frequency(self) -> float:
        """Get the frequency in Hz.
        
        Uses A4 = 440Hz as reference.
        """
        # MIDI 69 = A4 = 440Hz
        return 440 * (2 ** ((self.midi - 69) / 12))

    @property
    def letter(self) -> str:
        """Get the note letter (A-G)."""
        return self._name[0]

    @property
    def accidental(self) -> Optional[str]:
        """Get the accidental ('#', 'b', '##', 'bb', or None)."""
        if len(self._name) == 1:
            return None
        return self._name[1:]

    @property
    def is_natural(self) -> bool:
        """Check if note is natural (no accidental)."""
        return self.accidental is None

    @property
    def is_sharp(self) -> bool:
        """Check if note has sharp accidental."""
        acc = self.accidental
        return acc is not None and '#' in acc

    @property
    def is_flat(self) -> bool:
        """Check if note has flat accidental."""
        acc = self.accidental
        return acc is not None and 'b' in acc

    def enharmonic_equivalent(self, use_sharps: bool = True) -> Optional['Note']:
        """
        Get the enharmonic equivalent of this note.

        Args:
            use_sharps: Whether to return sharp or flat equivalent

        Returns:
            Note object with enharmonic equivalent, or None if no equivalent
        """
        if self.is_natural:
            return None

        equivalent_name = ENHARMONIC_EQUIVALENTS.get(self._name)
        if equivalent_name:
            return Note(equivalent_name)

        return None

    def transpose(self, semitones: int) -> 'Note':
        """
        Transpose this note by a given number of semitones.

        Args:
            semitones: Number of semitones to transpose (positive or negative)

        Returns:
            New Note object transposed by the given semitones
        """
        total_semitones = self._semitone + semitones
        new_octave = self._octave + (total_semitones // 12)
        new_semitone = total_semitones % 12

        # Use sharp notation by default (standard music theory convention)
        return Note.from_semitone(new_semitone, new_octave, use_sharps=True)

    def interval_to(self, other: 'Note') -> int:
        """
        Calculate the interval in semitones to another note.

        Args:
            other: Other Note object

        Returns:
            Interval in semitones (0-11)
        """
        return (other.semitone - self.semitone) % 12

    def get_all_enharmonics(self) -> List['Note']:
        """
        Get all enharmonic equivalents of this note.

        Returns:
            List of Note objects including this note and all its enharmonics
        """
        notes = [self]
        enharmonic = self.enharmonic_equivalent()
        if enharmonic:
            notes.append(enharmonic)
        return notes

    def __str__(self) -> str:
        """String representation of the note."""
        return f"{self._name}{self._octave}"

    def __repr__(self) -> str:
        """Detailed string representation for debugging."""
        return f"Note('{self._name}{self._octave}', semitone={self._semitone}, octave={self._octave})"

    def __eq__(self, other) -> bool:
        """Check equality based on note name and octave."""
        if isinstance(other, Note):
            return self._name == other._name and self._octave == other._octave
        elif isinstance(other, str):
            # Support comparison with string like "C4"
            return str(self) == other.upper()
        elif isinstance(other, int):
            return self._semitone == other
        return False

    def __hash__(self) -> int:
        """Hash based on note name and octave."""
        return hash((self._name, self._octave))

    def __lt__(self, other: 'Note') -> bool:
        """Less than comparison based on semitone value."""
        return self._semitone < other._semitone

    def __le__(self, other: 'Note') -> bool:
        """Less than or equal comparison."""
        return self._semitone <= other._semitone

    def __gt__(self, other: 'Note') -> bool:
        """Greater than comparison."""
        return self._semitone > other._semitone

    def __ge__(self, other: 'Note') -> bool:
        """Greater than or equal comparison."""
        return self._semitone >= other._semitone

    def __add__(self, semitones: int) -> 'Note':
        """Add semitones to this note."""
        return self.transpose(semitones)

    def __sub__(self, other: Union['Note', int]) -> int:
        """Subtract another note or semitones."""
        if isinstance(other, Note):
            return self.interval_to(other)
        elif isinstance(other, int):
            return self.transpose(-other)
        return NotImplemented

    # ==================== Conversion Methods ====================
    
    def to_music21(self):
        """
        Convert this Note to a music21 note.
        
        Returns:
            music21.note.Note object
            
        Requires:
            music21 library (pip install music21)
        """
        from music_engine.integrations.music21_adapter import note_to_music21
        return note_to_music21(self)
    
    @classmethod
    def from_music21(cls, m21_note):
        """
        Create a Note from a music21 note.
        
        Args:
            m21_note: music21.note.Note object
            
        Returns:
            Note object
        """
        from music_engine.integrations.music21_adapter import music21_to_note
        return music21_to_note(m21_note)
    
    def to_mingus(self):
        """
        Convert this Note to a mingus Note.
        
        Returns:
            mingus.containers.Note object
            
        Requires:
            mingus library (pip install mingus)
        """
        from music_engine.integrations.mingus_adapter import note_to_mingus
        return note_to_mingus(self)
    
    @classmethod
    def from_mingus(cls, mingus_note):
        """
        Create a Note from a mingus Note.
        
        Args:
            mingus_note: mingus.containers.Note object
            
        Returns:
            Note object
        """
        from music_engine.integrations.mingus_adapter import mingus_to_note
        return mingus_to_note(mingus_note)
