"""
Scale construction module for the music theory engine.

This module provides functions and classes for building all types of musical scales:
- Major and minor scales (natural, harmonic, melodic)
- Modal scales (Dorian, Phrygian, Lydian, Mixolydian, Locrian)
- Pentatonic scales (major and minor)
- Blues scales
- Other common scales (whole tone, chromatic, diminished, augmented)
"""

from typing import Union, List, Optional
import logging

# Import validators for robust input validation
try:
    from utils.validators import validate_note_input, validate_scale_type, validate_intervals
except ImportError:
    # Fallback if validators not available
    def validate_note_input(value):
        return isinstance(value, (str, int, Note)), ""

    def validate_scale_type(scale_type):
        return isinstance(scale_type, str) and scale_type.strip() != "", ""

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
from models.scale import Scale

# Import centralized constants
try:
    from utils.constants import SCALE_INTERVALS
except ImportError:
    # Fallback to local definition if import fails
    SCALE_INTERVALS = {
        'major': [0, 2, 4, 5, 7, 9, 11],
        'ionian': [0, 2, 4, 5, 7, 9, 11],
        'minor_natural': [0, 2, 3, 5, 7, 8, 10],
        'aeolian': [0, 2, 3, 5, 7, 8, 10],
        'minor_harmonic': [0, 2, 3, 5, 7, 8, 11],
        'minor_melodic': [0, 2, 3, 5, 7, 9, 11],
        'dorian': [0, 2, 3, 5, 7, 9, 10],
        'phrygian': [0, 1, 3, 5, 7, 8, 10],
        'lydian': [0, 2, 4, 6, 7, 9, 11],
        'mixolydian': [0, 2, 4, 5, 7, 9, 10],
        'locrian': [0, 1, 3, 5, 6, 8, 10],
        'pentatonic_major': [0, 2, 4, 7, 9],
        'pentatonic_minor': [0, 3, 5, 7, 10],
        'pentatonic_blues': [0, 3, 5, 6, 7, 10],
        'blues_major': [0, 2, 3, 4, 7, 9],
        'blues_minor': [0, 3, 5, 6, 7, 10],
        'whole_tone': [0, 2, 4, 6, 8, 10],
        'chromatic': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
        'diminished': [0, 2, 3, 5, 6, 8, 9, 11],
        'augmented': [0, 3, 4, 7, 8, 11],
    }

