"""
Interval module for the music theory engine.

This module provides the Interval class for representing and calculating
musical intervals between notes.
"""

from typing import Optional, Union, Tuple
from enum import Enum


class IntervalQuality(Enum):
    """Enumeration of interval qualities."""
    PERFECT = "P"
    MAJOR = "M"
    MINOR = "m"
    DIMINISHED = "d"
    AUGMENTED = "A"
    DOUBLY_DIMINISHED = "dd"
    DOUBLY_AUGMENTED = "AA"


class Interval:
    """
    Represents a musical interval between two notes.
    
    An interval is defined by:
    - Semitone distance (0-12 for simple intervals)
    - Quality (perfect, major, minor, diminished, augmented)
    - Compound intervals (greater than an octave)
    
    Examples:
        >>> i = Interval(4)  # Major third
        >>> i.name  # 'major 3rd'
        >>> i.semitones  # 4
        >>> i.short_name  # 'M3'
    """
    
    # Standard interval names indexed by semitones
    INTERVAL_NAMES = {
        0: ('unison', 'P1'),
        1: ('minor 2nd', 'm2'),
        2: ('major 2nd', 'M2'),
        3: ('minor 3rd', 'm3'),
        4: ('major 3rd', 'M3'),
        5: ('perfect 4th', 'P4'),
        6: ('tritone', 'TT'),
        7: ('perfect 5th', 'P5'),
        8: ('minor 6th', 'm6'),
        9: ('major 6th', 'M6'),
        10: ('minor 7th', 'm7'),
        11: ('major 7th', 'M7'),
        12: ('octave', 'P8'),
    }
    
    # Extended intervals (compound)
    EXTENDED_INTERVALS = {
        13: ('minor 9th', 'm9'),
        14: ('major 9th', 'M9'),
        15: ('minor 10th', 'm10'),
        16: ('major 10th', 'M10'),
        17: ('perfect 11th', 'P11'),
        18: ('augmented 11th', 'A11'),
        19: ('perfect 12th', 'P12'),
        20: ('minor 13th', 'm13'),
        21: ('major 13th', 'M13'),
        22: ('minor 14th', 'm14'),
        23: ('major 14th', 'M14'),
        24: ('double octave', 'P15'),
    }
    
    # All intervals combined
    ALL_INTERVALS = {**INTERVAL_NAMES, **EXTENDED_INTERVALS}
    
    def __init__(self, semitones: int, quality: Optional[IntervalQuality] = None):
        """
        Initialize an Interval.
        
        Args:
            semitones: Number of semitones in the interval (0-24)
            quality: Optional interval quality (auto-calculated if not provided)
            
        Raises:
            ValueError: If semitones is out of valid range
        """
        if semitones < 0 or semitones > 24:
            raise ValueError(f"Semitones must be between 0 and 24, got {semitones}")
        
        self._semitones = semitones
        self._quality = quality or self._infer_quality(semitones)
    
    @staticmethod
    def _infer_quality(semitones: int) -> IntervalQuality:
        """Infer the quality of an interval from its semitones."""
        # Perfect intervals
        if semitones in [0, 5, 7, 12]:
            return IntervalQuality.PERFECT
        # Major intervals
        elif semitones in [2, 4, 9, 11, 14, 16, 21, 23]:
            return IntervalQuality.MAJOR
        # Minor intervals
        elif semitones in [1, 3, 8, 10, 15, 20, 22]:
            return IntervalQuality.MINOR
        # Diminished (one semitone less than perfect/major)
        elif semitones in [4, 6, 11]:  # d4, d5, d8
            return IntervalQuality.DIMINISHED
        # Augmented (one semitone more than perfect/minor)
        elif semitones in [6, 8, 13]:  # A4, A5, A12
            return IntervalQuality.AUGMENTED
        else:
            return IntervalQuality.MAJOR
    
    @property
    def semitones(self) -> int:
        """Get the number of semitones in the interval."""
        return self._semitones
    
    @property
    def name(self) -> str:
        """Get the full name of the interval."""
        if self._semitones in self.INTERVAL_NAMES:
            return self.INTERVAL_NAMES[self._semitones][0]
        elif self._semitones in self.EXTENDED_INTERVALS:
            return self.EXTENDED_INTERVALS[self._semitones][0]
        return f"unknown interval ({self._semitones} semitones)"
    
    @property
    def short_name(self) -> str:
        """Get the short name of the interval."""
        if self._semitones in self.INTERVAL_NAMES:
            return self.INTERVAL_NAMES[self._semitones][1]
        elif self._semitones in self.EXTENDED_INTERVALS:
            return self.EXTENDED_INTERVALS[self._semitones][1]
        return str(self._semitones)
    
    @property
    def quality(self) -> IntervalQuality:
        """Get the quality of the interval."""
        return self._quality
    
    @property
    def is_perfect(self) -> bool:
        """Check if this is a perfect interval (unison, 4th, 5th, octave)."""
        return self._quality == IntervalQuality.PERFECT
    
    @property
    def is_major_minor(self) -> bool:
        """Check if this is a major/minor interval (2nd, 3rd, 6th, 7th)."""
        return self._quality in [IntervalQuality.MAJOR, IntervalQuality.MINOR]
    
    @property
    def is_consonance(self) -> bool:
        """Check if this is a consonance (perfect consonances)."""
        return self._semitones in [0, 3, 4, 5, 7, 8, 9, 12]
    
    @property
    def is_dissonance(self) -> bool:
        """Check if this is a dissonance."""
        return self._semitones in [1, 2, 6, 10, 11]
    
    @property
    def simple_semitones(self) -> int:
        """Get the simple interval (octave reduced)."""
        return self._semitones % 12
    
    @property
    def octaves(self) -> int:
        """Get the number of octaves in the interval."""
        return self._semitones // 12
    
    @property
    def interval_number(self) -> int:
        """Get the interval number (1=unison, 2=2nd, etc.)."""
        simple = self.simple_semitones
        # Map semitones to interval number
        number_map = {
            0: 1, 1: 2, 2: 2, 3: 3, 4: 3,
            5: 4, 6: 4, 7: 5, 8: 6, 9: 6,
            10: 7, 11: 7, 12: 8
        }
        return number_map.get(simple, 1) + (self.octaves * 7)
    
    @staticmethod
    def between(semitone1: int, semitone2: int) -> 'Interval':
        """
        Create an Interval between two semitone values.
        
        Args:
            semitone1: First semitone value (0-11)
            semitone2: Second semitone value (0-11)
            
        Returns:
            Interval object representing the distance
        """
        # Calculate the smallest distance (handling wrap-around)
        diff = (semitone2 - semitone1) % 12
        reverse_diff = (semitone1 - semitone2) % 12
        
        # Use the smaller distance for simple intervals
        if diff <= reverse_diff:
            return Interval(diff)
        else:
            return Interval(reverse_diff)
    
    @staticmethod
    def from_quality_and_number(quality: str, number: int) -> 'Interval':
        """
        Create an Interval from quality and number.
        
        Args:
            quality: Quality string ('P', 'M', 'm', 'd', 'A')
            number: Interval number (1-15)
            
        Returns:
            Interval object
            
        Examples:
            >>> Interval.from_quality_and_number('M', 3)  # Major 3rd
            >>> Interval.from_quality_and_number('P', 5)  # Perfect 5th
        """
        # Base semitones for each interval number (without quality)
        base_semitones = {
            1: 0, 2: 2, 3: 4, 4: 5, 5: 7, 6: 9, 7: 11,
            8: 12, 9: 14, 10: 16, 11: 17, 12: 19, 13: 21, 14: 23, 15: 24
        }
        
        quality = quality.upper()
        base = base_semitones.get(number, 0)
        
        # Adjust for quality
        if quality == 'P':
            return Interval(base)
        elif quality == 'M':
            return Interval(base)
        elif quality == 'M' and number in [2, 3, 6, 7]:
            return Interval(base)
        elif quality == 'm':
            return Interval(base - 1)
        elif quality == 'd':
            return Interval(base - 1 if number in [1, 4, 5, 8] else base - 2)
        elif quality == 'A':
            return Interval(base + 1 if number in [1, 4, 5, 8] else base + 2)
        else:
            return Interval(base)
    
    def invert(self) -> 'Interval':
        """
        Get the inverted interval.
        
        Returns:
            Inverted Interval
            
        Examples:
            >>> Interval(4).invert()  # Major 3rd -> Minor 6th
        """
        # Inversion formula: 12 - semitones
        inverted_semitones = 12 - self.simple_semitones
        return Interval(inverted_semitones + (self.octaves * 12))
    
    def transpose(self, semitones: int) -> 'Interval':
        """
        Transpose the interval by a given number of semitones.
        
        Args:
            semitones: Number of semitones to transpose
            
        Returns:
            New transposed Interval
        """
        new_semitones = (self._semitones + semitones) % 25
        if new_semitones < 0:
            new_semitones = 0
        return Interval(new_semitones)
    
    def __str__(self) -> str:
        """String representation of the interval."""
        return self.name
    
    def __repr__(self) -> str:
        """Detailed string representation."""
        return f"Interval(semitones={self._semitones}, quality={self._quality.value})"
    
    def __eq__(self, other) -> bool:
        """Check equality based on semitones."""
        if isinstance(other, Interval):
            return self._semitones == other._semitones
        return False
    
    def __hash__(self) -> int:
        """Hash based on semitones."""
        return hash(self._semitones)
    
    def __lt__(self, other) -> bool:
        """Compare intervals by semitones."""
        if isinstance(other, Interval):
            return self._semitones < other._semitones
        return NotImplemented
    
    def __add__(self, other: int) -> 'Interval':
        """Add semitones to interval."""
        if isinstance(other, int):
            return Interval(self._semitones + other)
        return NotImplemented
    
    def __sub__(self, other: int) -> 'Interval':
        """Subtract semitones from interval."""
        if isinstance(other, int):
            return Interval(max(0, self._semitones - other))
        return NotImplemented
    
    def __mul__(self, other: int) -> 'Interval':
        """Multiply interval (for compound intervals)."""
        if isinstance(other, int):
            return Interval(self._semitones * other)
        return NotImplemented


# Utility functions

def get_interval(semitones: int) -> Interval:
    """Create an Interval from semitones."""
    return Interval(semitones)


def interval_to_semitones(interval_name: str) -> int:
    """
    Convert an interval name to semitones.
    
    Args:
        interval_name: Name like 'major 3rd', 'P5', 'm7', etc.
        
    Returns:
        Number of semitones
    """
    interval_name = interval_name.lower().strip()
    
    # Try direct lookup
    for semitones, (name, short) in Interval.INTERVAL_NAMES.items():
        if interval_name == name or interval_name == short:
            return semitones
    
    for semitones, (name, short) in Interval.EXTENDED_INTERVALS.items():
        if interval_name == name or interval_name == short:
            return semitones
    
    # Try parsing quality + number
    parts = interval_name.split()
    if len(parts) >= 2:
        quality = parts[0]
        number = parts[-1]
        
        # Extract number
        try:
            num = int(''.join(c for c in number if c.isdigit()))
            return Interval.from_quality_and_number(quality, num).semitones
        except:
            pass
    
    raise ValueError(f"Unknown interval name: {interval_name}")

