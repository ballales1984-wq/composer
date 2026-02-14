"""
Solver Module

Provides scale and chord suggestion engines, and conflict resolution.
"""

import sys
import os
from typing import Dict, List, Optional, Union

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from models import Note, Chord, Scale, Progression
from core.harmony import HarmonyEngine


class ScaleSolver:
    """
    Suggests scales for given chord contexts.
    
    Provides methods for:
    - Finding scales for a specific chord
    - Suggesting improvisation scales
    - Scale recommendations based on genre/style
    """
    
    def __init__(self, harmony_engine: HarmonyEngine):
        self.harmony_engine = harmony_engine
    
    def suggest_scales_for_chord(self, chord: Chord, key: str = 'C') -> List[Dict]:
        """
        Suggest scales for a given chord.
        
        Args:
            chord: The chord to find scales for
            key: The tonal key context
            
        Returns:
            List of compatible scales with metadata
        """
        # Get all compatible scales from harmony engine
        compatible = self.harmony_engine.find_compatible_scales(chord)
        
        scales = []
        for scale_info in compatible.get('all_scales', []):
            scale = scale_info.get('scale')
            if scale:
                scales.append({
                    'name': scale.name,
                    'notes': scale.note_names,
                    'type': scale.scale_type,
                    'score': scale_info.get('compatibility', {}).get('score', 0),
                })
        
        return scales
    
    def suggest_improvisation_scale(self, chord: Chord) -> Optional[Dict]:
        """
        Suggest the best scale for improvisation over a chord.
        
        Args:
            chord: The chord to improvise over
            
        Returns:
            Recommended scale for improvisation
        """
        # Get tonal scales (most common for improvisation)
        tonal_scales = self.harmony_engine.get_tonal_scales(chord)
        
        if not tonal_scales:
            return None
        
        # Return the highest scoring scale
        best = tonal_scales[0]
        scale = best.get('scale')
        
        if scale:
            return {
                'name': scale.name,
                'notes': scale.note_names,
                'type': scale.scale_type,
                'reasoning': self._get_improvisation_reasoning(chord, scale),
            }
        
        return None
    
    def _get_improvisation_reasoning(self, chord: Chord, scale: Scale) -> str:
        """Generate reasoning for why this scale is recommended."""
        quality = chord.quality
        
        if 'maj7' in quality:
            return "Major 7th chords work well with major scale or Lydian mode"
        elif 'min7' in quality:
            return "Minor 7th chords work well with Dorian or natural minor"
        elif 'dom7' in quality or '7' in quality:
            return "Dominant 7th chords work well with Mixolydian or bebop scales"
        elif 'dim' in quality:
            return "Diminished chords work well with diminished or harmonic minor"
        elif 'aug' in quality:
            return "Augmented chords work well with Lydian or whole tone"
        else:
            return "Compatible scale for improvisation"
    
    def get_mode_for_chord(self, chord: Chord, mode_preference: str = 'dorian') -> Optional[Dict]:
        """
        Get a specific mode for a chord.
        
        Args:
            chord: The chord
            mode_preference: Preferred mode (dorian, phrygian, lydian, etc.)
            
        Returns:
            Scale object for the requested mode
        """
        # Try to create scale with same root and requested mode
        try:
            scale = Scale(chord.root.name.lower(), mode_preference)
            compat = self.harmony_engine.tonal_compatibility(chord, scale)
            
            return {
                'name': scale.name,
                'notes': scale.note_names,
                'type': scale.scale_type,
                'compatibility': compat,
            }
        except:
            return None