class ScaleBuilder:
    """
    Builder class for creating musical scales of all types.

    This class provides static methods for constructing scales
    with proper music theory rules and interval relationships.
    """

    @staticmethod
    def major(root: Union[str, int, Note]) -> Scale:
        """
        Build a major scale.

        Args:
            root: Root note

        Returns:
            Major scale starting from root
        """
        return Scale(root, 'major')

    @staticmethod
    def minor(root: Union[str, int, Note], variation: str = 'natural') -> Scale:
        """
        Build a minor scale.

        Args:
            root: Root note
            variation: Type of minor scale ('natural', 'harmonic', 'melodic')

        Returns:
            Minor scale of specified variation
        """
        variation_map = {
            'natural': 'minor_natural',
            'harmonic': 'minor_harmonic',
            'melodic': 'minor_melodic'
        }

        scale_type = variation_map.get(variation.lower(), 'minor_natural')
        return Scale(root, scale_type)

    @staticmethod
    def minor_natural(root: Union[str, int, Note]) -> Scale:
        """Build a natural minor scale (Aeolian mode)."""
        return Scale(root, 'minor_natural')

    @staticmethod
    def minor_harmonic(root: Union[str, int, Note]) -> Scale:
        """Build a harmonic minor scale."""
        return Scale(root, 'minor_harmonic')

    @staticmethod
    def minor_melodic(root: Union[str, int, Note]) -> Scale:
        """Build a melodic minor scale (ascending)."""
        return Scale(root, 'minor_melodic')

    # Modal scales
    @staticmethod
    def dorian(root: Union[str, int, Note]) -> Scale:
        """Build a Dorian mode scale."""
        return Scale(root, 'dorian')

    @staticmethod
    def phrygian(root: Union[str, int, Note]) -> Scale:
        """Build a Phrygian mode scale."""
        return Scale(root, 'phrygian')

    @staticmethod
    def lydian(root: Union[str, int, Note]) -> Scale:
        """Build a Lydian mode scale."""
        return Scale(root, 'lydian')

    @staticmethod
    def mixolydian(root: Union[str, int, Note]) -> Scale:
        """Build a Mixolydian mode scale."""
        return Scale(root, 'mixolydian')

    @staticmethod
    def locrian(root: Union[str, int, Note]) -> Scale:
        """Build a Locrian mode scale."""
        return Scale(root, 'locrian')

    # Pentatonic scales
    @staticmethod
    def pentatonic_major(root: Union[str, int, Note]) -> Scale:
        """Build a major pentatonic scale."""
        return Scale(root, 'pentatonic_major')

    @staticmethod
    def pentatonic_minor(root: Union[str, int, Note]) -> Scale:
        """Build a minor pentatonic scale."""
        return Scale(root, 'pentatonic_minor')

    @staticmethod
    def pentatonic_blues(root: Union[str, int, Note]) -> Scale:
        """Build a blues pentatonic scale."""
        return Scale(root, 'pentatonic_blues')

    # Blues scales
    @staticmethod
    def blues_major(root: Union[str, int, Note]) -> Scale:
        """Build a major blues scale."""
        return Scale(root, 'blues_major')

    @staticmethod
    def blues_minor(root: Union[str, int, Note]) -> Scale:
        """Build a minor blues scale."""
        return Scale(root, 'blues_minor')

    # Other scales
    @staticmethod
    def whole_tone(root: Union[str, int, Note]) -> Scale:
        """Build a whole tone scale."""
        return Scale(root, 'whole_tone')

    @staticmethod
    def chromatic(root: Union[str, int, Note]) -> Scale:
        """Build a chromatic scale."""
        return Scale(root, 'chromatic')

    @staticmethod
    def diminished(root: Union[str, int, Note]) -> Scale:
        """Build a diminished scale (half-whole)."""
        return Scale(root, 'diminished')

    @staticmethod
    def augmented(root: Union[str, int, Note]) -> Scale:
        """Build an augmented scale."""
        return Scale(root, 'augmented')

    @staticmethod
    def ionian(root: Union[str, int, Note]) -> Scale:
        """Build an Ionian mode scale (same as major)."""
        return Scale(root, 'ionian')

    @staticmethod
    def aeolian(root: Union[str, int, Note]) -> Scale:
        """Build an Aeolian mode scale (same as natural minor)."""
        return Scale(root, 'aeolian')

    @staticmethod
    def from_intervals(root: Union[str, int, Note], intervals: List[int],
                      name: str = "Custom Scale") -> Scale:
        """
        Build a custom scale from a list of intervals.

        Args:
            root: Root note
            intervals: List of intervals in semitones (relative to root)
            name: Name for the custom scale (for display purposes)

        Returns:
            Custom Scale object

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
            logger.error(f"Invalid intervals for scale '{name}': {error_msg}")
            raise ValueError(f"Invalid intervals: {error_msg}")

        # Sanitize name
        try:
            from utils.validators import sanitize_input
            name = sanitize_input(name, 50)  # Max 50 chars for scale name
        except ImportError:
            name = str(name)[:50]  # Fallback sanitization

        # Thread-safe: pass intervals directly instead of modifying global dict
        custom_type = f"custom_{name.replace(' ', '_').lower()}"
        scale = Scale(root, custom_type, custom_intervals=intervals)

        logger.info(f"Created custom scale '{name}' with {len(intervals)} intervals")
        return scale

    @staticmethod
    def get_all_scale_types() -> List[str]:
        """
        Get a list of all available scale types.

        Returns:
            List of scale type strings
        """
        return list(SCALE_INTERVALS.keys())

    @staticmethod
    def get_scales_for_note(root: Union[str, int, Note]) -> List[Scale]:
        """
        Get all available scales starting from a given root note.

        Args:
            root: Root note

        Returns:
            List of all Scale objects for that root
        """
        scales = []
        for scale_type in SCALE_INTERVALS.keys():
            try:
                scales.append(Scale(root, scale_type))
            except (ValueError, TypeError, KeyError) as e:
                # Skip invalid scale constructions with specific error types
                logger = logging.getLogger(__name__)
                logger.warning(f"Failed to create scale {scale_type} for root {root}: {e}")
                continue
            except Exception as e:
                # Log unexpected errors but continue processing
                logger = logging.getLogger(__name__)
                logger.error(f"Unexpected error creating scale {scale_type}: {e}", exc_info=True)
                continue
        return scales

    @staticmethod
    def get_relative_scales(scale: Scale) -> List[Scale]:
        """
        Get scales that are relative to the given scale.

        Args:
            scale: Base scale

        Returns:
            List of relative scales (parallel and relative major/minor)
        """
        relatives = []

        # Parallel scales (same root, different type)
        for scale_type in ['major', 'minor_natural', 'dorian', 'phrygian', 'lydian', 'mixolydian', 'locrian']:
            if scale_type != scale.scale_type:
                try:
                    relatives.append(Scale(scale.root, scale_type))
                except:
                    continue

        # Relative major/minor
        if scale.scale_type in ['major', 'minor_natural']:
            relative = scale.get_relative_scale(
                'minor_natural' if scale.scale_type == 'major' else 'major'
            )
            relatives.append(relative)

        return relatives


# Convenience functions for quick scale creation
def major(root: Union[str, int, Note]) -> Scale:
    """Create a major scale."""
    return ScaleBuilder.major(root)

def minor(root: Union[str, int, Note], variation: str = 'natural') -> Scale:
    """Create a minor scale."""
    return ScaleBuilder.minor(root, variation)

def dorian(root: Union[str, int, Note]) -> Scale:
    """Create a Dorian scale."""
    return ScaleBuilder.dorian(root)

def mixolydian(root: Union[str, int, Note]) -> Scale:
    """Create a Mixolydian scale."""
    return ScaleBuilder.mixolydian(root)

def pentatonic_minor(root: Union[str, int, Note]) -> Scale:
    """Create a minor pentatonic scale."""
    return ScaleBuilder.pentatonic_minor(root)

def blues_minor(root: Union[str, int, Note]) -> Scale:
    """Create a minor blues scale."""
    return ScaleBuilder.blues_minor(root)
