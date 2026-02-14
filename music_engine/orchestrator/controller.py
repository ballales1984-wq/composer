"""
Controller Module

Coordinates input handling, output formatting, and module orchestration
for the music theory engine.
"""

import sys
import os
from typing import Dict, List, Optional, Union, Any

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from models import Note, Chord, Scale, Progression
from core.harmony import HarmonyEngine
from .solver import ScaleSolver, ChordSolver, ConflictResolver
from .genre_rules import GenreDetector, GenreRules, JazzRules, PopRules, RockRules, BluesRules


class InputController:
    """
    Handles various input types and converts them to internal representations.
    
    Supports:
    - Chord strings (Cmaj7, Dm7, G7)
    - Scale strings (C major, A minor)
    - Roman numeral progressions (I-IV-V, ii-V-I)
    - Note lists
    """
    
    def __init__(self):
        self.harmony_engine = HarmonyEngine()
        self.scale_solver = ScaleSolver(self.harmony_engine)
        self.chord_solver = ChordSolver(self.harmony_engine)
        self.genre_detector = GenreDetector()
    
    def parse_input(self, input_str: str, context: Optional[Dict] = None) -> Dict:
        """
        Parse any input string and return structured data.
        
        Args:
            input_str: The input to parse (chord, scale, progression)
            context: Optional context (genre, key, etc.)
            
        Returns:
            Dictionary with parsed data and metadata
        """
        input_str = input_str.strip()
        
        # Try parsing as single chord
        chord_result = self._try_parse_chord(input_str)
        if chord_result:
            return chord_result
        
        # Try parsing as single scale
        scale_result = self._try_parse_scale(input_str)
        if scale_result:
            return scale_result
        
        # Try parsing as progression
        progression_result = self._try_parse_progression(input_str)
        if progression_result:
            return progression_result
        
        # Try detecting genre from input
        genre = self.genre_detector.detect_from_input(input_str)
        
        return {
            'success': False,
            'error': f"Could not parse input: {input_str}",
            'input': input_str,
        }
    
    def _try_parse_chord(self, input_str: str) -> Optional[Dict]:
        """Try to parse input as a chord."""
        import re
        
        pattern = r'^([A-G][#b]?)(.*)$'
        match = re.match(pattern, input_str)
        
        if not match:
            return None
        
        root_str = match.group(1)
        quality_str = match.group(2).strip() or 'maj'
        
        try:
            chord = Chord(root_str, quality_str)
            return {
                'success': True,
                'type': 'chord',
                'chord': chord,
                'name': chord.name,
                'notes': chord.note_names,
                'quality': chord.quality,
            }
        except Exception:
            return None
    
    def _try_parse_scale(self, input_str: str) -> Optional[Dict]:
        """Try to parse input as a scale."""
        import re
        
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
                type_map = {
                    'minor': 'minor_natural',
                    'natural_minor': 'minor_natural',
                    'harmonic_minor': 'minor_harmonic',
                    'melodic_minor': 'minor_melodic',
                    'pentatonic_major': 'pentatonic_major',
                    'pentatonic_minor': 'pentatonic_minor',
                    'blues': 'blues_minor',
                }
                scale_type = type_map.get(scale_type, scale_type)
                
                try:
                    scale = Scale(root_str, scale_type)
                    return {
                        'success': True,
                        'type': 'scale',
                        'scale': scale,
                        'name': scale.name,
                        'notes': scale.note_names,
                        'scale_type': scale.scale_type,
                    }
                except Exception:
                    return None
        
        return None
    
    def _try_parse_progression(self, input_str: str) -> Optional[Dict]:
        """Try to parse input as a chord progression."""
        import re
        
        # Split by common separators
        parts = re.split(r'[\s,\->]+', input_str)
        
        if len(parts) < 2:
            return None
        
        # Try to parse each part as a chord
        chords = []
        for part in parts:
            chord_result = self._try_parse_chord(part.strip())
            if chord_result:
                chords.append(chord_result['chord'])
            else:
                return None  # Not a valid progression
        
        if len(chords) < 2:
            return None
        
        try:
            progression = Progression(chords)
            return {
                'success': True,
                'type': 'progression',
                'progression': progression,
                'chords': [c.name for c in progression.chords],
                'length': len(progression.chords),
            }
        except Exception:
            return None


