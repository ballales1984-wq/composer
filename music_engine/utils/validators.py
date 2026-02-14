"""
Input validation utilities for Music Theory Engine.

Provides robust validation functions with detailed error messages
for all musical input types.
"""

import re
from typing import Union, Tuple, Optional, List
from utils.logging_config import get_logger
from models.note import Note

logger = get_logger(__name__)

# Regular expressions for note parsing
NOTE_PATTERN = re.compile(r'^([A-Ga-g])(#|b|♯|♭)?(\d)?$')
CHORD_PATTERN = re.compile(r'^([A-Ga-g])(#|b|♯|♭)?((maj|min|dim|aug|sus|dom|maj7|min7|dim7|7|9|11|13|6)+)?$')

# Valid note names and accidentals
VALID_NOTES = {'C', 'D', 'E', 'F', 'G', 'A', 'B'}
VALID_ACCIDENTALS = {'#', 'b', '♯', '♭', ''}
VALID_OCTAVES = set(range(-1, 10))  # Octaves from -1 to 9


def validate_note_input(value) -> Tuple[bool, str]:
    """
    Validate note input with detailed error messages.

    Args:
        value: Input to validate (Note, str, or int)

    Returns:
        Tuple of (is_valid, error_message)
    """
    if isinstance(value, Note):
        return True, ""

    if isinstance(value, str):
        return validate_note_string(value)

    if isinstance(value, int):
        if 0 <= value <= 11:
            return True, ""
        else:
            return False, f"Semitone value must be between 0-11, got {value}"

    return False, f"Invalid note type: {type(value)}. Expected Note, str, or int (0-11)"


def validate_note_string(note_string: str) -> Tuple[bool, str]:
    """
    Validate a note string with detailed parsing.

    Args:
        note_string: String to validate (e.g., "C4", "F#3", "Bb")

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not note_string or not isinstance(note_string, str):
        return False, "Note string cannot be empty and must be a string"

    note_string = note_string.strip()
    if not note_string:
        return False, "Note string cannot be empty after stripping"

    if len(note_string) > 4:
        return False, f"Note string too long: '{note_string}' (max 4 characters)"

    match = NOTE_PATTERN.match(note_string)
    if not match:
        return False, f"Invalid note format: '{note_string}'. Expected format like 'C4', 'F#3', or 'Bb'"

    note_name, accidental, octave_str = match.groups()

    # Validate note name
    if note_name.upper() not in VALID_NOTES:
        return False, f"Invalid note name '{note_name}'. Must be A-G or a-g"

    # Validate accidental
    if accidental not in VALID_ACCIDENTALS:
        return False, f"Invalid accidental '{accidental}'. Must be #, b, ♯, ♭, or empty"

    # Validate octave
    if octave_str is not None:
        try:
            octave = int(octave_str)
            if octave not in VALID_OCTAVES:
                return False, f"Invalid octave {octave}. Must be between -1 and 9"
        except ValueError:
            return False, f"Invalid octave format: '{octave_str}'"

    return True, ""


def validate_chord_string(chord_string: str) -> Tuple[bool, str]:
    """
    Validate chord string with detailed error messages.

    Args:
        chord_string: Chord string to validate (e.g., "Cmaj7", "F#min", "Bb")

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not chord_string or not isinstance(chord_string, str):
        return False, "Chord string cannot be empty and must be a string"

    chord_string = chord_string.strip()
    if not chord_string:
        return False, "Chord string cannot be empty after stripping"

    if len(chord_string) > 10:
        return False, f"Chord string too long: '{chord_string}' (max 10 characters)"

    # Basic validation - check if it starts with a valid note
    first_char = chord_string[0].upper()
    if first_char not in VALID_NOTES:
        return False, f"Chord must start with a valid note (A-G), got '{first_char}'"

    # Check for valid accidental after first character
    remaining = chord_string[1:]
    if remaining and remaining[0] in {'#', 'b', '♯', '♭'}:
        remaining = remaining[1:]

    # Check for octave at the end
    if remaining and remaining[-1].isdigit():
        try:
            octave = int(remaining[-1])
            if octave not in VALID_OCTAVES:
                return False, f"Invalid octave {octave} in chord '{chord_string}'"
            remaining = remaining[:-1]
        except ValueError:
            return False, f"Invalid octave format in chord '{chord_string}'"

    # Remaining should be chord quality symbols
    valid_qualities = {
        'maj', 'min', 'dim', 'aug', 'sus', 'dom', 'maj7', 'min7', 'dim7', '7',
        '9', '11', '13', '6', 'min9', 'maj9', 'min11', 'maj11', 'min13', 'maj13',
        '6/9', '7sus4', '7b9', '7#11', 'min7b5', 'maj7b5', '5'
    }

    # Simple check - if remaining contains only valid characters
    if remaining:
        # Allow some common chord symbols
        remaining_lower = remaining.lower()
        if not any(quality in remaining_lower for quality in valid_qualities):
            # Allow if it contains only valid chord characters
            valid_chars = set('majdimnaug7sus9/♭♯#b0123456789')
            if not all(c.lower() in valid_chars for c in remaining):
                return False, f"Invalid chord quality in '{chord_string}': '{remaining}'"

    return True, ""


