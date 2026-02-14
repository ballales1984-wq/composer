"""
Chord construction module for the music theory engine.

This module provides functions and classes for building all types of musical chords:
- Triads (major, minor, diminished, augmented)
- Seventh chords (maj7, dom7, min7, dim7, min7b5)
- Extended chords (9, 11, 13 and their variations)
- Added tone chords (6, 6/9, sus2, sus4)
- Quartal and quintal harmonies
"""

from typing import Union, List, Optional
import logging

# Import validators for robust input validation
try:
    from utils.validators import validate_note_input, validate_chord_quality, validate_intervals
except ImportError:
    # Fallback if validators not available
    def validate_note_input(value):
        return isinstance(value, (str, int, Note)), ""

    def validate_chord_quality(quality):
        return isinstance(quality, str) and quality.strip() != "", ""

    def validate_intervals(intervals):
        return isinstance(intervals, list) and len(intervals) > 0, ""

# Import with proper path handling
import sys
import os

# Ensure parent directory is in path
parent_dir = os.path.dirname(os.path.dirname(__file__))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from models.note import Note
from models.chord import Chord

# Import centralized constants
try:
    from utils.constants import CHORD_INTERVALS
except ImportError:
    # Fallback to local definition if import fails
    CHORD_INTERVALS = {
        'maj': [0, 4, 7], 'min': [0, 3, 7], 'dim': [0, 3, 6], 'aug': [0, 4, 8],
        'sus2': [0, 2, 7], 'sus4': [0, 5, 7], '5': [0, 7],
        'maj7': [0, 4, 7, 11], 'dom7': [0, 4, 7, 10], 'min7': [0, 3, 7, 10],
        'dim7': [0, 3, 6, 9], 'min7b5': [0, 3, 6, 10], 'maj7b5': [0, 4, 6, 11],
        '7sus4': [0, 5, 7, 10], '7b9': [0, 4, 7, 10, 13],
        '9': [0, 4, 7, 10, 14], 'min9': [0, 3, 7, 10, 14], 'maj9': [0, 4, 7, 11, 14],
        '11': [0, 4, 7, 10, 14, 17], 'min11': [0, 3, 7, 10, 14, 17],
        'maj11': [0, 4, 7, 11, 14, 17], '13': [0, 4, 7, 10, 14, 21],
        'min13': [0, 3, 7, 10, 14, 21], 'maj13': [0, 4, 7, 11, 14, 21],
        '6': [0, 4, 7, 9], 'min6': [0, 3, 7, 9], '6/9': [0, 4, 7, 9, 14],
        '7#11': [0, 4, 7, 10, 18],
        'quartal': [0, 5, 10, 15], 'quintal': [0, 7, 14, 21],
    }

