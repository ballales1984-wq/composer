"""
Scale model for the music theory engine.

This module defines the Scale class, which represents musical scales
with their intervals and note sequences.
"""

from typing import List, Optional, Union, Dict
from .note import Note

# Constants (copied to avoid circular imports)
SCALE_INTERVALS = {
    # Major scales
    'major': [0, 2, 4, 5, 7, 9, 11],
    'ionian': [0, 2, 4, 5, 7, 9, 11],
    # Minor scales
    'minor_natural': [0, 2, 3, 5, 7, 8, 10],
    'aeolian': [0, 2, 3, 5, 7, 8, 10],
    'minor_harmonic': [0, 2, 3, 5, 7, 8, 11],
    'minor_melodic': [0, 2, 3, 5, 7, 9, 11],
    # Modal scales
    'dorian': [0, 2, 3, 5, 7, 9, 10],
    'phrygian': [0, 1, 3, 5, 7, 8, 10],
    'lydian': [0, 2, 4, 6, 7, 9, 11],
    'mixolydian': [0, 2, 4, 5, 7, 9, 10],
    'locrian': [0, 1, 3, 5, 6, 8, 10],
    # Pentatonic scales
    'pentatonic_major': [0, 2, 4, 7, 9],
    'pentatonic_minor': [0, 3, 5, 7, 10],
    'pentatonic_blues': [0, 3, 5, 6, 7, 10],
    # Blues scales
    'blues_major': [0, 2, 3, 4, 7, 9],
    'blues_minor': [0, 3, 5, 6, 7, 10],
    # Other scales
    'whole_tone': [0, 2, 4, 6, 8, 10],
    'chromatic': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
    'diminished': [0, 2, 3, 5, 6, 8, 9, 11],
    'augmented': [0, 3, 4, 7, 8, 11],
}

SCALE_NAMES = {
    'major': 'Major (Ionian)',
    'minor_natural': 'Natural Minor (Aeolian)',
    'minor_harmonic': 'Harmonic Minor',
    'minor_melodic': 'Melodic Minor',
    'dorian': 'Dorian',
    'phrygian': 'Phrygian',
    'lydian': 'Lydian',
    'mixolydian': 'Mixolydian',
    'locrian': 'Locrian',
    'pentatonic_major': 'Major Pentatonic',
    'pentatonic_minor': 'Minor Pentatonic',
    'pentatonic_blues': 'Blues Pentatonic',
    'blues_major': 'Major Blues',
    'blues_minor': 'Minor Blues',
    'whole_tone': 'Whole Tone',
    'chromatic': 'Chromatic',
    'diminished': 'Diminished',
    'augmented': 'Augmented'
}


