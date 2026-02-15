"""
Harmony engine module for the music theory engine.

This module provides the HarmonyEngine class for analyzing chord-scale
compatibility using tonal and modal logic.
"""

from typing import List, Dict, Optional, Union, Tuple
import logging

# Import models
import sys
import os

# Ensure parent directory is in path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from models.note import Note
from models.chord import Chord
from models.scale import Scale
from models.fretboard import GuitarFretboard

# Import intervals
from core.intervals import Interval


class HarmonyEngine:
    """
    Engine for analyzing harmonic relationships between chords and scales.
    
    Provides methods for:
    - Tonal compatibility analysis
    - Modal compatibility analysis
    - Finding compatible scales for a chord
    - Finding compatible chords for a scale
    
    Examples:
        >>> engine = HarmonyEngine()
        >>> engine.find_compatible_scales(Chord('C', 'maj7'))
    """
    
    # Scale families and their characteristic intervals
    SCALE_FAMILIES = {
        'major': {
            'name': 'Major (Ionian)',
            'degrees': [0, 2, 4, 5, 7, 9, 11],
            'characteristic': [4, 11],  # Major 3rd, Major 7th
            'modes': ['ionian', 'dorian', 'phrygian', 'lydian', 'mixolydian', 'aeolian', 'locrian']
        },
        'minor_natural': {
            'name': 'Natural Minor (Aeolian)',
            'degrees': [0, 2, 3, 5, 7, 8, 10],
            'characteristic': [3, 10],  # Minor 3rd, Minor 7th
            'modes': ['aeolian', 'locrian', 'ionian', 'dorian', 'phrygian', 'lydian', 'mixolydian']
        },
        'minor_harmonic': {
            'name': 'Harmonic Minor',
            'degrees': [0, 2, 3, 5, 7, 8, 11],
            'characteristic': [3, 8, 11],  # Minor 3rd, Minor 6th, Major 7th
            'modes': []
        },
        'minor_melodic': {
            'name': 'Melodic Minor',
            'degrees': [0, 2, 3, 5, 7, 9, 11],
            'characteristic': [3, 9, 11],  # Minor 3rd, Major 6th, Major 7th
            'modes': ['melodic_minor', 'dorian_b2', 'lydian_aug', 'lydian_dom', 'mixolydian_b6', 'locrian']
        },
        'dorian': {
            'name': 'Dorian',
            'degrees': [0, 2, 3, 5, 7, 9, 10],
            'characteristic': [3, 10],  # Minor 3rd, Minor 7th
            'modes': []
        },
        'phrygian': {
            'name': 'Phrygian',
            'degrees': [0, 1, 3, 5, 7, 8, 10],
            'characteristic': [1, 8],  # Minor 2nd, Minor 6th
            'modes': []
        },
        'lydian': {
            'name': 'Lydian',
            'degrees': [0, 2, 4, 6, 7, 9, 11],
            'characteristic': [6, 11],  # Augmented 4th, Major 7th
            'modes': []
        },
        'mixolydian': {
            'name': 'Mixolydian',
            'degrees': [0, 2, 4, 5, 7, 9, 10],
            'characteristic': [4, 10],  # Major 3rd, Minor 7th
            'modes': []
        },
        'pentatonic_major': {
            'name': 'Major Pentatonic',
            'degrees': [0, 2, 4, 7, 9],
            'characteristic': [],
            'modes': []
        },
        'pentatonic_minor': {
            'name': 'Minor Pentatonic',
            'degrees': [0, 3, 5, 7, 10],
            'characteristic': [],
            'modes': []
        },
    }
    
    # Chord qualities and their compatible scale types
    CHORD_SCALE_COMPATIBILITY = {
        'maj': ['major', 'lydian', 'mixolydian', 'pentatonic_major'],
        'min': ['minor_natural', 'dorian', 'phrygian', 'pentatonic_minor'],
        'dim': ['minor_harmonic', 'locrian', 'diminished'],
        'aug': ['lydian', 'whole_tone', 'augmented'],
        'dom7': ['mixolydian', 'dorian', 'phrygian', 'lydian_dom'],
        'maj7': ['major', 'lydian', 'ionian'],
        'min7': ['dorian', 'minor_natural', 'phrygian'],
        'min7b5': ['locrian', 'phrygian'],
        'dim7': ['locrian', 'diminished'],
    }
    
    def __init__(self):
        """Initialize the HarmonyEngine."""
        self.logger = logging.getLogger(__name__)
        self.fretboard = GuitarFretboard()
    
    # ==================== Tonal Compatibility ====================
    
    def tonal_compatibility(self, chord: Chord, scale: Scale) -> Dict:
        """
        Analyze tonal compatibility between a chord and a scale.
        
        Tonal compatibility is based on:
        - The root of the chord being in the scale
        - All chord tones being available in the scale
        - Diatonic function of the chord within the scale
        
        Args:
            chord: The chord to analyze
            scale: The scale to check against
            
        Returns:
            Dictionary with compatibility analysis
        """
        # Get chord intervals (semitones modulo 12)
        chord_semitones = set(s % 12 for s in chord.semitones)
        # Get scale intervals
        scale_semitones = set(scale.semitones)
        
        # Check if chord root is in scale (compare modulo 12)
        root_in_scale = (chord.root.semitone % 12) in scale_semitones
        
        # Check if all chord tones are in scale
        all_tones_in_scale = chord_semitones.issubset(scale_semitones)
        
        # Calculate matching tones
        matching_tones = chord_semitones.intersection(scale_semitones)
        
        # Calculate missing tones (in chord but not in scale)
        missing_tones = chord_semitones - scale_semitones
        
        # Determine compatibility score (0-100)
        if not root_in_scale:
            score = 0
        elif all_tones_in_scale:
            score = 100
        else:
            # Score based on percentage of matching tones
            score = int(len(matching_tones) / len(chord_semitones) * 100)
        
        # Determine relationship type
        if not root_in_scale:
            relationship = 'none'
        elif all_tones_in_scale:
            if chord.root.semitone % 12 == scale.root.semitone % 12:
                relationship = 'diatonic'
            else:
                relationship = 'borrowed'
        else:
            relationship = 'partial'
        
        return {
            'score': score,
            'relationship': relationship,
            'root_in_scale': root_in_scale,
            'all_tones_in_scale': all_tones_in_scale,
            'matching_tones': len(matching_tones),
            'total_chord_tones': len(chord_semitones),
            'missing_tones': list(missing_tones),
            'chord_semitones': list(chord_semitones),
            'scale_semitones': list(scale_semitones),
        }
    
    def get_tonal_scales(self, chord: Chord) -> List[Dict]:
        """
        Get scales that are tonally compatible with a chord.
        
        Args:
            chord: The chord to find compatible scales for
            
        Returns:
            List of dictionaries with scale and compatibility info
        """
        results = []
        chord_quality = chord.quality
        
        # Get base quality for compatibility lookup
        base_quality = chord_quality
        if 'maj7' in chord_quality:
            base_quality = 'maj7'
        elif 'dom7' in chord_quality or '7' in chord_quality:
            base_quality = 'dom7'
        elif 'min7' in chord_quality:
            base_quality = 'min7'
        elif 'min' in chord_quality:
            base_quality = 'min'
        
        # Get root note name without octave
        root_name = self._get_root_name(chord)
        
        # Try scales based on chord quality
        compatible_types = self.CHORD_SCALE_COMPATIBILITY.get(base_quality, 
                                                               list(self.SCALE_FAMILIES.keys()))
        
        for scale_type in compatible_types:
            try:
                scale = Scale(root_name, scale_type)
                compatibility = self.tonal_compatibility(chord, scale)
                
                if compatibility['score'] >= 70:  # Only include reasonably compatible
                    results.append({
                        'scale': scale,
                        'scale_type': scale_type,
                        'scale_name': scale.name,
                        'compatibility': compatibility,
                    })
            except Exception as e:
                self.logger.warning(f"Error creating scale {scale_type}: {e}")
                continue
        
        # Sort by compatibility score
        results.sort(key=lambda x: x['compatibility']['score'], reverse=True)
        
        return results
    
    # ==================== Modal Compatibility ====================
    
    def modal_compatibility(self, chord: Chord, scale: Scale) -> Dict:
        """
        Analyze modal compatibility between a chord and a scale.
        
        Modal compatibility focuses on:
        - Characteristic intervals of the mode
        - Color tones and extensions
        - Modal interchange possibilities
        
        Args:
            chord: The chord to analyze
            scale: The scale to check against
            
        Returns:
            Dictionary with modal compatibility analysis
        """
        # Get chord and scale intervals
        chord_intervals = chord.intervals
        scale_intervals = scale.intervals
        
        # Find characteristic intervals in scale
        scale_family = self.SCALE_FAMILIES.get(scale.scale_type, {})
        characteristic = scale_family.get('characteristic', [])
        
        # Check if chord matches characteristic intervals
        matching_characteristic = []
        for char_interval in characteristic:
            if char_interval % 12 in [i % 12 for i in chord_intervals]:
                matching_characteristic.append(char_interval)
        
        # Calculate modal tension (color tones not in chord)
        scale_only_intervals = set(scale_intervals) - set(chord_intervals)
        
        # Modal tension score
        tension_score = len(scale_only_intervals) * 10
        
        # Determine modal relationship
        modal_relationship = self._determine_modal_relationship(chord, scale)
        
        return {
            'modal_relationship': modal_relationship,
            'characteristic_intervals': characteristic,
            'matching_characteristic': matching_characteristic,
            'tension_score': min(100, tension_score),
            'available_extensions': list(scale_only_intervals),
        }
    
    def _determine_modal_relationship(self, chord: Chord, scale: Scale) -> str:
        """Determine the modal relationship between chord and scale."""
        chord_root = chord.root.semitone
        scale_root = scale.root.semitone
        
        # Same root
        if chord_root == scale_root:
            return 'parallel'
        
        # Find which degree of the scale the chord root is
        scale_intervals = scale.intervals
        for i, interval in enumerate(scale_intervals):
            if interval % 12 == chord_root % 12:
                return f'degree_{i + 1}'
        
        return 'borrowed'
    
    def get_modal_scales(self, chord: Chord) -> List[Dict]:
        """
        Get scales that are modally compatible with a chord.
        
        This includes modal interchange - using chords from parallel modes.
        
        Args:
            chord: The chord to find modally compatible scales for
            
        Returns:
            List of dictionaries with scale and modal compatibility info
        """
        results = []
        
        # Get root note name without octave
        root_name = self._get_root_name(chord)
        
        # Get all available scale types
        for scale_type in self.SCALE_FAMILIES.keys():
            try:
                # Try with same root
                scale = Scale(root_name, scale_type)
                modal_comp = self.modal_compatibility(chord, scale)
                
                results.append({
                    'scale': scale,
                    'scale_type': scale_type,
                    'scale_name': scale.name,
                    'modal_compatibility': modal_comp,
                })
                
                # Also try with different roots (modal interchange)
                for root_offset in [3, 5, 7, 8, 9]:  # Common modal relationships
                    try:
                        new_root = chord.root.transpose(root_offset)
                        # Get just the note name without octave
                        new_root_name = self._get_note_name_without_octave(new_root)
                        scale = Scale(new_root_name, scale_type)
                        modal_comp = self.modal_compatibility(chord, scale)
                        
                        results.append({
                            'scale': scale,
                            'scale_type': scale_type,
                            'scale_name': scale.name,
                            'modal_compatibility': modal_comp,
                            'interchange': True,
                        })
                    except:
                        continue
            except Exception as e:
                continue
        
        # Sort by tension score (lower is more compatible)
        results.sort(key=lambda x: x['modal_compatibility']['tension_score'])
        
        return results[:10]  # Return top 10
    
    # ==================== General Compatibility ====================
    
    def find_compatible_scales(self, chord: Chord) -> Dict:
        """
        Find all compatible scales for a chord.
        
        Combines tonal and modal analysis.
        
        Args:
            chord: The chord to analyze
            
        Returns:
            Dictionary with tonal and modal compatible scales
        """
        tonal_scales = self.get_tonal_scales(chord)
        modal_scales = self.get_modal_scales(chord)
        
        # Merge results, avoiding duplicates
        seen = set()
        merged = []
        
        for scale_info in tonal_scales + modal_scales:
            key = (scale_info['scale'].root.name, scale_info['scale'].scale_type)
            if key not in seen:
                seen.add(key)
                merged.append(scale_info)
        
        return {
            'chord': chord.name,
            'chord_notes': chord.note_names,
            'tonal_scales': tonal_scales[:5],
            'modal_scales': modal_scales[:5],
            'all_scales': merged[:10],
        }
    
    def find_compatible_chords(self, scale: Scale) -> List[Dict]:
        """
        Find all chords that are compatible with a scale.
        
        Args:
            scale: The scale to analyze
            
        Returns:
            List of compatible chords with their function
        """
        results = []
        scale_semitones = set(scale.semitones)
        
        # Generate diatonic triads
        for degree in range(1, 8):
            try:
                triad = scale.get_triad(degree)
                
                # Check compatibility
                chord_semitones = set(triad.semitones)
                in_scale = chord_semitones.issubset(scale_semitones)
                
                # Determine function
                functions = {1: 'I', 2: 'ii', 3: 'iii', 4: 'IV', 5: 'V', 6: 'vi', 7: 'vii°'}
                quality_suffix = ''
                if triad.quality == 'min':
                    quality_suffix = 'm' if degree not in [2, 3, 6] else ''
                elif triad.quality == 'dim':
                    quality_suffix = '°'
                
                roman = functions.get(degree, str(degree))
                
                results.append({
                    'chord': triad,
                    'chord_name': triad.name,
                    'degree': degree,
                    'roman': roman + quality_suffix,
                    'function': self._get_chord_function(degree, triad.quality),
                    'in_scale': in_scale,
                })
            except:
                continue
        
        # Add seventh chords
        seventh_qualities = ['maj7', 'dom7', 'min7', 'min7b5']
        for degree in range(1, 8):
            for quality in seventh_qualities:
                try:
                    chord = scale.get_chord(degree, quality)
                    chord_semitones = set(chord.semitones)
                    in_scale = chord_semitones.issubset(scale_semitones)
                    
                    if in_scale:
                        results.append({
                            'chord': chord,
                            'chord_name': chord.name,
                            'degree': degree,
                            'quality': quality,
                            'in_scale': True,
                        })
                except:
                    continue
        
        return results
    
    def _get_chord_function(self, degree: int, quality: str) -> str:
        """Get the harmonic function of a chord."""
        functions = {
            1: 'Tonic',
            2: 'Supertonic',
            3: 'Mediant',
            4: 'Subdominant',
            5: 'Dominant',
            6: 'Submediant',
            7: 'Leading Tone',
        }
        
        base_function = functions.get(degree, 'Unknown')
        
        if quality == 'dim':
            return f'{base_function} (diminished)'
        elif quality == 'min':
            return f'{base_function} (minor)'
        else:
            return f'{base_function} (major)'
    
    # ==================== Input Analysis ====================
    
    def analyze_input(self, input_str: str) -> Dict:
        """
        Analyze an input string that could be a chord or a scale.
        
        Args:
            input_str: Input like 'Cmaj7', 'C major', 'A minor', etc.
            
        Returns:
            Dictionary with analysis results
        """
        input_str = input_str.strip()
        
        # Try to parse as chord first
        chord_result = self._try_parse_chord(input_str)
        if chord_result:
            return chord_result
        
        # Try to parse as scale
        scale_result = self._try_parse_scale(input_str)
        if scale_result:
            return scale_result
        
        # Could not parse
        return {
            'success': False,
            'error': f"Could not parse input: {input_str}",
            'input': input_str,
        }
    
    def _try_parse_chord(self, input_str: str) -> Optional[Dict]:
        """Try to parse input as a chord."""
        # Common chord patterns
        import re
        
        # Match patterns like: C, Cm, C7, Cmaj7, Cdim, Caug, etc.
        pattern = r'^([A-G][#b]?)(.*)$'
        match = re.match(pattern, input_str)
        
        if not match:
            return None
        
        root_str = match.group(1)
        quality_str = match.group(2).strip()
        
        if not quality_str:
            quality_str = 'maj'  # Default to major
        
        try:
            chord = Chord(root_str, quality_str)
            
            # Get compatible scales
            compatible = self.find_compatible_scales(chord)
            
            # Get fretboard positions
            positions = self._get_chord_positions(chord)
            
            return {
                'success': True,
                'type': 'chord',
                'chord': chord,
                'name': chord.name,
                'root': chord.root.name,
                'quality': chord.quality,
                'notes': chord.note_names,
                # Use modulo 12 to get intervals from semitones
                'intervals': [Interval(s % 12).name for s in chord.semitones],
                'compatible_scales': compatible,
                'fretboard_positions': positions,
            }
        except Exception as e:
            self.logger.debug(f"Could not parse as chord: {e}")
            return None
    
    def _try_parse_scale(self, input_str: str) -> Optional[Dict]:
        """Try to parse input as a scale."""
        import re
        
        # Try patterns like: "C major", "A minor", "D dorian", etc.
        patterns = [
            r'^([A-G][#b]?)\s+(major)$',
            r'^([A-G][#b]?)\s+(minor|natural\s*minor)$',
            r'^([A-G][#b]?)\s+(harmonic\s*minor)$',
            r'^([A-G][#b]?)\s+(melodic\s*minor)$',
            r'^([A-G][#b]?)\s+(dorian|phrygian|lydian|mixolydian|locrian)$',
            r'^([A-G][#b]?)\s+(pentatonic\s*major|pentatonic\s*minor)$',
            r'^([A-G][#b]?)\s+(blues)$',
        ]
        
        for pattern in patterns:
            match = re.match(pattern, input_str, re.IGNORECASE)
            if match:
                root_str = match.group(1)
                scale_type = match.group(2).lower().replace(' ', '_')
                
                # Normalize scale type
                if scale_type == 'minor':
                    scale_type = 'minor_natural'
                elif scale_type == 'natural_minor':
                    scale_type = 'minor_natural'
                elif scale_type == 'harmonic_minor':
                    scale_type = 'minor_harmonic'
                elif scale_type == 'melodic_minor':
                    scale_type = 'minor_melodic'
                elif scale_type == 'pentatonic_major':
                    scale_type = 'pentatonic_major'
                elif scale_type == 'pentatonic_minor':
                    scale_type = 'pentatonic_minor'
                elif scale_type == 'blues':
                    scale_type = 'blues_minor'
                
                try:
                    scale = Scale(root_str, scale_type)
                    
                    # Get compatible chords
                    compatible = self.find_compatible_chords(scale)
                    
                    # Get fretboard positions
                    positions = self._get_scale_positions(scale)
                    
                    # Get diatonic chords
                    diatonic = self._get_diatonic_chords(scale)
                    
                    return {
                        'success': True,
                        'type': 'scale',
                        'scale': scale,
                        'name': scale.name,
                        'root': scale.root.name,
                        'scale_type': scale.scale_type,
                        'notes': scale.note_names,
                        'intervals': [str(i) for i in scale.intervals],
                        'degrees': {str(i+1): n.name for i, n in enumerate(scale.notes[:7])},
                        'compatible_chords': compatible,
                        'diatonic_chords': diatonic,
                        'fretboard_positions': positions,
                    }
                except Exception as e:
                    self.logger.debug(f"Could not parse as scale: {e}")
                    return None
        
        return None
    
    def _get_chord_positions(self, chord: Chord) -> Dict:
        """Get fretboard positions for chord notes."""
        positions = {}
        
        for note in chord.notes:
            note_positions = self.fretboard.find_note_positions(note, max_fret=12)
            positions[note.name] = [
                {'string': p.string, 'fret': p.fret} 
                for p in note_positions[:3]  # Limit to first 3 positions
            ]
        
        return positions
    
    def _get_scale_positions(self, scale: Scale) -> Dict:
        """Get fretboard positions for scale notes."""
        positions = {}
        
        for note in scale.notes:
            note_positions = self.fretboard.find_note_positions(note, max_fret=12)
            positions[note.name] = [
                {'string': p.string, 'fret': p.fret} 
                for p in note_positions[:2]  # Limit to first 2 positions
            ]
        
        return positions
    
    def _get_diatonic_chords(self, scale: Scale) -> List[Dict]:
        """Get diatonic chords for a scale."""
        chords = []
        
        for degree in range(1, 8):
            try:
                triad = scale.get_triad(degree)
                chords.append({
                    'degree': degree,
                    'chord': triad.name,
                    'notes': triad.note_names,
                    'quality': triad.quality,
                })
                
                # Add seventh chord
                seventh = scale.get_chord(degree, 'maj7' if degree in [1, 4, 5] else 'min7')
                chords[-1]['seventh'] = seventh.name
            except:
                continue
        
        return chords
    
    # ==================== Helper Methods ====================
    
    def _get_root_name(self, chord: Chord) -> str:
        """
        Get the root note name without octave from a chord.
        
        Args:
            chord: The chord to get root from
            
        Returns:
            Root note name without octave (e.g., 'C' not 'C4')
        """
        # chord.root.name returns something like 'C4', we need just 'C'
        return self._get_note_name_without_octave(chord.root)
    
    def _get_note_name_without_octave(self, note) -> str:
        """
        Get note name without octave.
        
        Args:
            note: Note object or note name string
            
        Returns:
            Note name without octave
        """
        if hasattr(note, 'name'):
            # It's a Note object
            name = note.name
        else:
            # It's a string
            name = str(note)
        
        # Remove octave number at the end (e.g., 'C4' -> 'C', 'Db3' -> 'Db')
        import re
        return re.sub(r'\d+$', '', name)


# Convenience function
def create_harmony_engine() -> HarmonyEngine:
    """Create and return a HarmonyEngine instance."""
    return HarmonyEngine()


def analyze(input_str: str) -> Dict:
    """Analyze an input string (chord or scale)."""
    engine = HarmonyEngine()
    return engine.analyze_input(input_str)

