"""
Music Mathematics Utilities

This module contains mathematical functions for music theory calculations.
"""

from typing import List, Optional
import math

def semitones_between_notes(note1: str, note2: str) -> int:
    """
    Calculate the number of semitones between two notes.

    Args:
        note1: First note (e.g., 'C')
        note2: Second note (e.g., 'D')

    Returns:
        Number of semitones between the notes
    """
    chromatic_scale = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

    try:
        idx1 = chromatic_scale.index(note1.upper())
        idx2 = chromatic_scale.index(note2.upper())
        return (idx2 - idx1) % 12
    except ValueError:
        return 0

def note_at_semitone_distance(note: str, semitones: int) -> str:
    """
    Find the note at a given semitone distance from a starting note.

    Args:
        note: Starting note
        semitones: Number of semitones to move

    Returns:
        The resulting note
    """
    chromatic_scale = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

    try:
        idx = chromatic_scale.index(note.upper())
        new_idx = (idx + semitones) % 12
        return chromatic_scale[new_idx]
    except ValueError:
        return note

def interval_to_semitones(interval: str) -> int:
    """
    Convert interval name to semitones.

    Args:
        interval: Interval name (e.g., 'major3', 'perfect5')

    Returns:
        Number of semitones
    """
    interval_map = {
        'unison': 0,
        'minor2': 1,
        'major2': 2,
        'minor3': 3,
        'major3': 4,
        'perfect4': 5,
        'tritone': 6,
        'perfect5': 7,
        'minor6': 8,
        'major6': 9,
        'minor7': 10,
        'major7': 11,
        'octave': 12
    }

    return interval_map.get(interval.lower(), 0)

def frequency_to_note_name(frequency: float) -> str:
    """
    Convert frequency to note name (approximate).

    Args:
        frequency: Frequency in Hz

    Returns:
        Note name
    """
    # A4 = 440 Hz
    if frequency <= 0:
        return 'C'

    # Calculate semitone offset from A4
    semitones = round(12 * math.log2(frequency / 440))

    # Convert to note name
    chromatic_scale = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']
    note_idx = (semitones + 9) % 12  # A is at index 0, offset by 9 for A4

    octave = 4 + (semitones // 12)

    return f"{chromatic_scale[note_idx]}{octave}"

def note_name_to_frequency(note: str, octave: int = 4) -> float:
    """
    Convert note name to frequency.

    Args:
        note: Note name (e.g., 'A', 'C#')
        octave: Octave number

    Returns:
        Frequency in Hz
    """
    # A4 = 440 Hz
    chromatic_scale = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

    try:
        note_idx = chromatic_scale.index(note.upper())
        # C4 is 261.63 Hz, A4 is 440 Hz
        # Calculate semitones from C4
        semitones_from_c4 = (octave - 4) * 12 + note_idx
        return 261.63 * (2 ** (semitones_from_c4 / 12))
    except ValueError:
        return 440.0  # Default to A4

def transpose_notes(notes: List[str], semitones: int) -> List[str]:
    """
    Transpose a list of notes by a given number of semitones.

    Args:
        notes: List of note names
        semitones: Number of semitones to transpose

    Returns:
        List of transposed note names
    """
    return [note_at_semitone_distance(note, semitones) for note in notes]

def find_common_tones(notes1: List[str], notes2: List[str]) -> List[str]:
    """
    Find common notes between two note collections.

    Args:
        notes1: First list of notes
        notes2: Second list of notes

    Returns:
        List of common notes
    """
    return list(set(notes1) & set(notes2))

def calculate_scale_degree(root_note: str, target_note: str) -> int:
    """
    Calculate the scale degree of a note relative to a root.

    Args:
        root_note: Root note
        target_note: Target note

    Returns:
        Scale degree (1-7)
    """
    semitones = semitones_between_notes(root_note, target_note)
    scale_degrees = [0, 2, 4, 5, 7, 9, 11]  # Major scale intervals

    if semitones in scale_degrees:
        return scale_degrees.index(semitones) + 1
    else:
        return 0  # Not a diatonic note
