"""
Chord model for the music theory engine.

This module defines the Chord class, which represents musical chords
with their root note, quality, and component notes.
"""

from typing import List, Optional, Union, Dict, Tuple
from .note import Note
from music_engine.exceptions import InvalidChordError, InvalidQualityError, InvalidNoteError

# Constants (copied to avoid circular imports)
CHORD_INTERVALS = {
    # Triads
    'maj': [0, 4, 7], 'min': [0, 3, 7], 'dim': [0, 3, 6], 'aug': [0, 4, 8],
    'sus2': [0, 2, 7], 'sus4': [0, 5, 7], '5': [0, 7],
    # Seventh chords
    'maj7': [0, 4, 7, 11], 'dom7': [0, 4, 7, 10], 'min7': [0, 3, 7, 10],
    'dim7': [0, 3, 6, 9], 'min7b5': [0, 3, 6, 10], 'maj7b5': [0, 4, 6, 11],
    '7sus4': [0, 5, 7, 10], '7b9': [0, 4, 7, 10, 13],
    # Extended chords
    '9': [0, 4, 7, 10, 14], 'min9': [0, 3, 7, 10, 14], 'maj9': [0, 4, 7, 11, 14],
    '11': [0, 4, 7, 10, 14, 17], 'min11': [0, 3, 7, 10, 14, 17],
    'maj11': [0, 4, 7, 11, 14, 17], '13': [0, 4, 7, 10, 14, 21],
    'min13': [0, 3, 7, 10, 14, 21], 'maj13': [0, 4, 7, 11, 14, 21],
    # Added tone chords
    '6': [0, 4, 7, 9], 'min6': [0, 3, 7, 9], '6/9': [0, 4, 7, 9, 14],
    '7#11': [0, 4, 7, 10, 18],
    # Quartal and quintal
    'quartal': [0, 5, 10, 15], 'quintal': [0, 7, 14, 21],
}

CHORD_NAMES = {
    'maj': 'Major', 'min': 'Minor', 'dim': 'Diminished', 'aug': 'Augmented',
    'sus2': 'Suspended 2nd', 'sus4': 'Suspended 4th', '5': '5th',
    'maj7': 'Major 7th', 'dom7': 'Dominant 7th', 'min7': 'Minor 7th',
    'dim7': 'Diminished 7th', 'min7b5': 'Minor 7th Flat 5',
    'maj7b5': 'Major 7th Flat 5', '7sus4': '7th Suspended 4th',
    '7b9': '7th Flat 9', '9': '9th', 'min9': 'Minor 9th', 'maj9': 'Major 9th',
    '11': '11th', 'min11': 'Minor 11th', 'maj11': 'Major 11th',
    '13': '13th', 'min13': 'Minor 13th', 'maj13': 'Major 13th',
    '6': '6th', 'min6': 'Minor 6th', '6/9': '6/9', '7#11': '7th Sharp 11',
    'quartal': 'Quartal', 'quintal': 'Quintal'
}