class Scale:
    """
    Represents a musical scale with root note and scale type.

    A Scale contains:
    - Root note
    - Scale type (major, minor, modal, etc.)
    - List of intervals in semitones
    - List of notes in the scale

    Examples:
        >>> c_major = Scale(Note('C'), 'major')
        >>> a_minor = Scale('A', 'minor_natural')
        >>> d_dorian = Scale('D', 'dorian')
        >>> print(c_major.notes)  # [C, D, E, F, G, A, B]
    """

    def __init__(self, root: Union[str, int, Note], scale_type: str, octaves: int = 1, custom_intervals: Optional[List[int]] = None):
        """
        Initialize a Scale.

        Args:
            root: Root note (Note object, string, or semitone)
            scale_type: Type of scale (e.g., 'major', 'minor_natural', 'dorian')
            octaves: Number of octaves to generate (default: 1)
            custom_intervals: Optional custom intervals list (overrides scale_type)

        Raises:
            ValueError: If scale_type is not recognized (unless custom_intervals provided)
        """
        self._root = Note(root) if not isinstance(root, Note) else root
        self._scale_type = scale_type.lower()

        # Support for custom intervals (thread-safe alternative to modifying global dict)
        if custom_intervals is not None:
            if not custom_intervals or custom_intervals[0] != 0:
                raise ValueError("Custom intervals must start with 0 (unison)")
            # Validate intervals
            for i, interval in enumerate(custom_intervals):
                if interval < 0 or interval > 24:  # Allow up to 2 octaves
                    raise ValueError(f"Invalid interval at position {i}: {interval}")
            self._intervals = custom_intervals
            self._scale_type = scale_type if scale_type.startswith('custom_') else f'custom_{scale_type}'
        else:
            if self._scale_type not in SCALE_INTERVALS:
                raise ValueError(f"Unknown scale type: {scale_type}")
            self._intervals = SCALE_INTERVALS[self._scale_type]

        self._octaves = octaves
        self._notes = self._generate_notes()

    @property
    def root(self) -> Note:
        """Get the root note of the scale."""
        return self._root

    @property
    def scale_type(self) -> str:
        """Get the scale type."""
        return self._scale_type

    @property
    def name(self) -> str:
        """Get the full name of the scale."""
        root_name = self._root.name
        scale_name = SCALE_NAMES.get(self._scale_type, self._scale_type.title())
        return f"{root_name} {scale_name}"

    @property
    def intervals(self) -> List[int]:
        """Get the scale intervals in semitones."""
        return self._intervals.copy()

    @property
    def notes(self) -> List[Note]:
        """Get all notes in the scale."""
        return self._notes.copy()

    @property
    def note_names(self) -> List[str]:
        """Get note names in the scale."""
        return [note.name for note in self._notes]

    @property
    def semitones(self) -> List[int]:
        """Get semitone values of all notes in the scale."""
        return [note.semitone for note in self._notes]

    def _generate_notes(self) -> List[Note]:
        """Generate the list of notes for this scale."""
        notes = []

        root_octave = self._root.octave

        for interval in self._intervals:
            # Calculate absolute semitone value
            total_semitones = self._root.semitone + interval

            # Calculate octave offset (each 12 semitones = 1 octave)
            octave_offset = total_semitones // 12
            semitone_in_octave = total_semitones % 12

            # Create note with correct octave - use sharp notation by default
            note_octave = root_octave + octave_offset
            note = Note.from_semitone(semitone_in_octave, octave=note_octave, use_sharps=True)
            notes.append(note)

        return notes

    def get_degree(self, degree: int) -> Note:
        """
        Get the note at a specific scale degree.

        Args:
            degree: Scale degree (1-7 for diatonic scales, 1-5 for pentatonic)

        Returns:
            Note at the specified degree

        Raises:
            IndexError: If degree is out of range
        """
        # Convert to 0-based index
        index = degree - 1
        if not (0 <= index < len(self._notes)):
            raise IndexError(f"Scale degree {degree} is out of range for {self._scale_type}")

        return self._notes[index]

    def contains_note(self, note: Union[str, int, Note]) -> bool:
        """
        Check if a note is in this scale.

        Args:
            note: Note to check

        Returns:
            True if note is in scale, False otherwise
        """
        check_note = Note(note) if not isinstance(note, Note) else note
        return check_note.semitone in self.semitones

    def get_chord(self, degree: int, chord_type: str = 'maj') -> 'Chord':
        """
        Get a chord built on a specific scale degree.

        Args:
            degree: Scale degree to build chord on (1-7)
            chord_type: Type of chord ('maj', 'min', 'dim', etc.)

        Returns:
            Chord object
        """
        from .chord import Chord
        root_note = self.get_degree(degree)
        return Chord(root_note, chord_type)

    def get_triad(self, degree: int) -> 'Chord':
        """
        Get the triad built on a specific scale degree.

        Args:
            degree: Scale degree (1-7)

        Returns:
            Triad chord (maj, min, or dim based on scale)
        """
        # Determine chord quality based on scale type and degree
        if self._scale_type in ['major', 'ionian', 'lydian', 'mixolydian']:
            triad_qualities = ['maj', 'min', 'min', 'maj', 'maj', 'min', 'dim']
        elif self._scale_type in ['minor_natural', 'aeolian']:
            triad_qualities = ['min', 'dim', 'maj', 'min', 'min', 'maj', 'maj']
        elif self._scale_type == 'minor_harmonic':
            triad_qualities = ['min', 'dim', 'aug', 'min', 'maj', 'maj', 'dim']
        elif self._scale_type == 'dorian':
            triad_qualities = ['min', 'min', 'maj', 'maj', 'min', 'dim', 'maj']
        elif self._scale_type == 'phrygian':
            triad_qualities = ['min', 'maj', 'maj', 'min', 'dim', 'maj', 'min']
        elif self._scale_type == 'locrian':
            triad_qualities = ['dim', 'maj', 'min', 'min', 'maj', 'maj', 'min']
        else:
            # Default to major scale qualities
            triad_qualities = ['maj', 'min', 'min', 'maj', 'maj', 'min', 'dim']

        quality = triad_qualities[(degree - 1) % 7]
        return self.get_chord(degree, quality)

    def transpose(self, semitones: int) -> 'Scale':
        """
        Transpose the scale by a given number of semitones.

        Args:
            semitones: Number of semitones to transpose

        Returns:
            New Scale object with transposed root
        """
        new_root = self._root.transpose(semitones)
        return Scale(new_root, self._scale_type, self._octaves)

    def get_parallel_scale(self, scale_type: str) -> 'Scale':
        """
        Get a parallel scale (same root, different type).

        Args:
            scale_type: New scale type

        Returns:
            New Scale object with same root but different type
        """
        return Scale(self._root, scale_type, self._octaves)

    def get_relative_scale(self, scale_type: str) -> 'Scale':
        """
        Get a relative scale (same notes, different root).

        For major/minor relationships, this returns the relative major/minor.
        For other scales, behavior may vary.

        Args:
            scale_type: New scale type

        Returns:
            New Scale object with different root but same notes (when applicable)
        """
        if self._scale_type == 'major' and scale_type == 'minor_natural':
            # Relative minor is 3 steps down from major root (minor third)
            new_root = self._root.transpose(-3)  # 3rd degree down
        elif self._scale_type == 'minor_natural' and scale_type == 'major':
            # Relative major is 3 steps up from minor root
            new_root = self._root.transpose(3)  # 3rd degree up
        else:
            # For other relationships, just change type (not truly relative)
            new_root = self._root

        return Scale(new_root, scale_type, self._octaves)

    def get_mode(self, mode_number: int) -> 'Scale':
        """
        Get a mode of this scale.

        Args:
            mode_number: Mode number (1 = original scale, 2 = 2nd mode, etc.)

        Returns:
            New Scale object representing the mode

        Raises:
            ValueError: If mode_number is invalid
        """
        if not (1 <= mode_number <= len(self._intervals)):
            raise ValueError(f"Invalid mode number: {mode_number}")

        # Calculate new root (move up by mode_number - 1 steps)
        mode_root = self._root.transpose(self._intervals[mode_number - 1])

        # Rotate intervals to start from the mode root
        rotated_intervals = (self._intervals[mode_number - 1:] +
                           [x + 12 for x in self._intervals[:mode_number - 1]])

        # Create new scale with rotated intervals
        mode_scale = Scale.__new__(Scale)
        mode_scale._root = mode_root
        mode_scale._scale_type = f"{self._scale_type}_mode_{mode_number}"
        mode_scale._intervals = rotated_intervals
        mode_scale._octaves = self._octaves
        mode_scale._notes = mode_scale._generate_notes()

        return mode_scale

    def __str__(self) -> str:
        """String representation of the scale."""
        return self.name

    def __repr__(self) -> str:
        """Detailed string representation for debugging."""
        return f"Scale(root={self._root}, type='{self._scale_type}')"

    def __eq__(self, other) -> bool:
        """Check equality based on root and scale type."""
        if isinstance(other, Scale):
            return (self._root == other._root and
                    self._scale_type == other._scale_type)
        return False

    def __len__(self) -> int:
        """Get the number of notes in the scale."""
        return len(self._notes)

    def __getitem__(self, index: int) -> Note:
        """Get note at index."""
        return self._notes[index]

    def __iter__(self):
        """Iterate over notes in the scale."""
        return iter(self._notes)

    # ==================== Conversion Methods ====================
    
    def to_music21(self):
        """
        Convert this Scale to a music21 scale.
        
        Returns:
            music21.scale.Scale object
            
        Requires:
            music21 library (pip install music21)
        """
        from music_engine.integrations.music21_adapter import scale_to_music21
        return scale_to_music21(self)
    
    @classmethod
    def from_music21(cls, m21_scale, scale_type: str = 'major'):
        """
        Create a Scale from a music21 scale.
        
        Args:
            m21_scale: music21.scale.Scale object
            scale_type: Scale type string for the engine
            
        Returns:
            Scale object
        """
        from music_engine.integrations.music21_adapter import music21_to_scale
        return music21_to_scale(m21_scale, scale_type)
    
    def to_mingus(self):
        """
        Convert this Scale to a mingus scale representation.
        
        Returns:
            List of note names
            
        Requires:
            mingus library (pip install mingus)
        """
        from music_engine.integrations.mingus_adapter import scale_to_mingus
        return scale_to_mingus(self)
    
    @classmethod
    def from_mingus(cls, mingus_scale, scale_type: str = 'major'):
        """
        Create a Scale from a mingus scale.
        
        Args:
            mingus_scale: mingus container or list of notes
            scale_type: Scale type string for the engine
            
        Returns:
            Scale object
        """
        from music_engine.integrations.mingus_adapter import mingus_to_scale
        return mingus_to_scale(mingus_scale, scale_type)
