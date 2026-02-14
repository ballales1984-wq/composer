"""
Integration module for external music theory libraries.

This module provides integration with:
- music21: For MIDI, notation, and harmonic analysis
- mingus: For roman numeral analysis and diatonic chord generation

Example usage:
    >>> from music_engine.integrations import IntegrationFactory
    >>> 
    >>> # Using music21
    >>> m21 = IntegrationFactory.get_music21_converter()
    >>> m21_note = m21.note_to_music21(my_note)
    >>> 
    >>> # Using mingus
    >>> mingus = IntegrationFactory.get_mingus_converter()
    >>> roman_numerals = mingus.chords_to_roman_numerals(my_chords, 'C')
"""

from .music21_adapter import (
    Music21Converter,
    note_to_music21,
    music21_to_note,
    chord_to_music21,
    music21_to_chord,
    scale_to_music21,
    progression_to_music21_stream,
    stream_to_progression,
)

from .mingus_adapter import (
    MingusConverter,
    note_to_mingus,
    mingus_to_note,
    chord_to_mingus,
    mingus_to_chord,
    progression_to_mingus,
    roman_numerals_to_chords,
    chords_to_roman_numerals,
    generate_diatonic_progressions,
    scale_to_mingus,
    mingus_to_scale,
)

from .factory import (
    IntegrationFactory,
    get_music21_converter,
    get_mingus_converter,
    convert,
    is_library_available,
    get_available_libraries,
)

__all__ = [
    # Music21 adapter
    'Music21Converter',
    'note_to_music21',
    'music21_to_note',
    'chord_to_music21',
    'music21_to_chord',
    'scale_to_music21',
    'progression_to_music21_stream',
    'stream_to_progression',
    
    # Mingus adapter
    'MingusConverter',
    'note_to_mingus',
    'mingus_to_note',
    'chord_to_mingus',
    'mingus_to_chord',
    'progression_to_mingus',
    'roman_numerals_to_chords',
    'chords_to_roman_numerals',
    'generate_diatonic_progressions',
    'scale_to_mingus',
    'mingus_to_scale',
    
    # Factory
    'IntegrationFactory',
    'get_music21_converter',
    'get_mingus_converter',
    'convert',
    'is_library_available',
    'get_available_libraries',
]