class OutputFormatter:
    """
    Formats suggestions and results for various output types.
    
    Supports:
    - JSON responses (for API)
    - Human-readable text
    - Visual display data
    """
    
    @staticmethod
    def format_suggestions(suggestions: Dict, output_type: str = 'json') -> Union[Dict, str]:
        """
        Format suggestions for output.
        
        Args:
            suggestions: The suggestions dictionary
            output_type: Format type ('json', 'text', 'visual')
            
        Returns:
            Formatted output
        """
        if output_type == 'json':
            return suggestions
        elif output_type == 'text':
            return OutputFormatter._format_text(suggestions)
        elif output_type == 'visual':
            return OutputFormatter._format_visual(suggestions)
        else:
            return suggestions
    
    @staticmethod
    def _format_text(suggestions: Dict) -> str:
        """Format suggestions as human-readable text."""
        lines = []
        
        if 'scales' in suggestions:
            lines.append("Compatible Scales:")
            for scale in suggestions['scales'][:5]:
                lines.append(f"  - {scale['name']}: {', '.join(scale['notes'])}")
        
        if 'chords' in suggestions:
            lines.append("\nNext Chord Suggestions:")
            for chord in suggestions['chords'][:5]:
                lines.append(f"  - {chord['name']}: {chord.get('function', '')}")
        
        if 'expansion' in suggestions:
            lines.append("\nExpanded Progression:")
            lines.append(f"  {' → '.join(suggestions['expansion'])}")
        
        return '\n'.join(lines) if lines else "No suggestions available"
    
    @staticmethod
    def _format_visual(suggestions: Dict) -> Dict:
        """Format suggestions for visual display."""
        visual_data = {
            'notes': [],
            'positions': [],
            'highlight': [],
        }
        
        if 'scales' in suggestions and suggestions['scales']:
            scale = suggestions['scales'][0]
            visual_data['notes'] = scale.get('notes', [])
            visual_data['highlight'] = scale.get('notes', [])
        
        if 'chords' in suggestions and suggestions['chords']:
            chord = suggestions['chords'][0]
            visual_data['notes'] = chord.get('notes', [])
        
        return visual_data
    
    @staticmethod
    def format_progression_data(progression: Progression, key: str = 'C') -> Dict:
        """Format progression data for display."""
        return {
            'chords': [c.name for c in progression.chords],
            'chord_details': [
                {
                    'name': c.name,
                    'notes': c.note_names,
                    'quality': c.quality,
                }
                for c in progression.chords
            ],
            'roman_numerals': progression.get_roman_numerals(key) if hasattr(progression, 'get_roman_numerals') else [],
        }