class Chord:
    """
    Represents a musical chord with root note and quality.

    A Chord contains:
    - Root note
    - Chord quality (maj, min, 7, etc.)
    - List of intervals in semitones
    - List of notes in the chord
    - Optional bass note (for inversions)

    Examples:
        >>> c_major = Chord(Note('C'), 'maj')
        >>> d_minor = Chord('D', 'min')
        >>> g_dom7 = Chord('G', 'dom7')
        >>> print(c_major.notes)  # [C, E, G]
    """

    # Quality aliases for common abbreviations
    QUALITY_ALIASES = {
        'm': 'min',
        'minor': 'min',
        'maj': 'maj',
        'major': 'maj',
        'dim': 'dim',
        'diminished': 'dim',
        'aug': 'aug',
        'augmented': 'aug',
        'sus': 'sus4',
        'sus2': 'sus2',
        'sus4': 'sus4',
        '7': 'dom7',
        'dom': 'dom7',
        'dom7': 'dom7',
        'maj7': 'maj7',
        'major7': 'maj7',
        'min7': 'min7',
        'minor7': 'min7',
        'm7': 'min7',
        'dim7': 'dim7',
        'm7b5': 'min7b5',
        'min7b5': 'min7b5',
        '9': '9',
        'maj9': 'maj9',
        'min9': 'min9',
        'm9': 'min9',
        '11': '11',
        'min11': 'min11',
        'm11': 'min11',
        '13': '13',
        'min13': 'min13',
        'm13': 'min13',
        'maj13': 'maj13',
        '6': '6',
        'min6': 'min6',
        'm6': 'min6',
        '6/9': '6/9',
        '7sus4': '7sus4',
        '7sus': '7sus4',
        '7#11': '7#11',
        'add9': '9',
        'add11': '11',
        'add13': '13',
    }

    def __init__(self, root: Union[str, int, Note], quality: str, bass: Optional[Union[str, int, Note]] = None, custom_intervals: Optional[List[int]] = None):
        """
        Initialize a Chord.

        Args:
            root: Root note (Note object, string, or semitone)
            quality: Chord quality (e.g., 'maj', 'min', 'dom7', 'dim7')
            bass: Optional bass note for inversions (Note object, string, or semitone)
            custom_intervals: Optional custom intervals list (overrides quality)

        Raises:
            InvalidChordError: If chord cannot be created with given parameters
            InvalidQualityError: If quality is not recognized
            InvalidNoteError: If root or bass note is invalid
        """
        # Validate and create root note
        try:
            self._root = Note(root) if not isinstance(root, Note) else root
        except Exception as e:
            raise InvalidNoteError(f"Invalid root note: {root}", details={'root': str(root), 'error': str(e)})
        
        self._quality = quality.lower()
        
        # Apply quality aliases
        if self._quality in self.QUALITY_ALIASES:
            self._quality = self.QUALITY_ALIASES[self._quality]

        # Support for custom intervals (thread-safe alternative to modifying global dict)
        if custom_intervals is not None:
            if not custom_intervals or custom_intervals[0] != 0:
                raise InvalidChordError("Custom intervals must start with 0 (root)", 
                                        details={'custom_intervals': custom_intervals})
            # Validate intervals
            for i, interval in enumerate(custom_intervals):
                if interval < 0 or interval > 24:  # Allow up to 2 octaves
                    raise InvalidChordError(f"Invalid interval at position {i}: {interval}",
                                           details={'interval': interval, 'position': i})
            self._intervals = custom_intervals
            self._quality = quality if quality.startswith('custom_') else f'custom_{quality}'
        else:
            if self._quality not in CHORD_INTERVALS:
                raise InvalidQualityError(f"Unknown chord quality: {quality}",
                                         details={'quality': quality, 'valid_qualities': list(CHORD_INTERVALS.keys())})
            self._intervals = CHORD_INTERVALS[self._quality]

        # Validate and create bass note
        if bass is not None:
            try:
                self._bass = Note(bass) if not isinstance(bass, Note) else bass
            except Exception as e:
                raise InvalidNoteError(f"Invalid bass note: {bass}", details={'bass': str(bass), 'error': str(e)})
        else:
            self._bass = None
            
        self._notes = self._generate_notes()

    @property
    def root(self) -> Note:
        """Get the root note of the chord."""
        return self._root

    @property
    def quality(self) -> str:
        """Get the chord quality."""
        return self._quality

    @property
    def name(self) -> str:
        """Get the full name of the chord."""
        root_name = self._root.note_name  # Use note_name without octave
        quality_name = CHORD_NAMES.get(self._quality, self._quality.upper())
        chord_name = f"{root_name}{quality_name}"

        if self._bass and self._bass != self._root:
            chord_name += f"/{self._bass.note_name}"

        return chord_name

    @property
    def intervals(self) -> List[int]:
        """Get the chord intervals in semitones."""
        return self._intervals.copy()

    @property
    def notes(self) -> List[Note]:
        """Get all notes in the chord."""
        return self._notes.copy()

    @property
    def note_names(self) -> List[str]:
        """Get note names in the chord."""
        return [note.name for note in self._notes]

    @property
    def semitones(self) -> List[int]:
        """Get semitone values of all notes in the chord."""
        return [note.semitone for note in self._notes]

    @property
    def bass(self) -> Optional[Note]:
        """Get the bass note (for inversions)."""
        return self._bass

    @property
    def is_inverted(self) -> bool:
        """Check if chord has an inversion (bass note different from root)."""
        return self._bass is not None and self._bass != self._root

    def _generate_notes(self) -> List[Note]:
        """Generate the list of notes for this chord."""
        notes = []

        for interval in self._intervals:
            semitone = (self._root.semitone + interval) % 12
            note = Note.from_semitone(semitone, octave=self._root.octave, use_sharps=True)
            notes.append(note)

        # Sort notes - if bass is set, put bass first; otherwise root first
        if notes:
            if self._bass is not None:
                # Find bass note in the list and move it to front
                bass_index = None
                for i, note in enumerate(notes):
                    if note.semitone == self._bass.semitone:
                        bass_index = i
                        break
                if bass_index is not None and bass_index != 0:
                    notes = [notes[bass_index]] + notes[:bass_index] + notes[bass_index + 1:]
            else:
                # Find root note in the list and move it to front
                root_index = None
                for i, note in enumerate(notes):
                    if note.semitone == self._root.semitone:
                        root_index = i
                        break
                if root_index is not None and root_index != 0:
                    notes = [notes[root_index]] + notes[:root_index] + notes[root_index + 1:]

        return notes

    def contains_note(self, note: Union[str, int, Note]) -> bool:
        """
        Check if a note is in this chord.

        Args:
            note: Note to check

        Returns:
            True if note is in chord, False otherwise
        """
        check_note = Note(note) if not isinstance(note, Note) else note
        return check_note.semitone in self.semitones

    def get_inversion(self, inversion: int) -> 'Chord':
        """
        Get a specific inversion of this chord.

        Args:
            inversion: Inversion number (0 = root position, 1 = first inversion, etc.)

        Returns:
            New Chord object with the specified inversion

        Raises:
            InvalidChordError: If inversion is invalid for this chord
        """
        if inversion < 0:
            raise InvalidChordError("Inversion must be non-negative",
                                   details={'inversion': inversion})

        if inversion == 0:
            return Chord(self._root, self._quality)

        # For inversions, we need to rotate the notes and set the bass
        chord_notes = self._notes.copy()

        if inversion >= len(chord_notes):
            raise InvalidChordError(f"Inversion {inversion} is invalid for {len(chord_notes)}-note chord",
                                   details={'inversion': inversion, 'max_inversion': len(chord_notes) - 1})

        # Rotate notes so the bass note is first
        rotated_notes = chord_notes[inversion:] + chord_notes[:inversion]
        bass_note = rotated_notes[0]

        # Create new chord with same quality but different bass
        return Chord(self._root, self._quality, bass_note)

    def get_all_inversions(self) -> List['Chord']:
        """
        Get all possible inversions of this chord.

        Returns:
            List of Chord objects for all inversions
        """
        inversions = []
        for i in range(len(self._notes)):
            inversions.append(self.get_inversion(i))
        return inversions

    def transpose(self, semitones: int) -> 'Chord':
        """
        Transpose the chord by a given number of semitones.

        Args:
            semitones: Number of semitones to transpose

        Returns:
            New Chord object with transposed root and bass
        """
        new_root = self._root.transpose(semitones)
        new_bass = self._bass.transpose(semitones) if self._bass else None
        return Chord(new_root, self._quality, new_bass)

    def get_voicing(self, octave: int = 4, spread: bool = True) -> List[Tuple[Note, int]]:
        """
        Get a guitar-friendly voicing of the chord.

        Args:
            octave: Base octave for the root note
            spread: Whether to spread notes across octaves

        Returns:
            List of (Note, octave) tuples for a chord voicing
        """
        voicing = []

        for i, note in enumerate(self._notes):
            note_octave = octave
            if spread and i > 0:
                # Spread additional notes to higher octaves
                note_octave += (note.semitone < self._root.semitone)
            voicing.append((note, note_octave))

        return voicing

    def get_extensions(self) -> List[str]:
        """
        Get possible extensions for this chord.

        Returns:
            List of possible extended chord qualities
        """
        extensions = []

        # Define extension relationships
        extension_map = {
            'maj': ['6', 'maj7', 'maj9', 'maj11', 'maj13', '6/9'],
            'min': ['min6', 'min7', 'min9', 'min11', 'min13'],
            'dom7': ['9', '11', '13', '7b9', '7#11'],
            'dim': ['dim7'],
            'min7b5': [],  # Limited extensions for half-diminished
            'dim7': []     # Fully diminished has limited extensions
        }

        if self._quality in extension_map:
            extensions = extension_map[self._quality]

        return extensions

    def get_additions(self) -> List[str]:
        """
        Get possible added tone chords from this chord.

        Returns:
            List of possible added tone chord qualities
        """
        additions = []

        # Define addition relationships
        addition_map = {
            'maj': ['6', '6/9', 'maj7', 'maj9'],
            'min': ['min6', 'min7', 'min9'],
            'dom7': ['9', '11', '13'],
        }

        if self._quality in addition_map:
            additions = addition_map[self._quality]

        return additions

    def get_tension_notes(self) -> List[Note]:
        """
        Get the tension/extension notes in the chord.

        Returns:
            List of tension notes (9th, 11th, 13th, etc.)
        """
        tensions = []

        # Notes beyond the basic triad/7th are tensions
        basic_notes = 3  # Triad
        if '7' in self._quality or 'maj7' in self._quality:
            basic_notes = 4  # Seventh chord

        if len(self._notes) > basic_notes:
            tensions = self._notes[basic_notes:]

        return tensions

    def simplify(self) -> 'Chord':
        """
        Simplify the chord to its basic triad.

        Returns:
            New Chord object with basic triad quality
        """
        # Map extended qualities to basic triads
        simplification_map = {
            # Major family
            'maj': 'maj', '6': 'maj', '6/9': 'maj', 'maj7': 'maj',
            'maj9': 'maj', 'maj11': 'maj', 'maj13': 'maj',

            # Minor family
            'min': 'min', 'min6': 'min', 'min7': 'min', 'min7b5': 'dim',
            'min9': 'min', 'min11': 'min', 'min13': 'min',

            # Dominant family
            'dom7': 'maj', '9': 'maj', '11': 'maj', '13': 'maj',
            '7b9': 'maj', '7#11': 'maj',

            # Diminished family
            'dim': 'dim', 'dim7': 'dim',

            # Other
            'sus2': 'maj', 'sus4': 'maj', '5': 'maj', 'aug': 'aug'
        }

        basic_quality = simplification_map.get(self._quality, 'maj')
        return Chord(self._root, basic_quality)

    def __str__(self) -> str:
        """String representation of the chord."""
        return self.name

    def __repr__(self) -> str:
        """Detailed string representation for debugging."""
        bass_str = f", bass={self._bass}" if self._bass else ""
        return f"Chord(root={self._root}, quality='{self._quality}'{bass_str})"

    def __eq__(self, other) -> bool:
        """Check equality based on root, quality, and bass."""
        if isinstance(other, Chord):
            return (self._root == other._root and
                    self._quality == other._quality and
                    self._bass == other._bass)
        return False

    def __len__(self) -> int:
        """Get the number of notes in the chord."""
        return len(self._notes)

    def __getitem__(self, index: int) -> Note:
        """Get note at index."""
        return self._notes[index]

    def __iter__(self):
        """Iterate over notes in the chord."""
        return iter(self._notes)

    # ==================== Conversion Methods ====================
    
    def to_music21(self):
        """
        Convert this Chord to a music21 chord.
        
        Returns:
            music21.chord.Chord object
            
        Requires:
            music21 library (pip install music21)
        """
        from music_engine.integrations.music21_adapter import chord_to_music21
        return chord_to_music21(self)
    
    @classmethod
    def from_music21(cls, m21_chord, quality: str = None):
        """
        Create a Chord from a music21 chord.
        
        Args:
            m21_chord: music21.chord.Chord object
            quality: Optional quality string (auto-detected if not provided)
            
        Returns:
            Chord object
        """
        from music_engine.integrations.music21_adapter import music21_to_chord
        return music21_to_chord(m21_chord, quality)
    
    def to_mingus(self):
        """
        Convert this Chord to a mingus Chord.
        
        Returns:
            mingus.containers.Chord object
            
        Requires:
            mingus library (pip install mingus)
        """
        from music_engine.integrations.mingus_adapter import chord_to_mingus
        return chord_to_mingus(self)
    
    @classmethod
    def from_mingus(cls, mingus_chord, root_note = None):
        """
        Create a Chord from a mingus Chord.
        
        Args:
            mingus_chord: mingus.containers.Chord object
            root_note: Optional root note (auto-detected if not provided)
            
        Returns:
            Chord object
        """
        from music_engine.integrations.mingus_adapter import mingus_to_chord
        return mingus_to_chord(mingus_chord, root_note)
