"""
Mingus adapter for the music theory engine.

This module provides conversion between the internal music engine models
and mingus containers for advanced music theory analysis and roman numeral
notation.
"""

from typing import Optional, List, Union, TYPE_CHECKING

# Only import mingus when needed (lazy import)
_mingus = None

def _get_mingus():
    """Lazy import of mingus module."""
    global _mingus
    if _mingus is None:
        try:
            # Import specific containers to avoid issues
            from mingus import containers as mingus_containers
            _mingus = mingus_containers
        except ImportError:
            raise ImportError("mingus is required for this functionality. Install with: pip install mingus")
    return _mingus


class MingusConverter:
    """
    Converter class for transforming between music engine models and mingus containers.
    
    This allows using mingus's extensive capabilities for:
    - Roman numeral analysis
    - Diatonic chord generation
    - Progressions with roman numerals
    - Advanced music theory calculations
    """
    
    # Mapping from internal quality to mingus
    QUALITY_TO_MINGUS = {
        'maj': '',
        'min': 'm',
        'dim': 'dim',
        'aug': 'aug',
        'sus2': 'sus2',
        'sus4': 'sus4',
        'maj7': 'maj7',
        'dom7': '7',
        'min7': 'm7',
        'dim7': 'dim7',
        'min7b5': 'm7b5',
        '7sus4': '7sus4',
    }
    
    # Mapping from mingus to internal quality
    MINGUS_QUALITY_TO_INTERNAL = {
        '': 'maj',
        'major': 'maj',
        'm': 'min',
        'minor': 'min',
        'dim': 'dim',
        'aug': 'aug',
        'sus2': 'sus2',
        'sus4': 'sus4',
        'sus': 'sus4',
        'maj7': 'maj7',
        '7': 'dom7',
        'm7': 'min7',
        'dim7': 'dim7',
        'm7b5': 'min7b5',
    }

    @staticmethod
    def note_to_mingus(note) -> 'mingus.containers.Note':
        """
        Convert a Note object to a mingus Note.
        
        Args:
            note: Note object from music_engine
            
        Returns:
            mingus.containers.Note object
        """
        mingus = _get_mingus()
        
        # Get note name without octave for mingus
        note_name = note.note_name
        octave = note.octave
        
        # Create mingus note - use Note directly from containers
        mingus_note = mingus.Note(note_name, octave)
        
        return mingus_note
    
    @staticmethod
    def mingus_to_note(mingus_note) -> 'music_engine.models.Note':
        """
        Convert a mingus Note to a Note object.
        
        Args:
            mingus_note: mingus.containers.Note object
            
        Returns:
            Note object from music_engine
        """
        from music_engine.models import Note as EngineNote
        
        # Get name with octave
        note_name = f"{mingus_note.name}{mingus_note.octave}"
        
        return EngineNote(note_name)
    
    @staticmethod
    def chord_to_mingus(chord) -> 'mingus.containers.NoteContainer':
        """
        Convert a Chord object to a mingus NoteContainer.
        
        Args:
            chord: Chord object from music_engine
            
        Returns:
            mingus.containers.NoteContainer object
        """
        mingus = _get_mingus()
        
        # Get note names from the chord
        note_names = [note.note_name for note in chord.notes]
        
        # Create mingus NoteContainer (mingus doesn't have a Chord class)
        mingus_chord = mingus.NoteContainer(note_names)
        
        return mingus_chord
    
    @staticmethod
    def mingus_to_chord(mingus_chord, root_note: Optional = None) -> 'music_engine.models.Chord':
        """
        Convert a mingus Chord/NoteContainer to a Chord object.
        
        Args:
            mingus_chord: mingus.containers.NoteContainer or Chord object
            root_note: Optional root note (auto-detected if not provided)
            
        Returns:
            Chord object from music_engine
        """
        from music_engine.models import Note as EngineNote, Chord as EngineChord
        
        # Handle NoteContainer (doesn't have .name, use first note instead)
        if hasattr(mingus_chord, 'notes'):
            # It's a NoteContainer - get notes from it
            notes_list = list(mingus_chord.notes)
            if notes_list:
                # mingus stores notes like 'C-4' (note + octave) or just 'C'
                first_note = str(notes_list[0])
                # Parse the note name (remove octave if present)
                if '-' in first_note:
                    # Format is like 'C-4' means C in octave 4
                    parts = first_note.rsplit('-', 1)
                    root_name = parts[0]
                else:
                    root_name = first_note
                if root_note is None:
                    root_note = EngineNote(root_name)
        elif root_note is None:
            raise ValueError("root_note is required when converting from NoteContainer without notes")
        
        # Determine quality (NoteContainer doesn't have quality)
        internal_quality = 'maj'  # Default
        
        # Get bass note if present
        bass_note = None
        if hasattr(mingus_chord, 'bass'):
            bass_name = mingus_chord.bass
            if bass_name:
                bass_note = EngineNote(f"{bass_name}{root_note.octave}")
        
        return EngineChord(root_note, internal_quality, bass_note)
    
    @staticmethod
    def progression_to_mingus(progression) -> 'mingus.containers.Progressions':
        """
        Convert a Progression object to a mingus Progressions container.
        
        Args:
            progression: Progression object from music_engine
            
        Returns:
            mingus.containers.Progressions object
        """
        mingus = _get_mingus()
        
        # Create progressions container
        progressions = mingus.containers.Progressions()
        
        # Convert each chord
        for chord in progression.chords:
            mingus_chord = MingusConverter.chord_to_mingus(chord)
            progressions.add_chord(mingus_chord)
        
        return progressions
    
    @staticmethod
    def mingus_to_progression(mingus_progression, key: str = 'C') -> 'music_engine.models.Progression':
        """
        Convert a mingus Progressions to a Progression object.
        
        Args:
            mingus_progression: mingus.containers.Progressions object
            key: Key for the progression
            
        Returns:
            Progression object from music_engine
        """
        from music_engine.models import Chord as EngineChord, Progression as EngineProgression, Note as EngineNote
        
        # Parse roman numeral progressions
        chords = []
        
        if hasattr(mingus_progression, 'chords'):
            for mingus_chord in mingus_progression.chords:
                chord = MingusConverter.mingus_to_chord(mingus_chord)
                chords.append(chord)
        
        return EngineProgression(chords, key)
    
    @staticmethod
    def roman_numerals_to_chords(roman_numerals: List[str], key: str = 'C') -> List['music_engine.models.Chord']:
        """
        Convert roman numeral strings to Chord objects.
        
        Args:
            roman_numerals: List of roman numeral strings (e.g., ['I', 'IV', 'V'])
            key: Key for the progression (e.g., 'C', 'Am')
            
        Returns:
            List of Chord objects
        """
        mingus = _get_mingus()
        from music_engine.models import Chord as EngineChord, Note as EngineNote
        
        # Parse the key
        key_note = EngineNote(key)
        
        # Create a diatonic progression from roman numerals
        chords = []
        
        for numeral in roman_numerals:
            # Determine if major or minor
            is_major = numeral[0].isupper()
            is_diminished = numeral.startswith('vi') or numeral.startswith('vii')
            
            # Get degree from roman numeral
            numeral_upper = numeral.upper().replace('B', 'B').replace('#', '').replace('/', '')
            
            # Map roman numerals to scale degrees
            degree_map = {
                'I': 1, 'II': 2, 'III': 3, 'IV': 4, 'V': 5, 'VI': 6, 'VII': 7,
                'I7': 1, 'II7': 2, 'III7': 3, 'IV7': 4, 'V7': 5, 'VI7': 6, 'VII7': 7,
            }
            
            degree = degree_map.get(numeral_upper, 1)
            
            # Build chord from scale
            from music_engine.models import Scale
            scale = Scale(key_note, 'major')
            
            if is_diminished:
                quality = 'dim'
            elif is_major:
                quality = 'maj'
            else:
                quality = 'min'
            
            root = scale.get_degree(degree)
            chord = EngineChord(root, quality)
            chords.append(chord)
        
        return chords
    
    @staticmethod
    def chords_to_roman_numerals(chords: List, key: str = 'C') -> List[str]:
        """
        Convert Chord objects to roman numeral strings.
        
        Args:
            chords: List of Chord objects
            key: Key for the progression
            
        Returns:
            List of roman numeral strings
        """
        from music_engine.models import Note as EngineNote, Scale
        
        key_note = EngineNote(key)
        scale = Scale(key_note, 'major')
        
        roman_numerals = []
        
        for chord in chords:
            # Find the degree of the chord root in the scale
            root_semitone = chord.root.semitone
            
            # Calculate degree (1-7)
            root_in_scale = False
            for i, note in enumerate(scale.notes[:7]):
                if note.semitone == root_semitone:
                    degree = i + 1
                    root_in_scale = True
                    break
            
            if not root_in_scale:
                # Chord is not in the key, use chord name
                roman_numerals.append(chord.name)
                continue
            
            # Determine roman numeral quality
            # Check if chord matches the expected quality for the degree
            is_minor = chord.quality == 'min'
            is_diminished = chord.quality == 'dim'
            
            roman_map = {
                1: ('I', 'i'),
                2: ('II', 'ii'),
                3: ('III', 'iii'),
                4: ('IV', 'iv'),
                5: ('V', 'v'),
                6: ('VI', 'vi'),
                7: ('VII', 'vii'),
            }
            
            major_num, minor_num = roman_map.get(degree, ('I', 'i'))
            
            if is_diminished:
                numeral = minor_num + '°'  # Diminished symbol
            elif is_minor:
                numeral = minor_num
            else:
                numeral = major_num
            
            # Add 7th if applicable
            if '7' in chord.quality:
                if 'maj7' in chord.quality:
                    numeral += 'maj7'
                elif 'dim7' in chord.quality:
                    numeral += '°7'
                elif 'min7' in chord.quality:
                    numeral += '7'
                else:
                    numeral += '7'
            
            roman_numerals.append(numeral)
        
        return roman_numerals
    
    @staticmethod
    def generate_diatonic_progressions(key: str = 'C', 
                                        numeral_strings: Optional[List[str]] = None) -> List['music_engine.models.Chord']:
        """
        Generate diatonic chords for a given key from roman numerals.
        
        Args:
            key: Key for the progression (e.g., 'C', 'Am')
            numeral_strings: Optional list of roman numerals to use
            
        Returns:
            List of diatonic Chord objects
        """
        from music_engine.models import Chord as EngineChord, Note as EngineNote, Scale
        
        key_note = EngineNote(key)
        scale = Scale(key_note, 'major')
        
        # Default diatonic chord qualities for major key
        if numeral_strings is None:
            numeral_strings = ['I', 'ii', 'iii', 'IV', 'V', 'vi', 'vii°']
        
        chords = []
        
        for numeral in numeral_strings:
            # Determine quality from numeral
            numeral_upper = numeral.upper().replace('°', '')
            
            is_upper = numeral[0].isupper()
            has_7th = '7' in numeral
            
            # Check for diminished - VII is diminished in major key
            is_diminished = ('VII' in numeral_upper or '°' in numeral) and not is_upper
            
            # Determine degree (1-7) using proper mapping
            degree = 1
            degree_mapping = {
                'I': 1, 'II': 2, 'III': 3, 'IV': 4, 'V': 5, 'VI': 6, 'VII': 7,
            }
            
            # Check for degree in the cleaned numeral
            for deg_str, deg_num in degree_mapping.items():
                if deg_str in numeral_upper:
                    degree = deg_num
                    break
            
            # Get root note from scale
            root = scale.get_degree(degree)
            
            # Determine quality based on degree and 7th presence
            if is_diminished or degree == 7:
                # vii° is diminished
                quality = 'dim7' if has_7th else 'dim'
            elif not is_upper:
                # Minor chords: ii, iii, vi
                quality = 'min7' if has_7th else 'min'
            elif degree == 5:
                # V is dominant7 in major key
                quality = 'dom7' if has_7th else 'maj'
            else:
                # Major chords: I, IV
                quality = 'maj7' if has_7th else 'maj'
            
            chord = EngineChord(root, quality)
            chords.append(chord)
        
        return chords
    
    @staticmethod
    def analyze_progression(chords: List, key: str = 'C') -> dict:
        """
        Analyze a progression using mingus capabilities.
        
        Args:
            chords: List of Chord objects
            key: Key for analysis
            
        Returns:
            Dictionary with analysis results
        """
        from music_engine.models import Note as EngineNote
        
        analysis = {
            'key': key,
            'roman_numerals': [],
            'functions': [],
            'progressions': [],
        }
        
        # Convert to roman numerals
        analysis['roman_numerals'] = MingusConverter.chords_to_roman_numerals(chords, key)
        
        # Determine harmonic function for each chord
        key_note = EngineNote(key)
        
        for i, chord in enumerate(chords):
            function = 'T'  # Tonic (default)
            
            if i == 0:
                function = 'T'  # Tonic
            elif len(chords) > 1:
                root_semitone = chord.root.semitone - key_note.semitone
                root_semitone = root_semitone % 12
                
                if root_semitone == 7:  # V
                    function = 'D'  # Dominant
                elif root_semitone == 5:  # IV
                    function = 'S'  # Subdominant
                elif root_semitone == 2 or root_semitone == 9:  # ii or vi
                    function = 'T'  # Can be tonic function
            
            analysis['functions'].append(function)
        
        return analysis