def validate_scale_type(scale_type: str) -> Tuple[bool, str]:
    """
    Validate scale type string.

    Args:
        scale_type: Scale type to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not scale_type or not isinstance(scale_type, str):
        return False, "Scale type cannot be empty and must be a string"

    scale_type = scale_type.strip()
    if not scale_type:
        return False, "Scale type cannot be empty after stripping"

    # Import here to avoid circular imports
    try:
        from utils.constants import SCALE_INTERVALS
        if scale_type in SCALE_INTERVALS:
            return True, ""
        else:
            available = ", ".join(sorted(SCALE_INTERVALS.keys()))
            return False, f"Unknown scale type '{scale_type}'. Available: {available}"
    except ImportError:
        # Fallback validation
        valid_types = {
            'major', 'minor_natural', 'minor_harmonic', 'minor_melodic',
            'dorian', 'phrygian', 'lydian', 'mixolydian', 'locrian',
            'pentatonic_major', 'pentatonic_minor', 'pentatonic_blues',
            'blues_major', 'blues_minor', 'whole_tone', 'chromatic',
            'diminished', 'augmented'
        }
        if scale_type in valid_types:
            return True, ""
        else:
            return False, f"Unknown scale type '{scale_type}'"


def validate_chord_quality(quality: str) -> Tuple[bool, str]:
    """
    Validate chord quality string.

    Args:
        quality: Chord quality to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not quality or not isinstance(quality, str):
        return False, "Chord quality cannot be empty and must be a string"

    quality = quality.strip()
    if not quality:
        return False, "Chord quality cannot be empty after stripping"

    # Import here to avoid circular imports
    try:
        from utils.constants import CHORD_INTERVALS
        if quality in CHORD_INTERVALS:
            return True, ""
        else:
            available = ", ".join(sorted(CHORD_INTERVALS.keys()))
            return False, f"Unknown chord quality '{quality}'. Available: {available}"
    except ImportError:
        # Fallback validation
        valid_qualities = {
            'maj', 'min', 'dim', 'aug', 'sus2', 'sus4', '5',
            'maj7', 'dom7', 'min7', 'dim7', 'min7b5', 'maj7b5', '7sus4',
            '9', 'min9', 'maj9', '11', 'min11', 'maj11', '13', 'min13', 'maj13',
            '6', 'min6', '6/9', '7b9', '7#11', 'quartal', 'quintal'
        }
        if quality in valid_qualities:
            return True, ""
        else:
            return False, f"Unknown chord quality '{quality}'"


def validate_intervals(intervals: List[int]) -> Tuple[bool, str]:
    """
    Validate interval list for scales or chords.

    Args:
        intervals: List of intervals in semitones

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not intervals:
        return False, "Intervals list cannot be empty"

    if not isinstance(intervals, list):
        return False, f"Intervals must be a list, got {type(intervals)}"

    if intervals[0] != 0:
        return False, f"Intervals must start with 0 (unison), got {intervals[0]}"

    for i, interval in enumerate(intervals):
        if not isinstance(interval, int):
            return False, f"Interval at position {i} must be an integer, got {type(interval)}"

        if interval < 0:
            return False, f"Interval at position {i} cannot be negative, got {interval}"

        if interval > 24:  # Allow up to 2 octaves
            return False, f"Interval at position {i} too large (>24 semitones), got {interval}"

    # Check for duplicates (should be monotonically increasing)
    if len(intervals) > 1:
        for i in range(1, len(intervals)):
            if intervals[i] <= intervals[i-1]:
                return False, f"Intervals must be monotonically increasing, but position {i} ({intervals[i]}) <= position {i-1} ({intervals[i-1]})"

    return True, ""


def validate_bpm(bpm: Union[int, float]) -> Tuple[bool, str]:
    """
    Validate BPM (beats per minute) value.

    Args:
        bpm: BPM value to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        bpm_float = float(bpm)
        if 20 <= bpm_float <= 300:
            return True, ""
        else:
            return False, f"BPM must be between 20-300, got {bpm_float}"
    except (ValueError, TypeError):
        return False, f"Invalid BPM format: {bpm}. Must be a number."


def sanitize_input(value: str, max_length: int = 100) -> str:
    """
    Sanitize text input by removing dangerous characters and limiting length.

    Args:
        value: Input string to sanitize
        max_length: Maximum allowed length

    Returns:
        Sanitized string
    """
    if not isinstance(value, str):
        return ""

    # Remove potentially dangerous characters
    dangerous_chars = ['<', '>', '&', '"', "'", '\\', '\n', '\r', '\t']
    for char in dangerous_chars:
        value = value.replace(char, '')

    # Limit length
    if len(value) > max_length:
        value = value[:max_length]

    return value.strip()


# Convenience functions for common validations
def validate_and_log(value, validator_func, context: str = ""):
    """
    Validate input and log result.

    Args:
        value: Value to validate
        validator_func: Validation function to use
        context: Context for logging

    Returns:
        Tuple of (is_valid, error_message)
    """
    is_valid, error_msg = validator_func(value)

    if not is_valid:
        logger.warning(f"Validation failed for {context}: {error_msg}")
    else:
        logger.debug(f"Validation passed for {context}")

    return is_valid, error_msg