class ChordSolver:
    """
    Suggests chords for given contexts.
    
    Provides methods for:
    - Finding next chords in a progression
    - Chord substitutions
    - Voice leading suggestions
    """
    
    def __init__(self, harmony_engine: HarmonyEngine):
        self.harmony_engine = harmony_engine
    
    def suggest_next_chords(self, current_chord: Chord) -> List[Dict]:
        """
        Suggest next chords after the current chord.
        
        Args:
            current_chord: The current chord
            
        Returns:
            List of suggested next chords with metadata
        """
        suggestions = []
        
        # Get compatible chords from the current chord's compatible scales
        for scale_type in ['major', 'minor_natural', 'dorian', 'mixolydian']:
            try:
                scale = Scale(current_chord.root.name.lower(), scale_type)
                chords = self.harmony_engine.find_compatible_chords(scale)
                
                for chord_info in chords[:5]:
                    chord = chord_info.get('chord')
                    if chord and chord.name != current_chord.name:
                        suggestions.append({
                            'name': chord.name,
                            'notes': chord.note_names,
                            'quality': chord.quality,
                            'function': chord_info.get('function', ''),
                            'degree': chord_info.get('degree'),
                            'scale': scale.name,
                        })
            except:
                continue
        
        # Add common jazz progressions
        suggestions.extend(self._get_common_progressions(current_chord))
        
        # Remove duplicates and sort
        seen = set()
        unique = []
        for s in suggestions:
            if s['name'] not in seen:
                seen.add(s['name'])
                unique.append(s)
        
        return unique[:10]
    
    def _get_common_progressions(self, chord: Chord) -> List[Dict]:
        """Get common chord progressions for this chord."""
        suggestions = []
        
        # ii-V-I suggestions for minor 7th chords
        if 'min7' in chord.quality:
            try:
                # ii in key of C is Dm7
                dominant = chord.root.transpose(5)  # Perfect 5th up
                suggestions.append({
                    'name': f"{dominant.name}7",
                    'notes': [dominant.name, 'B', 'D', 'F'],
                    'quality': 'dom7',
                    'function': 'Dominant',
                    'progression_type': 'ii-V',
                })
            except:
                pass
        
        # V7 suggestions for major/minor
        if chord.quality in ['maj', 'min']:
            try:
                dominant = chord.root.transpose(7)  # Perfect 5th up
                suggestions.append({
                    'name': f"{dominant.name}7",
                    'notes': [dominant.name, 'B#', 'D#', 'F#'],
                    'quality': 'dom7',
                    'function': 'Dominant',
                    'progression_type': 'V-I',
                })
            except:
                pass
        
        return suggestions
    
    def suggest_chords_for_scale(self, scale: Scale) -> List[Dict]:
        """
        Suggest chords that work with a scale.
        
        Args:
            scale: The scale
            
        Returns:
            List of compatible chords
        """
        chords = self.harmony_engine.find_compatible_chords(scale)
        
        result = []
        for chord_info in chords:
            chord = chord_info.get('chord')
            if chord:
                result.append({
                    'name': chord.name,
                    'notes': chord.note_names,
                    'quality': chord.quality,
                    'function': chord_info.get('function', ''),
                    'degree': chord_info.get('degree'),
                })
        
        return result
    
    def suggest_continuation(self, chords: List[Chord]) -> List[Dict]:
        """
        Suggest how to continue a progression.
        
        Args:
            chords: Current progression
            
        Returns:
            Suggested continuations
        """
        if not chords:
            return []
        
        last_chord = chords[-1]
        
        # Get next chord suggestions
        next_chords = self.suggest_next_chords(last_chord)
        
        # Add some specific continuation patterns
        continuations = []
        
        # Common endings
        if last_chord.quality == 'dom7':
            # Resolve to tonic
            try:
                tonic = last_chord.root.transpose(-5)
                continuations.append({
                    'name': f"{tonic.name}maj7",
                    'notes': [tonic.name, 'E', 'G#', 'B'],
                    'quality': 'maj7',
                    'resolution_type': 'authentic',
                })
            except:
                pass
        
        return (continuations + next_chords)[:5]
    
    def get_traditional_progressions(self, key: str = 'C') -> Dict[str, List[str]]:
        """
        Get traditional chord progressions in a key.
        
        Args:
            key: The key
            
        Returns:
            Dictionary of named progressions
        """
        return {
            'I-IV-V': [f'{key}', f'{self._transpose_to(key, 5)}', f'{self._transpose_to(key, 7)}'],
            'I-V-vi-IV': [f'{key}', f'{self._transpose_to(key, 7)}', f'{self._transpose_to(key, 9)}m', f'{self._transpose_to(key, 5)}'],
            'ii-V-I': [f'{self._transpose_to(key, 2)}m7', f'{self._transpose_to(key, 5)}7', f'{key}maj7'],
            'I-vi-IV-V': [f'{key}', f'{self._transpose_to(key, 9)}m', f'{self._transpose_to(key, 5)}', f'{self._transpose_to(key, 7)}'],
            'vi-IV-I-V': [f'{self._transpose_to(key, 9)}m', f'{self._transpose_to(key, 5)}', f'{key}', f'{self._transpose_to(key, 7)}'],
        }
    
    def _transpose_to(self, root: str, semitones: int) -> str:
        """Transpose a note by semitones."""
        notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        try:
            idx = notes.index(root.replace('b', '#').replace('♭', '#'))
            return notes[(idx + semitones) % 12]
        except:
            return root


