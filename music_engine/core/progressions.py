"""
Progression analysis module for the music theory engine.

This module provides functions and classes for analyzing musical chord
progressions, finding compatible scales, and suggesting musical ideas.
"""

from typing import List, Union, Dict, Optional

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
from models.progression import Progression


class ProgressionAnalyzer:
    """
    Analyzer class for musical chord progressions.

    This class provides methods for analyzing progressions,
    finding compatible scales, and generating musical suggestions.
    """

    @staticmethod
    def analyze_progression(chords: List[Union[Chord, str]]) -> Progression:
        """
        Analyze a chord progression.

        Args:
            chords: List of chords

        Returns:
            Analyzed Progression object
        """
        return Progression(chords)

    @staticmethod
    def find_compatible_scales(progression: Union[Progression, List[Union[Chord, str]]]) -> List[Scale]:
        """
        Find scales compatible with a progression.

        Args:
            progression: Progression object or list of chords

        Returns:
            List of compatible Scale objects
        """
        if isinstance(progression, list):
            progression = Progression(progression)

        return progression.get_compatible_scales()

    @staticmethod
    def suggest_scales_for_improvisation(progression: Union[Progression, List[Union[Chord, str]]],
                                        max_suggestions: int = 5) -> List[Scale]:
        """
        Suggest scales for improvising over a progression.

        Args:
            progression: Progression or list of chords
            max_suggestions: Maximum number of suggestions

        Returns:
            List of recommended Scale objects
        """
        if isinstance(progression, list):
            progression = Progression(progression)

        return progression.get_scale_suggestions(max_suggestions)

    @staticmethod
    def detect_key(chords: List[Union[Chord, str]]) -> Optional[Note]:
        """
        Detect the key of a chord progression.

        Args:
            chords: List of chords

        Returns:
            Detected key Note, or None if unclear
        """
        progression = Progression(chords)
        return progression.key

    @staticmethod
    def get_progression_complexity(chords: List[Union[Chord, str]]) -> str:
        """
        Analyze the complexity of a chord progression.

        Args:
            chords: List of chords

        Returns:
            Complexity level ('simple', 'intermediate', 'complex')
        """
        progression = Progression(chords)
        return progression.analysis['complexity']

    @staticmethod
    def generate_similar_progression(chords: List[Union[Chord, str]],
                                   variation_type: str = 'similar') -> List[str]:
        """
        Generate a similar progression based on the input.

        Args:
            chords: Base progression chords
            variation_type: Type of variation ('similar', 'contrasting', 'extended')

        Returns:
            List of chord names for the new progression
        """
        progression = Progression(chords)

        if variation_type == 'similar':
            similar = progression.get_similar_progressions()
            return similar[0] if similar else []

        # For other types, return the original as fallback
        return [chord.name for chord in progression.chords]

    @staticmethod
    def transpose_progression(chords: List[Union[Chord, str]],
                            semitones: int) -> List[Chord]:
        """
        Transpose an entire chord progression.

        Args:
            chords: Original chords
            semitones: Semitones to transpose

        Returns:
            List of transposed Chord objects
        """
        progression = Progression(chords)
        transposed = progression.transpose(semitones)
        return transposed.chords

    @staticmethod
    def extract_melody_notes(progression: Union[Progression, List[Union[Chord, str]]]) -> List[Note]:
        """
        Extract all unique notes from a progression for melody creation.

        Args:
            progression: Progression or list of chords

        Returns:
            List of unique Note objects available for melody
        """
        if isinstance(progression, list):
            progression = Progression(progression)

        return list(progression.all_notes)

    @staticmethod
    def get_progression_cadences(progression: Union[Progression, List[Union[Chord, str]]]) -> List[str]:
        """
        Identify cadences in a progression.

        Args:
            progression: Progression or list of chords

        Returns:
            List of cadence types found
        """
        if isinstance(progression, list):
            progression = Progression(progression)

        cadences = []

        # Simple cadence detection
        chords = progression.chords
        if len(chords) >= 2:
            last_two = chords[-2:]

            # Perfect authentic cadence (V -> I)
            if (len(last_two[0]) >= 4 and 'dom7' in last_two[0].quality and
                last_two[1].quality == 'maj'):
                cadences.append('perfect_authentic')

            # Imperfect authentic cadence (I, II, IV, VI -> V)
            elif (last_two[1].quality in ['maj', 'dom7'] and
                  any(c.quality in ['maj', 'min'] for c in last_two[:-1])):
                cadences.append('imperfect_authentic')

            # Plagal cadence (IV -> I)
            elif (last_two[0].quality == 'maj' and last_two[1].quality == 'maj'):
                cadences.append('plagal')

            # Deceptive cadence (V -> vi)
            elif (last_two[0].quality in ['maj', 'dom7'] and
                  last_two[1].quality == 'min'):
                cadences.append('deceptive')

        return cadences

    @staticmethod
    def create_progression_from_roman_numerals(roman_numerals: List[str],
                                             key: Union[str, Note]) -> Progression:
        """
        Create a chord progression from Roman numeral notation.

        Args:
            roman_numerals: List of Roman numerals (e.g., ['I', 'IV', 'V', 'I'])
            key: Key of the progression

        Returns:
            Progression object
        """
        key_note = Note(key) if not isinstance(key, Note) else key

        chords = []
        major_intervals = [0, 2, 4, 5, 7, 9, 11]  # Major scale intervals
        minor_intervals = [0, 2, 3, 5, 7, 8, 10]  # Natural minor intervals

        roman_to_degree = {
            'I': 0, 'II': 1, 'III': 2, 'IV': 3, 'V': 4, 'VI': 5, 'VII': 6,
            'i': 0, 'ii': 1, 'iii': 2, 'iv': 3, 'v': 4, 'vi': 5, 'vii': 6
        }

        for numeral in roman_numerals:
            # Remove any quality symbols for now
            clean_numeral = ''.join(c for c in numeral if c.isalnum())

            if clean_numeral in roman_to_degree:
                degree = roman_to_degree[clean_numeral]
                root_semitone = key_note.semitone + major_intervals[degree]
                root = Note.from_semitone(root_semitone % 12)

                # Determine chord quality based on numeral case
                if clean_numeral.isupper():
                    quality = 'maj'
                else:
                    quality = 'min'

                # Add seventh for dominant function chords
                if clean_numeral in ['V', 'v', 'VII', 'vii']:
                    quality = 'dom7'

                chords.append(Chord(root, quality))

        return Progression(chords, key_note)

    @staticmethod
    def get_progression_length(progression: Union[Progression, List[Union[Chord, str]]]) -> int:
        """
        Get the length of a progression.

        Args:
            progression: Progression or list of chords

        Returns:
            Number of chords
        """
        if isinstance(progression, Progression):
            return len(progression)
        return len(progression)

    @staticmethod
    def split_progression(progression: Union[Progression, List[Union[Chord, str]]],
                         sections: int) -> List[List[Chord]]:
        """
        Split a progression into sections.

        Args:
            progression: Progression or list of chords
            sections: Number of sections to split into

        Returns:
            List of chord lists, one per section
        """
        if isinstance(progression, list):
            chords = progression
        else:
            chords = progression.chords

        section_size = len(chords) // sections
        split_progressions = []

        for i in range(sections):
            start = i * section_size
            end = start + section_size if i < sections - 1 else len(chords)
            split_progressions.append(chords[start:end])

        return split_progressions


# Convenience functions
def analyze(chords: List[Union[Chord, str]]) -> Progression:
    """Analyze a chord progression."""
    return ProgressionAnalyzer.analyze_progression(chords)

def find_scales(chords: List[Union[Chord, str]]) -> List[Scale]:
    """Find compatible scales for a progression."""
    return ProgressionAnalyzer.find_compatible_scales(chords)

def suggest_scales(chords: List[Union[Chord, str]], max_suggestions: int = 5) -> List[Scale]:
    """Suggest scales for improvising over a progression."""
    return ProgressionAnalyzer.suggest_scales_for_improvisation(chords, max_suggestions)