class ChordBuilder:
    """
    Builder class for creating musical chords of all types.

    This class provides static methods for constructing chords
    with proper music theory rules and interval relationships.
    """

    # Triads
    @staticmethod
    def major(root: Union[str, int, Note]) -> Chord:
        """Build a major triad."""
        return Chord(root, 'maj')

    @staticmethod
    def minor(root: Union[str, int, Note]) -> Chord:
        """Build a minor triad."""
        return Chord(root, 'min')

    @staticmethod
    def diminished(root: Union[str, int, Note]) -> Chord:
        """Build a diminished triad."""
        return Chord(root, 'dim')

    @staticmethod
    def augmented(root: Union[str, int, Note]) -> Chord:
        """Build an augmented triad."""
        return Chord(root, 'aug')

    # Seventh chords
    @staticmethod
    def major7(root: Union[str, int, Note]) -> Chord:
        """Build a major 7th chord."""
        return Chord(root, 'maj7')

    @staticmethod
    def dominant7(root: Union[str, int, Note]) -> Chord:
        """Build a dominant 7th chord."""
        return Chord(root, 'dom7')

    @staticmethod
    def minor7(root: Union[str, int, Note]) -> Chord:
        """Build a minor 7th chord."""
        return Chord(root, 'min7')

    @staticmethod
    def diminished7(root: Union[str, int, Note]) -> Chord:
        """Build a diminished 7th chord."""
        return Chord(root, 'dim7')

    @staticmethod
    def minor7b5(root: Union[str, int, Note]) -> Chord:
        """Build a minor 7th flat 5 chord (half-diminished)."""
        return Chord(root, 'min7b5')

    @staticmethod
    def major7b5(root: Union[str, int, Note]) -> Chord:
        """Build a major 7th flat 5 chord."""
        return Chord(root, 'maj7b5')

    # Extended chords
    @staticmethod
    def dom9(root: Union[str, int, Note]) -> Chord:
        """Build a dominant 9th chord."""
        return Chord(root, '9')

    @staticmethod
    def major9(root: Union[str, int, Note]) -> Chord:
        """Build a major 9th chord."""
        return Chord(root, 'maj9')

    @staticmethod
    def minor9(root: Union[str, int, Note]) -> Chord:
        """Build a minor 9th chord."""
        return Chord(root, 'min9')

    @staticmethod
    def dom11(root: Union[str, int, Note]) -> Chord:
        """Build a dominant 11th chord."""
        return Chord(root, '11')

    @staticmethod
    def major11(root: Union[str, int, Note]) -> Chord:
        """Build a major 11th chord."""
        return Chord(root, 'maj11')

    @staticmethod
    def minor11(root: Union[str, int, Note]) -> Chord:
        """Build a minor 11th chord."""
        return Chord(root, 'min11')

    @staticmethod
    def dom13(root: Union[str, int, Note]) -> Chord:
        """Build a dominant 13th chord."""
        return Chord(root, '13')

    @staticmethod
    def major13(root: Union[str, int, Note]) -> Chord:
        """Build a major 13th chord."""
        return Chord(root, 'maj13')

    @staticmethod
    def minor13(root: Union[str, int, Note]) -> Chord:
        """Build a minor 13th chord."""
        return Chord(root, 'min13')

    # Added tone chords
    @staticmethod
    def sixth(root: Union[str, int, Note]) -> Chord:
        """Build a major 6th chord."""
        return Chord(root, '6')

    @staticmethod
    def minor6(root: Union[str, int, Note]) -> Chord:
        """Build a minor 6th chord."""
        return Chord(root, 'min6')

    @staticmethod
    def six_nine(root: Union[str, int, Note]) -> Chord:
        """Build a 6/9 chord."""
        return Chord(root, '6/9')

    @staticmethod
    def suspended2(root: Union[str, int, Note]) -> Chord:
        """Build a suspended 2nd chord."""
        return Chord(root, 'sus2')

    @staticmethod
    def suspended4(root: Union[str, int, Note]) -> Chord:
        """Build a suspended 4th chord."""
        return Chord(root, 'sus4')

    @staticmethod
    def seven_sus4(root: Union[str, int, Note]) -> Chord:
        """Build a 7th suspended 4th chord."""
        return Chord(root, '7sus4')

    @staticmethod
    def power_chord(root: Union[str, int, Note]) -> Chord:
        """Build a power chord (5th)."""
        return Chord(root, '5')

    # Altered chords
    @staticmethod
    def seven_flat9(root: Union[str, int, Note]) -> Chord:
        """Build a 7th flat 9 chord."""
        return Chord(root, '7b9')

    @staticmethod
    def seven_sharp11(root: Union[str, int, Note]) -> Chord:
        """Build a 7th sharp 11 chord."""
        return Chord(root, '7#11')

    # Quartal and quintal harmonies
    @staticmethod
    def quartal(root: Union[str, int, Note]) -> Chord:
        """Build a quartal harmony chord."""
        return Chord(root, 'quartal')

    @staticmethod
    def quintal(root: Union[str, int, Note]) -> Chord:
        """Build a quintal harmony chord."""
        return Chord(root, 'quintal')

    @staticmethod
    def from_quality(root: Union[str, int, Note], quality: str) -> Chord:
        """
        Build a chord from a root note and quality string.

        Args:
            root: Root note
            quality: Chord quality (e.g., 'maj', 'min7', 'dim7')

        Returns:
            Chord object

        Raises:
            ValueError: If quality is not recognized
        """
        return Chord(root, quality)

    @staticmethod
    def from_intervals(root: Union[str, int, Note], intervals: List[int],
                      name: str = "Custom Chord") -> Chord:
        """
        Build a custom chord from a list of intervals.

        Args:
            root: Root note
            intervals: List of intervals in semitones (relative to root)
            name: Name for the custom chord (for display purposes)

        Returns:
            Custom Chord object

        Raises:
            ValueError: If intervals are invalid
            TypeError: If input types are incorrect
        """
        logger = logging.getLogger(__name__)

        # Validate inputs using robust validators
        is_valid, error_msg = validate_note_input(root)
        if not is_valid:
            logger.error(f"Invalid root note '{root}': {error_msg}")
            raise ValueError(f"Invalid root note: {error_msg}")

        is_valid, error_msg = validate_intervals(intervals)
        if not is_valid:
            logger.error(f"Invalid intervals for chord '{name}': {error_msg}")
            raise ValueError(f"Invalid intervals: {error_msg}")

        # Sanitize name
        try:
            from utils.validators import sanitize_input
            name = sanitize_input(name, 50)  # Max 50 chars for chord name
        except ImportError:
            name = str(name)[:50]  # Fallback sanitization

        # Thread-safe: pass intervals directly instead of modifying global dict
        custom_type = f"custom_{name.replace(' ', '_').lower()}"
        chord = Chord(root, custom_type, custom_intervals=intervals)

        logger.info(f"Created custom chord '{name}' with {len(intervals)} intervals")
        return chord

    @staticmethod
    def get_all_chord_qualities() -> List[str]:
        """
        Get a list of all available chord qualities.

        Returns:
            List of chord quality strings
        """
        return list(CHORD_INTERVALS.keys())

    @staticmethod
    def get_chords_for_note(root: Union[str, int, Note]) -> List[Chord]:
        """
        Get all available chords starting from a given root note.

        Args:
            root: Root note

        Returns:
            List of all Chord objects for that root
        """
        chords = []
        for quality in CHORD_INTERVALS.keys():
            try:
                chords.append(Chord(root, quality))
            except (ValueError, TypeError, KeyError) as e:
                # Skip invalid chord constructions with specific error types
                logger = logging.getLogger(__name__)
                logger.warning(f"Failed to create chord {quality} for root {root}: {e}")
                continue
            except Exception as e:
                # Log unexpected errors but continue processing
                logger = logging.getLogger(__name__)
                logger.error(f"Unexpected error creating chord {quality}: {e}", exc_info=True)
                continue
        return chords

    @staticmethod
    def get_diatonic_chords(scale: 'Scale') -> List[Chord]:
        """
        Get all diatonic chords for a given scale.

        Args:
            scale: Scale object

        Returns:
            List of diatonic chords (one for each scale degree)
        """
        chords = []
        for degree in range(1, len(scale) + 1):
            try:
                chord = scale.get_triad(degree)
                chords.append(chord)
            except:
                continue
        return chords

    @staticmethod
    def get_chord_progression(chords: List[Union[str, Chord]]) -> List[Chord]:
        """
        Create a chord progression from a list of chord specifications.

        Args:
            chords: List of chord strings (e.g., 'C', 'Dm', 'G7') or Chord objects

        Returns:
            List of Chord objects
        """
        progression = []

        for chord_spec in chords:
            if isinstance(chord_spec, Chord):
                progression.append(chord_spec)
            elif isinstance(chord_spec, str):
                # Parse chord string like 'Cmaj7', 'Dmin', 'G7'
                progression.append(ChordBuilder.parse_chord_string(chord_spec))
            else:
                raise ValueError(f"Invalid chord specification: {chord_spec}")

        return progression

    @staticmethod
    def parse_chord_string(chord_string: str) -> Chord:
        """
        Parse a chord string into a Chord object.

        Args:
            chord_string: Chord string (e.g., 'Cmaj7', 'Bbmin', 'F#7')

        Returns:
            Chord object

        Raises:
            ValueError: If chord string cannot be parsed
        """
        # Simple parser - can be enhanced for more complex chords
        chord_string = chord_string.strip()

        # Find where the note name ends and quality begins
        i = 0
        while i < len(chord_string) and chord_string[i].isalpha():
            i += 1

        if i == 0:
            raise ValueError(f"Invalid chord string: {chord_string}")

        root_name = chord_string[:i]
        quality_part = chord_string[i:].lower()

        # Map common quality abbreviations to our internal format
        quality_map = {
            '': 'maj',  # Just 'C' means C major
            'm': 'min',
            'maj': 'maj',
            'maj7': 'maj7',
            'm7': 'min7',
            '7': 'dom7',
            'dim': 'dim',
            'dim7': 'dim7',
            'aug': 'aug',
            'sus2': 'sus2',
            'sus4': 'sus4',
            '6': '6',
            'm6': 'min6',
            '9': '9',
            'm9': 'min9',
            'maj9': 'maj9',
            '11': '11',
            'm11': 'min11',
            'maj11': 'maj11',
            '13': '13',
            'm13': 'min13',
            'maj13': 'maj13',
            '7sus4': '7sus4',
            'ø7': 'min7b5',
            'm7b5': 'min7b5'
        }

        quality = quality_map.get(quality_part, quality_part)

        if quality not in CHORD_INTERVALS:
            raise ValueError(f"Unknown chord quality: {quality_part}")

        return Chord(root_name, quality)


# Convenience functions for quick chord creation
def maj(root: Union[str, int, Note]) -> Chord:
    """Create a major triad."""
    return ChordBuilder.major(root)

def min(root: Union[str, int, Note]) -> Chord:
    """Create a minor triad."""
    return ChordBuilder.minor(root)

def dom7(root: Union[str, int, Note]) -> Chord:
    """Create a dominant 7th chord."""
    return ChordBuilder.dominant7(root)

def min7(root: Union[str, int, Note]) -> Chord:
    """Create a minor 7th chord."""
    return ChordBuilder.minor7(root)

def maj7(root: Union[str, int, Note]) -> Chord:
    """Create a major 7th chord."""
    return ChordBuilder.major7(root)

def dim7(root: Union[str, int, Note]) -> Chord:
    """Create a diminished 7th chord."""
    return ChordBuilder.diminished7(root)
