"""
Note system module for the music theory engine.

This module provides utilities for working with musical notes,
including chromatic scale generation, note conversion, and
music theory operations on notes.
"""

from typing import List, Union, Optional

# Import with proper path handling
import sys
import os

# Ensure parent directory is in path
parent_dir = os.path.dirname(os.path.dirname(__file__))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from models.note import Note
from utils.constants import (
    NATURAL_NOTES, NOTE_TO_SEMITONE, SEMITONE_TO_NOTES,
    ENHARMONIC_EQUIVALENTS
)


class NoteSystem:
    """
    Utility class for working with the musical note system.

    Provides methods for chromatic scale operations, note conversions,
    and music theory calculations involving notes.
    """

    @staticmethod
    def chromatic_scale(start_note: Union[str, int, Note] = 'C',
                       octaves: int = 1) -> List[Note]:
        """
        Generate a chromatic scale starting from a given note.

        Args:
            start_note: Starting note
            octaves: Number of octaves to generate

        Returns:
            List of Note objects in chromatic order
        """
        start = Note(start_note)
        notes = []

        for octave in range(octaves):
            for semitone in range(12):
                note_semitone = (start.semitone + semitone + octave * 12) % 12
                note = Note.from_semitone(note_semitone, use_sharps=start.is_sharp)
                notes.append(note)

        # Remove duplicates at octave boundaries
        if octaves > 1:
            notes = notes[:-1]  # Remove the duplicated starting note

        return notes

    @staticmethod
    def circle_of_fifths(start_note: Union[str, int, Note] = 'C',
                        direction: str = 'clockwise') -> List[Note]:
        """
        Generate the circle of fifths starting from a given note.

        Args:
            start_note: Starting note
            direction: 'clockwise' (fifths) or 'counterclockwise' (fourths)

        Returns:
            List of Note objects in circle of fifths order
        """
        start = Note(start_note)
        notes = [start]

        interval = 7 if direction == 'clockwise' else 5  # 5th up or 4th up (5th down)

        current = start
        for _ in range(11):  # 12 notes total
            current = current.transpose(interval)
            notes.append(current)

        return notes

    @staticmethod
    def get_enharmonic_equivalents(note: Union[str, int, Note]) -> List[Note]:
        """
        Get all enharmonic equivalents of a note.

        Args:
            note: Note to find equivalents for

        Returns:
            List of enharmonically equivalent Note objects
        """
        n = Note(note)
        return n.get_all_enharmonics()

    @staticmethod
    def find_notes_by_interval(root: Union[str, int, Note],
                             interval_semitones: int) -> List[Note]:
        """
        Find all notes that are a given interval from a root note.

        Args:
            root: Root note
            interval_semitones: Interval in semitones

        Returns:
            List of Note objects at the specified interval
        """
        root_note = Note(root)
        target_semitone = (root_note.semitone + interval_semitones) % 12

        return [Note.from_semitone(target_semitone, use_sharps=root_note.is_sharp),
                Note.from_semitone(target_semitone, use_sharps=not root_note.is_sharp)]

    @staticmethod
    def get_scale_degrees(root: Union[str, int, Note],
                         scale_notes: List[Union[str, int, Note]]) -> List[int]:
        """
        Get scale degrees for a list of notes relative to a root.

        Args:
            root: Root note
            scale_notes: List of notes in the scale

        Returns:
            List of scale degrees (1-7) corresponding to the notes
        """
        root_note = Note(root)
        degrees = []

        for note in scale_notes:
            note_obj = Note(note)
            interval = root_note.interval_to(note_obj)

            # Convert semitone interval to scale degree (approximate)
            # This is a simplification - real scale degree calculation
            # would depend on the specific scale
            degree = (interval % 12) + 1
            if degree > 7:
                degree -= 7  # Wrap around for larger intervals
            degrees.append(degree)

        return degrees

    @staticmethod
    def transpose_notes(notes: List[Union[str, int, Note]],
                       semitones: int) -> List[Note]:
        """
        Transpose a list of notes by a given number of semitones.

        Args:
            notes: List of notes to transpose
            semitones: Number of semitones to transpose

        Returns:
            List of transposed Note objects
        """
        return [Note(note).transpose(semitones) for note in notes]

    @staticmethod
    def notes_to_semitones(notes: List[Union[str, int, Note]]) -> List[int]:
        """
        Convert a list of notes to their semitone values.

        Args:
            notes: List of notes

        Returns:
            List of semitone values
        """
        return [Note(note).semitone for note in notes]

    @staticmethod
    def semitones_to_notes(semitones: List[int],
                          use_sharps: bool = True) -> List[Note]:
        """
        Convert a list of semitone values to Note objects.

        Args:
            semitones: List of semitone values
            use_sharps: Whether to use sharp notation for accidentals

        Returns:
            List of Note objects
        """
        return [Note.from_semitone(s, use_sharps) for s in semitones]

    @staticmethod
    def get_note_frequency(note: Union[str, int, Note],
                          octave: int = 4,
                          concert_pitch: float = 440.0) -> float:
        """
        Calculate the frequency of a note in a given octave.

        Args:
            note: Note
            octave: Octave number (A4 = 440Hz)
            concert_pitch: Reference frequency for A4

        Returns:
            Frequency in Hz
        """
        n = Note(note)

        # A4 is the reference (semitone 9 in octave 4)
        a4_semitone = 9
        a4_octave = 4

        # Calculate semitone distance from A4
        octave_diff = octave - a4_octave
        semitone_diff = n.semitone - a4_semitone
        total_semitones = octave_diff * 12 + semitone_diff

        # Calculate frequency using equal temperament
        return concert_pitch * (2 ** (total_semitones / 12))

    @staticmethod
    def frequency_to_note(frequency: float,
                         concert_pitch: float = 440.0) -> tuple[Note, int]:
        """
        Convert a frequency to the nearest note and octave.

        Args:
            frequency: Frequency in Hz
            concert_pitch: Reference frequency for A4

        Returns:
            Tuple of (Note, octave)
        """
        if frequency <= 0:
            raise ValueError("Frequency must be positive")

        # Calculate semitones from A4
        semitones_from_a4 = round(12 * (frequency / concert_pitch).log2())

        # A4 is semitone 9 in octave 4
        total_semitones = 9 + semitones_from_a4
        octave = 4 + (total_semitones // 12)
        semitone = total_semitones % 12

        note = Note.from_semitone(semitone)
        return note, octave

    @staticmethod
    def validate_note_name(note_name: str) -> bool:
        """
        Validate if a string is a valid note name.

        Args:
            note_name: Note name to validate

        Returns:
            True if valid, False otherwise
        """
        try:
            Note(note_name)
            return True
        except ValueError:
            return False

    @staticmethod
    def normalize_note_name(note_name: str) -> str:
        """
        Normalize a note name to standard format.

        Args:
            note_name: Note name to normalize

        Returns:
            Normalized note name
        """
        note = Note(note_name)
        return note.name


# Convenience functions
def chromatic_scale(start_note: Union[str, int, Note] = 'C',
                   octaves: int = 1) -> List[Note]:
    """Generate a chromatic scale."""
    return NoteSystem.chromatic_scale(start_note, octaves)

def circle_of_fifths(start_note: Union[str, int, Note] = 'C',
                    direction: str = 'clockwise') -> List[Note]:
    """Generate the circle of fifths."""
    return NoteSystem.circle_of_fifths(start_note, direction)

def get_enharmonic_equivalents(note: Union[str, int, Note]) -> List[Note]:
    """Get enharmonic equivalents."""
    return NoteSystem.get_enharmonic_equivalents(note)

def transpose_notes(notes: List[Union[str, int, Note]],
                   semitones: int) -> List[Note]:
    """Transpose a list of notes."""
    return NoteSystem.transpose_notes(notes, semitones)
