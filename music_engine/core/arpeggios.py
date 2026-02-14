"""
Arpeggio construction module for the music theory engine.

This module provides functions and classes for building musical arpeggios
from chords and scales with different directions and patterns.
"""

from typing import Union, List

# Import with proper path handling
import sys
import os

# Ensure parent directory is in path
parent_dir = os.path.dirname(os.path.dirname(__file__))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from models.note import Note
from models.chord import Chord
from models.scale import Scale
from models.arpeggio import Arpeggio

# Add CHORD_INTERVALS constant for arpeggio parsing
CHORD_INTERVALS = {
    'maj': [0, 4, 7], 'min': [0, 3, 7], 'dom7': [0, 4, 7, 10],
}


class ArpeggioBuilder:
    """
    Builder class for creating musical arpeggios.

    This class provides static methods for constructing arpeggios
    from chords and scales with various patterns and directions.
    """

    @staticmethod
    def from_chord(chord: Union[Chord, str],
                  direction: str = 'up',
                  octaves: int = 1) -> Arpeggio:
        """
        Build an arpeggio from a chord.

        Args:
            chord: Chord object or chord specification string
            direction: Direction ('up', 'down', 'up_down', 'down_up')
            octaves: Number of octaves to span

        Returns:
            Arpeggio object
        """
        if isinstance(chord, str):
            from .chords import ChordBuilder
            chord = ChordBuilder.parse_chord_string(chord)

        return Arpeggio(chord, direction, octaves)

    @staticmethod
    def from_scale(scale: Union[Scale, str],
                  direction: str = 'up',
                  octaves: int = 1) -> Arpeggio:
        """
        Build an arpeggio from a scale.

        Args:
            scale: Scale object or scale specification string
            direction: Direction ('up', 'down', 'up_down', 'down_up')
            octaves: Number of octaves to span

        Returns:
            Arpeggio object
        """
        if isinstance(scale, str):
            # Simple scale parsing - could be enhanced
            from .scales import ScaleBuilder
            # Assume format like "C major" or "A minor"
            parts = scale.split()
            if len(parts) == 2:
                root, scale_type = parts
                # Map common type names to internal format
                type_map = {
                    'major': 'major',
                    'minor': 'minor_natural',
                    'dorian': 'dorian',
                    'mixolydian': 'mixolydian',
                    'blues': 'blues_minor'
                }
                internal_type = type_map.get(scale_type.lower(), scale_type.lower())
                scale = Scale(root, internal_type)
            else:
                raise ValueError(f"Invalid scale specification: {scale}")

        return Arpeggio(scale, direction, octaves)

    # Triad arpeggios
    @staticmethod
    def major_triad(root: Union[str, int, Note],
                   direction: str = 'up') -> Arpeggio:
        """Build a major triad arpeggio."""
        from .chords import ChordBuilder
        chord = ChordBuilder.major(root)
        return Arpeggio(chord, direction)

    @staticmethod
    def minor_triad(root: Union[str, int, Note],
                   direction: str = 'up') -> Arpeggio:
        """Build a minor triad arpeggio."""
        from .chords import ChordBuilder
        chord = ChordBuilder.minor(root)
        return Arpeggio(chord, direction)

    @staticmethod
    def diminished_triad(root: Union[str, int, Note],
                        direction: str = 'up') -> Arpeggio:
        """Build a diminished triad arpeggio."""
        from .chords import ChordBuilder
        chord = ChordBuilder.diminished(root)
        return Arpeggio(chord, direction)

    @staticmethod
    def augmented_triad(root: Union[str, int, Note],
                       direction: str = 'up') -> Arpeggio:
        """Build an augmented triad arpeggio."""
        from .chords import ChordBuilder
        chord = ChordBuilder.augmented(root)
        return Arpeggio(chord, direction)

    # Seventh chord arpeggios
    @staticmethod
    def dominant7(root: Union[str, int, Note],
                 direction: str = 'up') -> Arpeggio:
        """Build a dominant 7th arpeggio."""
        from .chords import ChordBuilder
        chord = ChordBuilder.dominant7(root)
        return Arpeggio(chord, direction)

    @staticmethod
    def major7(root: Union[str, int, Note],
              direction: str = 'up') -> Arpeggio:
        """Build a major 7th arpeggio."""
        from .chords import ChordBuilder
        chord = ChordBuilder.major7(root)
        return Arpeggio(chord, direction)

    @staticmethod
    def minor7(root: Union[str, int, Note],
              direction: str = 'up') -> Arpeggio:
        """Build a minor 7th arpeggio."""
        from .chords import ChordBuilder
        chord = ChordBuilder.minor7(root)
        return Arpeggio(chord, direction)

    @staticmethod
    def diminished7(root: Union[str, int, Note],
                   direction: str = 'up') -> Arpeggio:
        """Build a diminished 7th arpeggio."""
        from .chords import ChordBuilder
        chord = ChordBuilder.diminished7(root)
        return Arpeggio(chord, direction)

    @staticmethod
    def minor7b5(root: Union[str, int, Note],
                direction: str = 'up') -> Arpeggio:
        """Build a minor 7th flat 5 arpeggio."""
        from .chords import ChordBuilder
        chord = ChordBuilder.minor7b5(root)
        return Arpeggio(chord, direction)

    # Extended arpeggios
    @staticmethod
    def dominant9(root: Union[str, int, Note],
                 direction: str = 'up') -> Arpeggio:
        """Build a dominant 9th arpeggio."""
        from .chords import ChordBuilder
        chord = ChordBuilder.dom9(root)
        return Arpeggio(chord, direction)

    @staticmethod
    def dominant11(root: Union[str, int, Note],
                  direction: str = 'up') -> Arpeggio:
        """Build a dominant 11th arpeggio."""
        from .chords import ChordBuilder
        chord = ChordBuilder.dom11(root)
        return Arpeggio(chord, direction)

    @staticmethod
    def dominant13(root: Union[str, int, Note],
                  direction: str = 'up') -> Arpeggio:
        """Build a dominant 13th arpeggio."""
        from .chords import ChordBuilder
        chord = ChordBuilder.dom13(root)
        return Arpeggio(chord, direction)

    # Scale arpeggios
    @staticmethod
    def major_scale(root: Union[str, int, Note],
                   direction: str = 'up') -> Arpeggio:
        """Build a major scale arpeggio."""
        from .scales import ScaleBuilder
        scale = ScaleBuilder.major(root)
        return Arpeggio(scale, direction)

    @staticmethod
    def minor_scale(root: Union[str, int, Note],
                   direction: str = 'up') -> Arpeggio:
        """Build a natural minor scale arpeggio."""
        from .scales import ScaleBuilder
        scale = ScaleBuilder.minor_natural(root)
        return Arpeggio(scale, direction)

    @staticmethod
    def dorian_scale(root: Union[str, int, Note],
                    direction: str = 'up') -> Arpeggio:
        """Build a Dorian scale arpeggio."""
        from .scales import ScaleBuilder
        scale = ScaleBuilder.dorian(root)
        return Arpeggio(scale, direction)

    @staticmethod
    def mixolydian_scale(root: Union[str, int, Note],
                        direction: str = 'up') -> Arpeggio:
        """Build a Mixolydian scale arpeggio."""
        from .scales import ScaleBuilder
        scale = ScaleBuilder.mixolydian(root)
        return Arpeggio(scale, direction)

    @staticmethod
    def pentatonic_minor(root: Union[str, int, Note],
                        direction: str = 'up') -> Arpeggio:
        """Build a minor pentatonic scale arpeggio."""
        from .scales import ScaleBuilder
        scale = ScaleBuilder.pentatonic_minor(root)
        return Arpeggio(scale, direction)

    @staticmethod
    def blues_scale(root: Union[str, int, Note],
                   direction: str = 'up') -> Arpeggio:
        """Build a blues scale arpeggio."""
        from .scales import ScaleBuilder
        scale = ScaleBuilder.blues_minor(root)
        return Arpeggio(scale, direction)

    @staticmethod
    def create_pattern(notes: List[Union[str, int, Note]],
                      direction: str = 'up') -> Arpeggio:
        """
        Create a custom arpeggio pattern from a list of notes.

        Args:
            notes: List of notes for the pattern
            direction: Direction for the pattern

        Returns:
            Custom Arpeggio object
        """
        # Convert notes to Note objects
        note_objects = [Note(note) for note in notes]

        # Create a minimal chord from the notes to use as source

        # Calculate intervals from first note
        root = note_objects[0]
        intervals = [0]  # Root
        for note in note_objects[1:]:
            interval = root.interval_to(note)
            intervals.append(interval)

        # Create custom chord
        custom_type = f"custom_arpeggio_{hash(tuple(intervals))}"
        CHORD_INTERVALS[custom_type] = intervals
        chord = Chord(root, custom_type)

        return Arpeggio(chord, direction)

    @staticmethod
    def get_arpeggio_techniques() -> List[str]:
        """
        Get available arpeggio techniques/patterns.

        Returns:
            List of technique names
        """
        return [
            'basic_triad', 'seventh_chord', 'extended_chord',
            'scale_run', 'broken_chord', 'sweep_picking',
            'fingerstyle', 'tapping', 'hybrid_picking'
        ]

    @staticmethod
    def suggest_arpeggios_for_chord(chord: Union[Chord, str]) -> List[Arpeggio]:
        """
        Suggest appropriate arpeggios for a given chord.

        Args:
            chord: Chord to find arpeggios for

        Returns:
            List of suggested Arpeggio objects
        """
        if isinstance(chord, str):
            from .chords import ChordBuilder
            chord = ChordBuilder.parse_chord_string(chord)

        suggestions = []

        # Basic triad arpeggio
        suggestions.append(Arpeggio(chord, 'up'))

        # Seventh chord arpeggios for 7th chords
        if len(chord) >= 4 and '7' in chord.quality:
            suggestions.append(Arpeggio(chord, 'up_down'))

        # Extended arpeggios for complex chords
        if len(chord) > 4:
            suggestions.append(Arpeggio(chord, 'down'))

        return suggestions


