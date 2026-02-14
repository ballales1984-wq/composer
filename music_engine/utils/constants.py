"""
Musical constants and definitions for the music theory engine.

This module contains all the fundamental musical constants used throughout
the music engine, including note names, intervals, scales, and chords.
"""

from typing import Dict, List, Tuple

# ============================================================================
# NOTE SYSTEM CONSTANTS
# ============================================================================

# Natural note names (without accidentals)
NATURAL_NOTES = ['C', 'D', 'E', 'F', 'G', 'A', 'B']

# All note names including sharps and flats
ALL_NOTES = [
    'C', 'C#', 'Db', 'D', 'D#', 'Eb', 'E', 'F',
    'F#', 'Gb', 'G', 'G#', 'Ab', 'A', 'A#', 'Bb', 'B'
]

# Note names with their semitone values (C = 0)
NOTE_TO_SEMITONE = {
    'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3,
    'E': 4, 'F': 5, 'F#': 6, 'Gb': 6, 'G': 7, 'G#': 8,
    'Ab': 8, 'A': 9, 'A#': 10, 'Bb': 10, 'B': 11
}

# Reverse mapping: semitone to note names
SEMITONE_TO_NOTES = {
    0: ['C'], 1: ['C#', 'Db'], 2: ['D'], 3: ['D#', 'Eb'],
    4: ['E'], 5: ['F'], 6: ['F#', 'Gb'], 7: ['G'], 8: ['G#', 'Ab'],
    9: ['A'], 10: ['A#', 'Bb'], 11: ['B']
}

# Enharmonic equivalents
ENHARMONIC_EQUIVALENTS = {
    'C#': 'Db', 'Db': 'C#', 'D#': 'Eb', 'Eb': 'D#',
    'F#': 'Gb', 'Gb': 'F#', 'G#': 'Ab', 'Ab': 'G#',
    'A#': 'Bb', 'Bb': 'A#'
}

# ============================================================================
# INTERVAL CONSTANTS
# ============================================================================

# Basic intervals in semitones
INTERVALS_SEMITONES = {
    'unison': 0,
    'minor_second': 1, 'major_second': 2,
    'minor_third': 3, 'major_third': 4,
    'perfect_fourth': 5,
    'tritone': 6,
    'perfect_fifth': 7,
    'minor_sixth': 8, 'major_sixth': 9,
    'minor_seventh': 10, 'major_seventh': 11,
    'octave': 12,
    'minor_ninth': 13, 'major_ninth': 14,
    'minor_tenth': 15, 'major_tenth': 16,
    'perfect_eleventh': 17,
    'minor_thirteenth': 20, 'major_thirteenth': 21
}

# Interval names by semitone value
SEMITONE_TO_INTERVAL = {
    0: 'unison', 1: 'minor_second', 2: 'major_second',
    3: 'minor_third', 4: 'major_third', 5: 'perfect_fourth',
    6: 'tritone', 7: 'perfect_fifth', 8: 'minor_sixth',
    9: 'major_sixth', 10: 'minor_seventh', 11: 'major_seventh',
    12: 'octave', 13: 'minor_ninth', 14: 'major_ninth',
    15: 'minor_tenth', 16: 'major_tenth', 17: 'perfect_eleventh',
    20: 'minor_thirteenth', 21: 'major_thirteenth'
}

# ============================================================================
# SCALE CONSTANTS
# ============================================================================

