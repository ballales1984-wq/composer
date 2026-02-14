"""
Progression model for the music theory engine.

This module defines the Progression class, which represents musical chord
progressions and their harmonic analysis.
"""

from typing import List, Optional, Union, Set, Dict
from .note import Note
from .chord import Chord
from music_engine.exceptions import InvalidProgressionError, InvalidChordError


class Progression:
    """
    Represents a musical chord progression.

    A Progression contains:
    - List of chords in sequence
    - Key/tonality information
    - Harmonic analysis results
    - Compatible scales

    Examples:
        >>> chords = [Chord('C', 'maj'), Chord('F', 'maj'), Chord('G', 'maj')]
        >>> prog = Progression(chords)
        >>> print(prog.key)  # 'C major - progression.py:26'
    """

    def __init__(self, chords: List[Union[Chord, str]],
                 key: Optional[Union[str, Note]] = None):
        """
        Initialize a Progression.

        Args:
            chords: List of Chord objects or chord specification strings
            key: Optional key specification (Note object or string)

        Raises:
            InvalidProgressionError: If chords list is empty or invalid
            InvalidChordError: If any chord cannot be created
        """
        if not chords:
            raise InvalidProgressionError("Chords list cannot be empty", 
                                        details={'chords': chords})
        
        self._chords = []
        for chord in chords:
            if isinstance(chord, str):
                from music_engine.core.chords import ChordBuilder
                chord = ChordBuilder.parse_chord_string(chord)
            self._chords.append(chord)

        self._key = Note(key) if key and not isinstance(key, Note) else key
        self._analysis = self._analyze_progression()

    @property
    def chords(self) -> List[Chord]:
        """Get the chords in the progression."""
        return self._chords.copy()

    @property
    def key(self) -> Optional[Note]:
        """Get the detected or specified key."""
        # Return explicitly set key, or detect from first chord
        if self._key:
            return self._key
        # Try to get detected key from analysis
        if self._analysis and self._analysis.get('detected_key'):
            return self._analysis['detected_key']
        return None

    @property
    def key_name(self) -> Optional[str]:
        """Get the key name."""
        return self._key.name if self._key else None

    @property
    def all_notes(self) -> Set[Note]:
        """
        Get all unique notes used in the progression.

        Returns:
            Set of Note objects
        """
        notes = set()
        for chord in self._chords:
            notes.update(chord.notes)
        return notes

    @property
    def all_note_names(self) -> Set[str]:
        """
        Get all unique note names used in the progression.

        Returns:
            Set of note name strings
        """
        return {note.name for note in self.all_notes}

    @property
    def all_semitones(self) -> Set[int]:
        """
        Get all unique semitone values used in the progression.

        Returns:
            Set of semitone integers
        """
        return {note.semitone for note in self.all_notes}

    @property
    def analysis(self) -> Dict:
        """Get the harmonic analysis results."""
        return self._analysis.copy()

    def _analyze_progression(self) -> Dict:
        """
        Analyze the progression to determine key, function, etc.

        Returns:
            Dictionary with analysis results
        """
        analysis = {
            'detected_key': None,
            'confidence': 0.0,
            'roman_numerals': [],
            'functions': [],
            'compatible_scales': [],
            'complexity': 'simple'  # simple, intermediate, complex
        }

        if not self._chords:
            return analysis

        # Simple key detection based on first chord
        first_chord = self._chords[0]
        if first_chord.quality == 'maj':
            analysis['detected_key'] = first_chord.root
            analysis['confidence'] = 0.8
        elif first_chord.quality == 'min':
            # Could be minor key or relative major
            analysis['detected_key'] = first_chord.root
            analysis['confidence'] = 0.6

        # Calculate complexity
        qualities = [chord.quality for chord in self._chords]
        if any(q in ['9', '11', '13', '7b9', '7#11'] for q in qualities):
            analysis['complexity'] = 'complex'
        elif any(q in ['maj7', 'min7', 'dom7', 'dim7'] for q in qualities):
            analysis['complexity'] = 'intermediate'

        return analysis

    def get_compatible_scales(self) -> List['Scale']:
        """
        Get scales that are compatible with this progression.

        Returns:
            List of Scale objects that contain all progression notes
        """
        from music_engine.core.scales import ScaleBuilder

        if not self._chords:
            return []