# Convenience functions for quick arpeggio creation
def triad(root: Union[str, int, Note], quality: str = 'maj',
         direction: str = 'up') -> Arpeggio:
    """Create a triad arpeggio."""
    from .chords import ChordBuilder
    chord = ChordBuilder.from_quality(root, quality)
    return Arpeggio(chord, direction)

def seventh(root: Union[str, int, Note], quality: str = 'dom7',
           direction: str = 'up') -> Arpeggio:
    """Create a seventh chord arpeggio."""
    from .chords import ChordBuilder
    chord = ChordBuilder.from_quality(root, quality)
    return Arpeggio(chord, direction)

def scale_arpeggio(root: Union[str, int, Note], scale_type: str = 'major',
                  direction: str = 'up') -> Arpeggio:
    """Create a scale arpeggio."""
    from .scales import ScaleBuilder

    # Map scale type strings to ScaleBuilder methods
    scale_type_map = {
        'major': lambda r: ScaleBuilder.major(r),
        'minor': lambda r: ScaleBuilder.minor(r),
        'minor_natural': lambda r: ScaleBuilder.minor_natural(r),
        'minor_harmonic': lambda r: ScaleBuilder.minor_harmonic(r),
        'minor_melodic': lambda r: ScaleBuilder.minor_melodic(r),
        'dorian': lambda r: ScaleBuilder.dorian(r),
        'phrygian': lambda r: ScaleBuilder.phrygian(r),
        'lydian': lambda r: ScaleBuilder.lydian(r),
        'mixolydian': lambda r: ScaleBuilder.mixolydian(r),
        'aeolian': lambda r: ScaleBuilder.aeolian(r),
        'locrian': lambda r: ScaleBuilder.locrian(r),
        'pentatonic_major': lambda r: ScaleBuilder.pentatonic_major(r),
        'pentatonic_minor': lambda r: ScaleBuilder.pentatonic_minor(r),
        'blues': lambda r: ScaleBuilder.blues(r),
        'chromatic': lambda r: ScaleBuilder.chromatic(r),
    }

    # Get the scale builder function, default to major if not found
    scale_builder = scale_type_map.get(scale_type.lower(), lambda r: ScaleBuilder.major(r))
    scale = scale_builder(root)
    return Arpeggio(scale, direction)