# Scale intervals in semitones (relative to root)
SCALE_INTERVALS = {
    # Major scales
    'major': [0, 2, 4, 5, 7, 9, 11],
    'ionian': [0, 2, 4, 5, 7, 9, 11],  # Same as major

    # Minor scales
    'minor_natural': [0, 2, 3, 5, 7, 8, 10],
    'aeolian': [0, 2, 3, 5, 7, 8, 10],  # Same as natural minor
    'minor_harmonic': [0, 2, 3, 5, 7, 8, 11],
    'minor_melodic': [0, 2, 3, 5, 7, 9, 11],  # Ascending

    # Modal scales (church modes)
    'dorian': [0, 2, 3, 5, 7, 9, 10],
    'phrygian': [0, 1, 3, 5, 7, 8, 10],
    'lydian': [0, 2, 4, 6, 7, 9, 11],
    'mixolydian': [0, 2, 4, 5, 7, 9, 10],
    'locrian': [0, 1, 3, 5, 6, 8, 10],

    # Pentatonic scales
    'pentatonic_major': [0, 2, 4, 7, 9],
    'pentatonic_minor': [0, 3, 5, 7, 10],
    'pentatonic_blues': [0, 3, 5, 6, 7, 10],

    # Blues scales
    'blues_major': [0, 2, 3, 4, 7, 9],
    'blues_minor': [0, 3, 5, 6, 7, 10],

    # Other common scales
    'whole_tone': [0, 2, 4, 6, 8, 10],
    'chromatic': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
    'diminished': [0, 2, 3, 5, 6, 8, 9, 11],
    'augmented': [0, 3, 4, 7, 8, 11],
}

# Scale names for display
SCALE_NAMES = {
    'major': 'Major (Ionian)',
    'minor_natural': 'Natural Minor (Aeolian)',
    'minor_harmonic': 'Harmonic Minor',
    'minor_melodic': 'Melodic Minor',
    'dorian': 'Dorian',
    'phrygian': 'Phrygian',
    'lydian': 'Lydian',
    'mixolydian': 'Mixolydian',
    'locrian': 'Locrian',
    'pentatonic_major': 'Major Pentatonic',
    'pentatonic_minor': 'Minor Pentatonic',
    'pentatonic_blues': 'Blues Pentatonic',
    'blues_major': 'Major Blues',
    'blues_minor': 'Minor Blues',
    'whole_tone': 'Whole Tone',
    'chromatic': 'Chromatic',
    'diminished': 'Diminished',
    'augmented': 'Augmented'
}

# ============================================================================
# CHORD CONSTANTS
# ============================================================================

# Chord intervals in semitones (relative to root)
CHORD_INTERVALS = {
    # Triads
    'maj': [0, 4, 7],      # Major triad
    'min': [0, 3, 7],      # Minor triad
    'dim': [0, 3, 6],      # Diminished triad
    'aug': [0, 4, 8],      # Augmented triad
    'sus2': [0, 2, 7],     # Suspended 2nd
    'sus4': [0, 5, 7],     # Suspended 4th
    '5': [0, 7],           # Power chord (5th)

    # Seventh chords
    'maj7': [0, 4, 7, 11],     # Major 7th
    'dom7': [0, 4, 7, 10],     # Dominant 7th
    'min7': [0, 3, 7, 10],     # Minor 7th
    'dim7': [0, 3, 6, 9],      # Diminished 7th
    'min7b5': [0, 3, 6, 10],   # Minor 7th flat 5
    'maj7b5': [0, 4, 6, 11],   # Major 7th flat 5
    '7sus4': [0, 5, 7, 10],    # 7th suspended 4th
    '7b9': [0, 4, 7, 10, 13],  # 7th flat 9

    # Extended chords
    '9': [0, 4, 7, 10, 14],        # Dominant 9th
    'min9': [0, 3, 7, 10, 14],     # Minor 9th
    'maj9': [0, 4, 7, 11, 14],     # Major 9th
    '11': [0, 4, 7, 10, 14, 17],   # Dominant 11th
    'min11': [0, 3, 7, 10, 14, 17], # Minor 11th
    'maj11': [0, 4, 7, 11, 14, 17], # Major 11th
    '13': [0, 4, 7, 10, 14, 21],   # Dominant 13th
    'min13': [0, 3, 7, 10, 14, 21], # Minor 13th
    'maj13': [0, 4, 7, 11, 14, 21], # Major 13th

    # Added tone chords
    '6': [0, 4, 7, 9],          # Major 6th
    'min6': [0, 3, 7, 9],       # Minor 6th
    '6/9': [0, 4, 7, 9, 14],    # 6/9 chord
    '7#11': [0, 4, 7, 10, 18],  # 7th sharp 11

    # Quartal and quintal chords
    'quartal': [0, 5, 10, 15],  # Quartal harmony
    'quintal': [0, 7, 14, 21],  # Quintal harmony
}