# Convenience functions for easy conversion
def note_to_mingus(note):
    """Convert Note to mingus Note."""
    return MingusConverter.note_to_mingus(note)


def mingus_to_note(mingus_note):
    """Convert mingus Note to Note."""
    return MingusConverter.mingus_to_note(mingus_note)


def chord_to_mingus(chord):
    """Convert Chord to mingus Chord."""
    return MingusConverter.chord_to_mingus(chord)


def mingus_to_chord(mingus_chord, root_note: Optional = None):
    """Convert mingus Chord to Chord."""
    return MingusConverter.mingus_to_chord(mingus_chord, root_note)


def progression_to_mingus(progression):
    """Convert Progression to mingus Progressions."""
    return MingusConverter.progression_to_mingus(progression)


def roman_numerals_to_chords(roman_numerals: List[str], key: str = 'C'):
    """Convert roman numerals to Chord list."""
    return MingusConverter.roman_numerals_to_chords(roman_numerals, key)


def chords_to_roman_numerals(chords: List, key: str = 'C'):
    """Convert Chord list to roman numerals."""
    return MingusConverter.chords_to_roman_numerals(chords, key)


def generate_diatonic_progressions(key: str = 'C', numeral_strings: Optional[List[str]] = None):
    """Generate diatonic chords from roman numerals."""
    return MingusConverter.generate_diatonic_progressions(key, numeral_strings)


def scale_to_mingus(scale) -> List[str]:
    """
    Convert a Scale object to a list of note names for mingus.

    Args:
        scale: Scale object from music_engine

    Returns:
        List of note name strings
    """
    # Return note names from the scale
    return [note.note_name for note in scale.notes]


def mingus_to_scale(mingus_scale, scale_type: str = 'major') -> 'music_engine.models.Scale':
    """
    Convert a mingus scale representation to a Scale object.

    Args:
        mingus_scale: List of note names or mingus container
        scale_type: Scale type string for the engine

    Returns:
        Scale object from music_engine
    """
    from music_engine.models import Note as EngineNote, Scale as EngineScale

    # Handle different input types
    if isinstance(mingus_scale, list):
        # List of note names
        note_names = mingus_scale
    elif hasattr(mingus_scale, 'notes'):
        # Mingus container with notes attribute
        note_names = [str(n) for n in mingus_scale.notes]
    else:
        raise ValueError(f"Unsupported mingus scale type: {type(mingus_scale)}")

    # Get root note from first note
    if note_names:
        root_name = note_names[0]
        root_note = EngineNote(root_name)
    else:
        root_note = EngineNote('C')  # Default

    return EngineScale(root_note, scale_type)