class ConflictResolver:
    """
    Resolves harmonic conflicts between chords and scales.
    
    Provides methods for:
    - Identifying conflicts
    - Suggesting resolutions
    - Voice leading optimizations
    """
    
    def __init__(self, harmony_engine: HarmonyEngine):
        self.harmony_engine = harmony_engine
    
    def find_conflicts(self, chord: Chord, scale: Scale) -> List[Dict]:
        """
        Find conflicts between a chord and scale.
        
        Args:
            chord: The chord
            scale: The scale
            
        Returns:
            List of identified conflicts
        """
        conflicts = []
        
        compat = self.harmony_engine.tonal_compatibility(chord, scale)
        
        if not compat['root_in_scale']:
            conflicts.append({
                'type': 'root_not_in_scale',
                'message': f"Chord root {chord.root.name} is not in the scale",
                'severity': 'high',
            })
        
        for semitone in compat.get('missing_tones', []):
            conflicts.append({
                'type': 'tone_not_in_scale',
                'message': f"Tone {semitone} semitones is not in the scale",
                'severity': 'medium',
            })
        
        return conflicts
    
    def suggest_resolution(self, chord: Chord, scale: Scale) -> Optional[Dict]:
        """
        Suggest how to resolve conflicts.
        
        Args:
            chord: The conflicting chord
            scale: The scale
            
        Returns:
            Resolution suggestion or None
        """
        # Find a compatible scale
        compatible = self.harmony_engine.find_compatible_scales(chord)
        
        if compatible.get('tonal_scales'):
            best = compatible['tonal_scales'][0]
            return {
                'suggested_scale': best.get('scale').name,
                'reason': 'Most compatible scale for this chord',
                'compatibility_score': best.get('compatibility', {}).get('score', 0),
            }
        
        # Try modal interchange
        modal_scales = compatible.get('modal_scales', [])
        if modal_scales:
            return {
                'suggested_scale': modal_scales[0].get('scale').name,
                'reason': 'Modal interchange - borrowed from parallel mode',
                'type': 'modal',
            }
        
        return None
    
    def optimize_voice_leading(self, from_chord: Chord, to_chord: Chord) -> Dict:
        """
        Optimize voice leading between two chords.
        
        Args:
            from_chord: Starting chord
            to_chord: Target chord
            
        Returns:
            Voice leading suggestions
        """
        # Simple voice leading: minimal movement
        suggestions = {
            'from': from_chord.name,
            'to': to_chord.name,
            'movements': [],
        }
        
        from_notes = from_chord.notes
        to_notes = to_chord.notes
        
        # Find closest voice movements
        for i, from_note in enumerate(from_notes[:len(to_notes)]):
            movements = []
            for to_note in to_notes:
                distance = abs(from_note.semitone - to_note.semitone)
                distance = min(distance, 12 - distance)  # Wrap around octave
                movements.append((to_note.name, distance))
            
            movements.sort(key=lambda x: x[1])
            suggestions['movements'].append({
                'from': from_note.name,
                'suggested_to': movements[0][0],
                'distance': movements[0][1],
            })
        
        return suggestions


# Convenience functions
def create_scale_solver() -> ScaleSolver:
    """Create and return a ScaleSolver instance."""
    return ScaleSolver(HarmonyEngine())


def create_chord_solver() -> ChordSolver:
    """Create and return a ChordSolver instance."""
    return ChordSolver(HarmonyEngine())


def create_conflict_resolver() -> ConflictResolver:
    """Create and return a ConflictResolver instance."""
    return ConflictResolver(HarmonyEngine())