# Chord names for display
CHORD_NAMES = {
    'maj': 'Major',
    'min': 'Minor',
    'dim': 'Diminished',
    'aug': 'Augmented',
    'sus2': 'Suspended 2nd',
    'sus4': 'Suspended 4th',
    '5': '5th',
    'maj7': 'Major 7th',
    'dom7': 'Dominant 7th',
    'min7': 'Minor 7th',
    'dim7': 'Diminished 7th',
    'min7b5': 'Minor 7th Flat 5',
    'maj7b5': 'Major 7th Flat 5',
    '7sus4': '7th Suspended 4th',
    '7b9': '7th Flat 9',
    '9': '9th',
    'min9': 'Minor 9th',
    'maj9': 'Major 9th',
    '11': '11th',
    'min11': 'Minor 11th',
    'maj11': 'Major 11th',
    '13': '13th',
    'min13': 'Minor 13th',
    'maj13': 'Major 13th',
    '6': '6th',
    'min6': 'Minor 6th',
    '6/9': '6/9',
    '7#11': '7th Sharp 11',
    'quartal': 'Quartal',
    'quintal': 'Quintal'
}

# Chord qualities (for analysis)
CHORD_QUALITIES = {
    'major': ['maj', '6', '6/9', 'maj7', 'maj9', 'maj11', 'maj13'],
    'minor': ['min', 'min6', 'min7', 'min9', 'min11', 'min13'],
    'dominant': ['dom7', '9', '11', '13', '7b9', '7#11'],
    'diminished': ['dim', 'dim7', 'min7b5'],
    'augmented': ['aug'],
    'suspended': ['sus2', 'sus4', '7sus4'],
    'other': ['5', 'quartal', 'quintal']
}

# ============================================================================
# ARPEGGIO CONSTANTS
# ============================================================================

# Arpeggio directions
ARPEGGIO_DIRECTIONS = ['up', 'down', 'up_down', 'down_up']

# Arpeggio patterns (based on chord intervals)
ARPEGGIO_PATTERNS = {
    'triad': lambda intervals: intervals,  # Basic triad
    '7th': lambda intervals: intervals,    # 7th chord arpeggio
    '9th': lambda intervals: intervals,    # 9th chord arpeggio
    '11th': lambda intervals: intervals,   # 11th chord arpeggio
    '13th': lambda intervals: intervals,   # 13th chord arpeggio
}

# ============================================================================
# ROMAN NUMERAL ANALYSIS
# ============================================================================

# Roman numerals for harmonic analysis
ROMAN_NUMERALS = {
    'major': ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII'],
    'minor': ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii']
}

# Quality symbols for roman numerals
ROMAN_QUALITY_SYMBOLS = {
    'major': '',
    'minor': '',
    'diminished': '°',
    'augmented': '+',
    'dominant_7th': '7',
    'major_7th': 'maj7',
    'minor_7th': '7',
    'diminished_7th': '°7',
    'minor_7th_flat_5': 'ø7'
}

# ============================================================================
# TEMPO AND RHYTHM CONSTANTS
# ============================================================================

# Common tempo markings
TEMPO_MARKINGS = {
    'grave': (40, 60),
    'lento': (45, 60),
    'larghetto': (60, 66),
    'adagio': (66, 76),
    'andante': (76, 108),
    'moderato': (108, 120),
    'allegro': (120, 168),
    'vivace': (168, 176),
    'presto': (168, 200),
    'prestissimo': (200, 500)
}

# Common note durations (in beats)
NOTE_DURATIONS = {
    'whole': 4.0,
    'half': 2.0,
    'quarter': 1.0,
    'eighth': 0.5,
    'sixteenth': 0.25,
    'thirty_second': 0.125,
    'sixty_fourth': 0.0625
}

# Common time signatures
TIME_SIGNATURES = [
    '4/4', '3/4', '2/4', '6/8', '9/8', '12/8',
    '2/2', '3/2', '5/4', '7/4', '5/8', '7/8'
]