# Get all notes in the progression
        prog_notes = self.all_notes
        prog_semitones = {note.chroma for note in prog_notes}

        compatible_scales = []

        # Test common scales
        common_scale_types = [
            'major', 'minor_natural', 'minor_harmonic', 'minor_melodic',
            'dorian', 'phrygian', 'lydian', 'mixolydian', 'locrian',
            'pentatonic_major', 'pentatonic_minor', 'blues_minor'
        ]

        # Try scales from each root note in the progression
        tested_roots = set()
        for chord in self._chords[:3]:  # Check first few chords
            root = chord.root
            if root in tested_roots:
                continue
            tested_roots.add(root)

            for scale_type in common_scale_types:
                try:
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
                    scale_semitones = set(scale.semitones)

                    # Check if scale contains all progression notes
                    if prog_semitones.issubset(scale_semitones):
                        compatible_scales.append(scale)

                except Exception:
                    continue

        # Remove duplicates while preserving order
        seen = set()
        unique_scales = []
        for scale in compatible_scales:
            scale_id = (scale.root, scale.scale_type)
            if scale_id not in seen:
                seen.add(scale_id)
                unique_scales.append(scale)

        return unique_scales

    def get_scale_suggestions(self, max_suggestions: int = 5) -> List['Scale']:
        """
        Get scale suggestions for improvising over this progression.

        Returns:
            List of recommended Scale objects
        """
        compatible = self.get_compatible_scales()

        if len(compatible) <= max_suggestions:
            return compatible

        # Prioritize certain scales
        priority_order = [
            'mixolydian', 'dorian', 'minor_natural', 'major',
            'lydian', 'phrygian', 'minor_harmonic', 'blues_minor',
            'pentatonic_minor', 'pentatonic_major'
        ]

        # Sort by priority
        def get_priority(scale):
            try:
                return priority_order.index(scale.scale_type)
            except ValueError:
                return len(priority_order)

        compatible.sort(key=get_priority)
        return compatible[:max_suggestions]

    def transpose(self, semitones: int) -> 'Progression':
        """
        Transpose the entire progression by semitones.

        Args:
            semitones: Number of semitones to transpose

        Returns:
            New Progression object with transposed chords
        """
        transposed_chords = [chord.transpose(semitones) for chord in self._chords]
        transposed_key = self._key.transpose(semitones) if self._key else None

        return Progression(transposed_chords, transposed_key)

    def extend(self, additional_chords: List[Union[Chord, str]]) -> 'Progression':
        """
        Extend the progression with additional chords.

        Args:
            additional_chords: Chords to add

        Returns:
            New Progression object with extended sequence
        """
        new_chords = self._chords.copy()

        for chord in additional_chords:
            if isinstance(chord, str):
                from music_engine.core.chords import ChordBuilder
                chord = ChordBuilder.parse_chord_string(chord)
            new_chords.append(chord)

        return Progression(new_chords, self._key)

    def get_similar_progressions(self) -> List[List[str]]:
        """
        Get similar chord progressions for inspiration.

        Returns:
            List of similar progression chord name lists
        """
        # This is a simplified implementation
        # In a real system, this would use a database of known progressions

        # Common progressions starting with same first chord
        if not self._chords:
            return []

        first_chord = self._chords[0]
        similar = []

        if first_chord.quality == 'maj':
            similar.extend([
                ['I', 'IV', 'V', 'I'],  # Perfect cadence
                ['I', 'vi', 'IV', 'V'], # Pop progression
                ['I', 'V', 'vi', 'IV'], # Circle progression
                ['I', 'IV', 'I', 'V'],  # Simple blues
            ])
        elif first_chord.quality == 'min':
            similar.extend([
                ['i', 'iv', 'v', 'i'],  # Minor cadence
                ['i', 'VI', 'III', 'VII'], # Minor key progression
            ])

        return similar

    def __str__(self) -> str:
        """String representation of the progression."""
        chord_names = [chord.name for chord in self._chords]
        return " → ".join(chord_names)

    def __repr__(self) -> str:
        """Detailed string representation for debugging."""
        return f"Progression({self._chords}, key={self._key})"

    def __len__(self) -> int:
        """Get the number of chords in the progression."""
        return len(self._chords)

    def __getitem__(self, index: int) -> Chord:
        """Get chord at index."""
        return self._chords[index]

    def __iter__(self):
        """Iterate over chords in the progression."""
        return iter(self._chords)

    # ==================== Conversion Methods ====================
    
    def to_music21(self):
        """
        Convert this Progression to a music21 stream.
        
        Returns:
            music21.stream.Stream object
            
        Requires:
            music21 library (pip install music21)
        """
        from music_engine.integrations.music21_adapter import progression_to_music21_stream
        return progression_to_music21_stream(self)
    
    @classmethod
    def from_music21(cls, m21_stream):
        """
        Create a Progression from a music21 stream.
        
        Args:
            m21_stream: music21.stream.Stream object
            
        Returns:
            Progression object
        """
        from music_engine.integrations.music21_adapter import stream_to_progression
        return stream_to_progression(m21_stream)
    
    def to_mingus(self):
        """
        Convert this Progression to a mingus Progressions.
        
        Returns:
            mingus.containers.Progressions object
            
        Requires:
            mingus library (pip install mingus)
        """
        from music_engine.integrations.mingus_adapter import progression_to_mingus
        return progression_to_mingus(self)
    
    @classmethod
    def from_mingus(cls, mingus_progression, key: str = 'C'):
        """
        Create a Progression from a mingus Progressions.
        
        Args:
            mingus_progression: mingus.containers.Progressions object
            key: Key for the progression
            
        Returns:
            Progression object
        """
        from music_engine.integrations.mingus_adapter import mingus_to_progression
        return mingus_to_progression(mingus_progression, key)
    
    def to_roman_numerals(self) -> List[str]:
        """
        Convert progression to Roman numeral notation.

        Returns:
            List of Roman numeral strings
        """
        from music_engine.integrations.mingus_adapter import chords_to_roman_numerals
        return chords_to_roman_numerals(self._chords, self._key.name if self._key else 'C')
    
    @classmethod
    def from_roman_numerals(cls, roman_numerals: List[str], key: str = 'C'):
        """
        Create a Progression from Roman numeral strings.
        
        Args:
            roman_numerals: List of roman numeral strings (e.g., ['I', 'IV', 'V'])
            key: Key for the progression (e.g., 'C', 'Am')
            
        Returns:
            Progression object
        """
        from music_engine.integrations.mingus_adapter import roman_numerals_to_chords
        chords = roman_numerals_to_chords(roman_numerals, key)
        return cls(chords, key)
