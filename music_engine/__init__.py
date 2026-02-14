"""
Music Engine - A comprehensive music theory analysis engine for guitarists and musicians.

This package provides tools for:
- Note representation and chromatic scale
- Scale construction (major, minor, modal, pentatonic, blues)
- Chord construction (triads, seventh chords, extended chords)
- Arpeggio generation from chords and scales
- Harmonic progression analysis and scale suggestions

Author: AI Music Engineer
Version: 0.1.0
"""

__version__ = "0.1.0"
__author__ = "AI Music Engineer"

# Lazy imports commented to avoid import issues when running as script
# from .core import notes, scales, chords, arpeggios, progressions
# from .models import note, chord, scale, arpeggio, progression

__all__ = [
    'notes', 'scales', 'chords', 'arpeggios', 'progressions',
    'note', 'chord', 'scale', 'arpeggio', 'progression',
    'integrations'
]