class Coordinator:
    """
    Main coordinator that orchestrates all modules.
    
    Coordinates:
    - Input handling
    - Engine processing
    - Suggestion generation
    - Output formatting
    """
    
    def __init__(self):
        self.input_controller = InputController()
        self.output_formatter = OutputFormatter()
        self.harmony_engine = HarmonyEngine()
        self.scale_solver = ScaleSolver(self.harmony_engine)
        self.chord_solver = ChordSolver(self.harmony_engine)
        self.conflict_resolver = ConflictResolver(self.harmony_engine)
        self.genre_detector = GenreDetector()
        self.genre_rules = {
            'jazz': JazzRules(),
            'pop': PopRules(),
            'rock': RockRules(),
            'blues': BluesRules(),
        }
    
    def process(self, input_str: str, context: Optional[Dict] = None) -> Dict:
        """
        Process input and generate comprehensive output.
        
        Args:
            input_str: Input to process
            context: Optional context (genre, key, etc.)
            
        Returns:
            Comprehensive result dictionary
        """
        context = context or {}
        
        # Parse input
        parsed = self.input_controller.parse_input(input_str, context)
        
        if not parsed.get('success'):
            return parsed
        
        # Detect genre if not specified
        genre = context.get('genre') or self.genre_detector.detect_from_input(input_str)
        genre_rules = self.genre_rules.get(genre, JazzRules())  # Default to jazz
        
        result = {
            'input': input_str,
            'type': parsed['type'],
            'genre': genre,
        }
        
        # Process based on type
        if parsed['type'] == 'chord':
            result.update(self._process_chord(parsed, genre_rules))
        elif parsed['type'] == 'scale':
            result.update(self._process_scale(parsed, genre_rules))
        elif parsed['type'] == 'progression':
            result.update(self._process_progression(parsed, genre_rules))
        
        return result
    
    def _process_chord(self, parsed: Dict, genre_rules: GenreRules) -> Dict:
        """Process chord input."""
        chord = parsed['chord']
        
        # Get compatible scales
        compatible = self.harmony_engine.find_compatible_scales(chord)
        
        # Apply genre filter
        filtered_scales = genre_rules.filter_scales(compatible.get('all_scales', []))
        
        # Get next chord suggestions
        next_chords = self.chord_solver.suggest_next_chords(chord)
        genre_chords = genre_rules.filter_chords(next_chords)
        
        # Get scale for improvisation
        improv_scale = self.scale_solver.suggest_improvisation_scale(chord)
        
        return {
            'chord': {
                'name': chord.name,
                'notes': chord.note_names,
                'quality': chord.quality,
            },
            'compatible_scales': filtered_scales[:5],
            'next_chords': genre_chords[:5],
            'improvisation_scale': improv_scale,
            'genre_recommendations': genre_rules.get_chord_recommendations(chord),
        }
    
    def _process_scale(self, parsed: Dict, genre_rules: GenreRules) -> Dict:
        """Process scale input."""
        scale = parsed['scale']
        
        # Get compatible chords
        compatible = self.harmony_engine.find_compatible_chords(scale)
        
        # Apply genre filter
        filtered_chords = genre_rules.filter_chords(compatible)
        
        # Get common progressions using this scale
        progressions = genre_rules.get_progressions_for_scale(scale)
        
        return {
            'scale': {
                'name': scale.name,
                'notes': scale.note_names,
                'type': scale.scale_type,
            },
            'compatible_chords': filtered_chords[:7],
            'common_progressions': progressions,
            'genre_tips': genre_rules.get_scale_tips(scale),
        }
    
    def _process_progression(self, parsed: Dict, genre_rules: GenreRules) -> Dict:
        """Process progression input."""
        progression = parsed['progression']
        
        # Analyze the progression
        analysis = self._analyze_progression(progression)
        
        # Get suggestions for continuation
        continuation = self.chord_solver.suggest_continuation(progression.chords)
        
        # Get expansions
        from .expansion import ProgressionExpander
        expander = ProgressionExpander(self.harmony_engine)
        expansions = expander.expand(progression.chords)
        
        # Filter by genre
        genre_expansions = genre_rules.filter_progressions(expansions)
        
        return {
            'progression': {
                'chords': [c.name for c in progression.chords],
                'length': len(progression.chords),
            },
            'analysis': analysis,
            'continuation': continuation[:3],
            'expansions': genre_expansions[:3],
            'genre_fit': genre_rules.analyze_progression(progression),
        }
    
    def _analyze_progression(self, progression: Progression) -> Dict:
        """Analyze a chord progression."""
        chords = progression.chords
        
        if len(chords) < 2:
            return {'status': 'too_short'}
        
        # Check for common patterns
        chord_names = [c.name for c in chords]
        
        # Detect ii-V-I
        is_ii_v_i = self._check_ii_v_i(chord_names)
        
        # Detect I-IV-V
        is_i_iv_v = self._check_i_iv_v(chord_names)
        
        # Detect 12-bar blues
        is_blues = len(chords) >= 12
        
        # Detect turnaround
        is_turnaround = self._check_turnaround(chord_names)
        
        return {
            'is_ii_v_i': is_ii_v_i,
            'is_i_iv_v': is_i_iv_v,
            'is_blues': is_blues,
            'is_turnaround': is_turnaround,
            'chord_count': len(chords),
        }
    
    def _check_ii_v_i(self, chords: List[str]) -> bool:
        """Check if progression contains ii-V-I pattern."""
        # Simple pattern check (would need key context for accuracy)
        patterns = [
            ['Dm7', 'G7', 'Cmaj7'],
            ['Dm7b5', 'G7b9', 'Cm7'],
            ['Dø', 'G7', 'Cmaj7'],
        ]
        return any(p in ' '.join(chords) for p in [' '.join(x) for x in patterns])
    
    def _check_i_iv_v(self, chords: List[str]) -> bool:
        """Check if progression is I-IV-V."""
        patterns = [
            ['C', 'F', 'G'],
            ['C', 'F', 'G7'],
        ]
        return any(p in ' '.join(chords) for p in [' '.join(x) for x in patterns])
    
    def _check_turnaround(self, chords: List[str]) -> bool:
        """Check if progression contains a turnaround."""
        turnarounds = [
            ['I', 'vi', 'ii', 'V'],
            ['Cmaj7', 'Am7', 'Dm7', 'G7'],
        ]
        return any(t in ' '.join(chords) for t in [' '.join(x) for x in turnarounds])
    
    def suggest_for_context(self, current: str, context: Dict) -> Dict:
        """
        Get suggestions based on current context.
        
        Args:
            current: Current chord or scale
            context: Context including key, genre, etc.
            
        Returns:
            Suggestions dictionary
        """
        genre = context.get('genre', 'jazz')
        key = context.get('key', 'C')
        
        genre_rules = self.genre_rules.get(genre, JazzRules())
        
        # Parse current
        parsed = self.input_controller.parse_input(current)
        
        if not parsed.get('success'):
            return {'error': f'Could not parse: {current}'}
        
        if parsed['type'] == 'chord':
            # Get scale suggestions
            scales = self.scale_solver.suggest_scales_for_chord(parsed['chord'], key)
            filtered = genre_rules.filter_scales(scales)
            
            # Get next chord suggestions
            next_chords = self.chord_solver.suggest_next_chords(parsed['chord'])
            filtered_chords = genre_rules.filter_chords(next_chords)
            
            return {
                'current': current,
                'suggested_scales': filtered[:3],
                'suggested_next_chords': filtered_chords[:3],
            }
        
        elif parsed['type'] == 'scale':
            # Get chord suggestions
            chords = self.chord_solver.suggest_chords_for_scale(parsed['scale'])
            filtered = genre_rules.filter_chords(chords)
            
            # Get progressions
            progressions = genre_rules.get_progressions_for_scale(parsed['scale'])
            
            return {
                'current': current,
                'suggested_chords': filtered[:5],
                'common_progressions': progressions[:3],
            }
        
        return {'error': 'Unknown input type'}


# Convenience function
def create_coordinator() -> Coordinator:
    """Create and return a Coordinator instance."""
    return Coordinator()


def process(input_str: str, context: Optional[Dict] = None) -> Dict:
    """Process input and return coordinated output."""
    coordinator = Coordinator()
    return coordinator.process(input_str, context)

