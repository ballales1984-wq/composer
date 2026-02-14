"""
Arpeggio model for the music theory engine.

This module defines the Arpeggio class, which represents musical arpeggios
with different directions and patterns.
"""

from typing import List, Optional, Union
from .note import Note
from .chord import Chord
from .scale import Scale


class Arpeggio:
    """
    Represents a musical arpeggio with direction and pattern.

    An Arpeggio contains:
    - Source chord or scale
    - Direction (up, down, up_down, etc.)
    - Pattern of notes
    - Speed/rhythm information (future extension)

    Examples:
        >>> c_major = Chord('C', 'maj')
        >>> arp = Arpeggio(c_major, 'up')
        >>> print(arp.notes)  # [C, E, G, C]
    """

    def __init__(self, source: Union[Chord, Scale],
                 direction: str = 'up',
                 octaves: int = 1,
                 start_degree: int = 1):
        """
        Initialize an Arpeggio.

        Args:
            source: Source chord or scale
            direction: Direction ('up', 'down', 'up_down', 'down_up')
            octaves: Number of octaves to span
            start_degree: Starting degree (for scales) or note index (for chords)

        Raises:
            ValueError: If direction is invalid or source is not supported
        """
        self._source = source
        self._direction = direction.lower()
        self._octaves = octaves
        self._start_degree = start_degree

        if self._direction not in ['up', 'down', 'up_down', 'down_up']:
            raise ValueError(f"Invalid direction: {direction}. Must be 'up', 'down', 'up_down', or 'down_up'")

        self._notes = self._generate_arpeggio()

    @property
    def source(self) -> Union[Chord, Scale]:
        """Get the source chord or scale."""
        return self._source

    @property
    def direction(self) -> str:
        """Get the arpeggio direction."""
        return self._direction

    @property
    def notes(self) -> List[Note]:
        """Get all notes in the arpeggio."""
        return self._notes.copy()

    @property
    def note_names(self) -> List[str]:
        """Get note names in the arpeggio."""
        return [note.name for note in self._notes]

    @property
    def semitones(self) -> List[int]:
        """Get semitone values of all notes in the arpeggio."""
        return [note.semitone for note in self._notes]

    def _generate_arpeggio(self) -> List[Note]:
        """Generate the arpeggio pattern based on source and direction."""
        if isinstance(self._source, Chord):
            return self._generate_from_chord()
        elif isinstance(self._source, Scale):
            return self._generate_from_scale()
        else:
            raise ValueError("Source must be a Chord or Scale object")

    def _generate_from_chord(self) -> List[Note]:
        """Generate arpeggio from a chord."""
        base_notes = self._source.notes.copy()

        # Add octave duplication for multi-octave arpeggios
        if self._octaves > 1:
            for octave in range(1, self._octaves):
                for note in base_notes:
                    transposed = note.transpose(octave * 12)
                    base_notes.append(transposed)

        # Apply direction
        if self._direction == 'up':
            pattern = base_notes
        elif self._direction == 'down':
            pattern = list(reversed(base_notes))
        elif self._direction == 'up_down':
            # Up and then down (including the top note in both directions)
            pattern = base_notes + list(reversed(base_notes))
        elif self._direction == 'down_up':
            # Down and then up (including the bottom note in both directions)
            reversed_notes = list(reversed(base_notes))
            pattern = reversed_notes + base_notes

        return pattern

    def _generate_from_scale(self) -> List[Note]:
        """Generate arpeggio from a scale."""
        # For scales, we typically play all notes in the scale
        scale_notes = self._source.notes.copy()

        # Add octaves
        if self._octaves > 1:
            for octave in range(1, self._octaves):
                for note in scale_notes:
                    transposed = note.transpose(octave * 12)
                    scale_notes.append(transposed)

        # Apply direction
        if self._direction == 'up':
            pattern = scale_notes
        elif self._direction == 'down':
            pattern = list(reversed(scale_notes))
        elif self._direction == 'up_down':
            pattern = scale_notes + list(reversed(scale_notes))
        elif self._direction == 'down_up':
            reversed_notes = list(reversed(scale_notes))
            pattern = reversed_notes + scale_notes

        return pattern

    def get_subset(self, degrees: List[int]) -> 'Arpeggio':
        """
        Create a subset arpeggio using specific degrees.

        Args:
            degrees: List of degrees to include (1-based for scales, 0-based for chords)

        Returns:
            New Arpeggio object with subset of notes
        """
        subset_notes = []

        for degree in degrees:
            if isinstance(self._source, Scale):
                # Scale degrees are 1-based
                try:
                    note = self._source.get_degree(degree)
                    subset_notes.append(note)
                except IndexError:
                    continue
            else:
                # Chord notes are 0-based
                index = degree - 1 if degree > 0 else degree
                if 0 <= index < len(self._source):
                    subset_notes.append(self._source[index])

        # Create a new arpeggio from the subset
        subset_arpeggio = Arpeggio.__new__(Arpeggio)
        subset_arpeggio._source = self._source
        subset_arpeggio._direction = self._direction
        subset_arpeggio._octaves = 1  # Reset octaves for subset
        subset_arpeggio._start_degree = self._start_degree
        subset_arpeggio._notes = subset_notes

        return subset_arpeggio

    def transpose(self, semitones: int) -> 'Arpeggio':
        """
        Transpose the arpeggio by a given number of semitones.

        Args:
            semitones: Number of semitones to transpose

        Returns:
            New Arpeggio object with transposed notes
        """
        transposed_source = self._source.transpose(semitones)

        arpeggio = Arpeggio(transposed_source, self._direction,
                          self._octaves, self._start_degree)
        return arpeggio

    def change_direction(self, new_direction: str) -> 'Arpeggio':
        """
        Change the direction of the arpeggio.

        Args:
            new_direction: New direction ('up', 'down', 'up_down', 'down_up')

        Returns:
            New Arpeggio object with changed direction
        """
        return Arpeggio(self._source, new_direction,
                       self._octaves, self._start_degree)

    def get_guitar_positions(self, capo: int = 0) -> List[List[tuple]]:
        """
        Get guitar positions for playing the arpeggio.

        Args:
            capo: Capo position

        Returns:
            List of positions, each containing (string, fret) tuples
        """
        # This is a simplified guitar position calculator
        # In a real implementation, this would be much more sophisticated

        positions = []

        # Basic guitar string tunings (EADGBE)
        string_notes = ['E', 'A', 'D', 'G', 'B', 'E']  # Low to high

        for note in self._notes:
            note_positions = []

            for string_num, string_note in enumerate(string_notes):
                string_note_obj = Note(string_note)

                # Calculate fret position
                interval = string_note_obj.interval_to(note)
                if interval >= 0:  # Note is reachable on this string
                    fret = interval
                    if capo > 0:
                        fret += capo
                    if fret <= 24:  # Reasonable fret limit
                        note_positions.append((string_num + 1, fret))  # 1-based string numbering

            if note_positions:
                positions.append(note_positions)

        return positions

    def __str__(self) -> str:
        """String representation of the arpeggio."""
        source_name = str(self._source)
        return f"{source_name} Arpeggio ({self._direction})"

    def __repr__(self) -> str:
        """Detailed string representation for debugging."""
        return f"Arpeggio(source={self._source}, direction='{self._direction}')"

    def __eq__(self, other) -> bool:
        """Check equality based on source and direction."""
        if isinstance(other, Arpeggio):
            return (self._source == other._source and
                    self._direction == other._direction)
        return False

    def __len__(self) -> int:
        """Get the number of notes in the arpeggio."""
        return len(self._notes)

    def __getitem__(self, index: int) -> Note:
        """Get note at index."""
        return self._notes[index]

    def __iter__(self):
        """Iterate over notes in the arpeggio."""
        return iter(self._notes)
