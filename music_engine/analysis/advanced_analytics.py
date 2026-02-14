"""
Advanced Analytics for Music Theory Engine.

This module provides sophisticated analysis tools for musical progressions,
including tension/release analysis, harmonic complexity metrics, and
circle of fifths relationships.
"""

import math
from typing import List, Dict, Tuple, Optional, Set
from collections import Counter, defaultdict

# Import with proper path handling
import sys
import os

# Ensure parent directory is in path
parent_dir = os.path.dirname(os.path.dirname(__file__))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from models.chord import Chord
from models.note import Note
from models.progression import Progression


class HarmonicAnalyzer:
    """
    Advanced harmonic analysis for chord progressions.

    Provides metrics for:
    - Tension/Release analysis
    - Harmonic complexity
    - Circle of fifths relationships
    - Functional harmony analysis
    - Voice leading efficiency
    """

    # Circle of fifths relationships (semitone distances)
    CIRCLE_OF_FIFTHS = {
        'C': 0, 'G': 7, 'D': 2, 'A': 9, 'E': 4, 'B': 11,
        'F#': 6, 'C#': 1, 'G#': 8, 'D#': 3, 'A#': 10, 'F': 5,
        # Relative minors (3 semitones down)
        'Am': 9, 'Em': 4, 'Bm': 11, 'F#m': 6, 'C#m': 1,
        'G#m': 8, 'D#m': 3, 'A#m': 10, 'Fm': 5, 'Cm': 0,
        'Gm': 7, 'Dm': 2
    }

    # Tension values for different chord functions (0-10 scale)
    CHORD_TENSION = {
        # Tonic function (stable)
        'maj': 1, 'min': 2, 'maj7': 1.5, 'min7': 2.5,

        # Dominant function (tension building)
        'dom7': 6, '7': 6, 'dom9': 7, '9': 7,
        'dom11': 8, '11': 8, 'dom13': 9, '13': 9,

        # Subdominant function (moderate tension)
        'min7b5': 7, 'dim7': 8, 'dim': 5,
        'maj6': 3, 'min6': 4, '6': 3, '6/9': 3.5,

        # Other tensions
        'aug': 8, 'sus2': 4, 'sus4': 4, '7sus4': 7,
        'add9': 4, 'maj9': 3, 'min9': 5, 'min11': 6
    }

    # Roman numeral analysis for major keys
    ROMAN_NUMERALS_MAJOR = {
        0: 'I', 2: 'II', 4: 'III', 5: 'III#', 7: 'IV', 9: 'V', 11: 'VI',
        1: 'bII', 3: 'bIII', 6: 'bV', 8: 'bVI', 10: 'bVII'
    }

    # Roman numeral analysis for minor keys
    ROMAN_NUMERALS_MINOR = {
        0: 'i', 2: 'ii', 3: 'bIII', 5: 'iv', 7: 'v', 8: 'bVI', 10: 'bVII',
        1: 'bii', 4: 'III', 6: 'biv', 9: 'VI', 11: 'VII'
    }

    @staticmethod
    def analyze_progression(progression: Progression) -> Dict:
        """
        Perform comprehensive analysis of a chord progression.

        Args:
            progression: Progression object to analyze

        Returns:
            Dictionary with detailed analysis results
        """
        analysis = {
            'basic_metrics': HarmonicAnalyzer._calculate_basic_metrics(progression),
            'tension_profile': HarmonicAnalyzer._calculate_tension_profile(progression),
            'harmonic_flow': HarmonicAnalyzer._analyze_harmonic_flow(progression),
            'circle_of_fifths': HarmonicAnalyzer._analyze_circle_relationships(progression),
            'functional_analysis': HarmonicAnalyzer._analyze_functional_harmony(progression),
            'complexity_metrics': HarmonicAnalyzer._calculate_complexity_metrics(progression),
            'voice_leading': HarmonicAnalyzer._analyze_voice_leading(progression),
            'patterns': HarmonicAnalyzer._identify_patterns(progression)
        }

        return analysis

    @staticmethod
    def _calculate_basic_metrics(progression: Progression) -> Dict:
        """Calculate basic statistical metrics."""
        chords = progression.chords
        if not chords:
            return {}

        # Chord count and distribution
        qualities = [chord.quality for chord in chords]
        quality_counts = Counter(qualities)

        # Root notes distribution
        root_notes = [chord.root.name[0] for chord in chords]  # Just the letter
        root_counts = Counter(root_notes)

        # Interval analysis
        all_intervals = []
        for chord in chords:
            for note in chord.notes:
                all_intervals.append(note.semitone % 12)
        interval_counts = Counter(all_intervals)

        return {
            'chord_count': len(chords),
            'unique_qualities': len(quality_counts),
            'quality_distribution': dict(quality_counts),
            'unique_roots': len(root_counts),
            'root_distribution': dict(root_counts),
            'pitch_class_distribution': dict(interval_counts),
            'average_notes_per_chord': sum(len(c.notes) for c in chords) / len(chords)
        }

    @staticmethod
    def _calculate_tension_profile(progression: Progression) -> Dict:
        """Calculate tension/release profile of the progression."""
        chords = progression.chords
        if not chords:
            return {}

        tensions = []
        releases = []

        for i, chord in enumerate(chords):
            # Calculate chord tension
            tension = HarmonicAnalyzer.CHORD_TENSION.get(chord.quality, 5)
            tensions.append(tension)

            # Calculate release (based on position and context)
            release = HarmonicAnalyzer._calculate_release_factor(chord, i, chords)
            releases.append(release)

        # Calculate tension curve
        tension_curve = []
        for i in range(len(tensions)):
            if i == 0:
                curve = tensions[i]
            else:
                # Tension builds or releases based on harmonic movement
                movement = HarmonicAnalyzer._calculate_harmonic_movement(chords[i-1], chords[i])
                curve = tensions[i] + movement
            tension_curve.append(min(10, max(0, curve)))

        return {
            'chord_tensions': tensions,
            'tension_curve': tension_curve,
            'average_tension': sum(tensions) / len(tensions),
            'tension_variance': HarmonicAnalyzer._calculate_variance(tensions),
            'peak_tension': max(tensions),
            'tension_range': max(tensions) - min(tensions),
            'releases': releases
        }

    @staticmethod
    def _calculate_release_factor(chord: Chord, position: int, all_chords: List[Chord]) -> float:
        """Calculate release factor for a chord in context."""
        # Tonic chords provide more release
        if chord.quality in ['maj', 'min', 'maj7', 'min7']:
            root_semitone = chord.root.semitone % 12
            # C, F, G, Am, Em, Dm provide more release
            tonic_roots = [0, 5, 7, 9, 4, 2]  # C, F, G, A, E, D
            if root_semitone in tonic_roots:
                return 0.8
        return 0.3

    @staticmethod
    def _calculate_harmonic_movement(chord1: Chord, chord2: Chord) -> float:
        """Calculate tension change between two chords."""
        # Root movement analysis
        root1 = chord1.root.semitone % 12
        root2 = chord2.root.semitone % 12

        # Perfect fifth movement (most stable)
        if abs(root2 - root1) == 7 or abs(root2 - root1) == 5:
            return -1.0  # Release

        # Tritone movement (creates tension)
        if abs(root2 - root1) == 6:
            return 1.5  # Tension build

        # Same root (repetition)
        if root1 == root2:
            return -0.5  # Slight release

        # Other movements
        return 0.0

    @staticmethod
    def _analyze_harmonic_flow(progression: Progression) -> Dict:
        """Analyze the overall harmonic flow of the progression."""
        chords = progression.chords
        if not chords:
            return {}

        # Movement patterns
        movements = []
        for i in range(1, len(chords)):
            movement = HarmonicAnalyzer._calculate_harmonic_movement(chords[i-1], chords[i])
            movements.append(movement)

        # Flow characteristics
        flow_score = sum(movements) / len(movements) if movements else 0

        # Predictability analysis
        predictable_moves = sum(1 for m in movements if abs(m) < 0.5)
        unpredictable_moves = len(movements) - predictable_moves

        return {
            'harmonic_movements': movements,
            'flow_score': flow_score,
            'flow_description': HarmonicAnalyzer._describe_flow(flow_score),
            'predictable_moves': predictable_moves,
            'unpredictable_moves': unpredictable_moves,
            'flow_consistency': HarmonicAnalyzer._calculate_variance(movements) if movements else 0
        }

    @staticmethod
    def _describe_flow(flow_score: float) -> str:
        """Describe harmonic flow based on score."""
        if flow_score < -0.5:
            return "Very stable - mostly stepwise or fifth movements"
        elif flow_score < 0:
            return "Stable - good balance of tension and release"
        elif flow_score < 0.5:
            return "Moderate tension - balanced harmonic movement"
        elif flow_score < 1.0:
            return "Tense - significant harmonic movement"
        else:
            return "Very tense - complex harmonic relationships"

    @staticmethod
    def _analyze_circle_relationships(progression: Progression) -> Dict:
        """Analyze relationships within the circle of fifths."""
        chords = progression.chords
        if not chords:
            return {}

        # Calculate positions on circle of fifths
        positions = []
        for chord in chords:
            root_name = chord.root.name
            # Handle different octaves
            root_letter = root_name[0]
            if len(root_name) > 1 and root_name[1] in ['#', 'b']:
                root_key = root_name[:2]
            else:
                root_key = root_name[0]

            # Add quality for minor chords
            if chord.quality.startswith('min'):
                root_key += 'm'

            position = HarmonicAnalyzer.CIRCLE_OF_FIFTHS.get(root_key, -1)
            positions.append(position)

        # Calculate movement distances
        distances = []
        for i in range(1, len(positions)):
            if positions[i-1] != -1 and positions[i] != -1:
                # Calculate shortest distance on circle (max 6 steps)
                dist = abs(positions[i] - positions[i-1])
                dist = min(dist, 12 - dist)  # Circle distance
                distances.append(dist)

        # Circle efficiency
        close_movements = sum(1 for d in distances if d <= 2)
        far_movements = sum(1 for d in distances if d > 4)

        return {
            'circle_positions': positions,
            'movement_distances': distances,
            'close_movements': close_movements,
            'far_movements': far_movements,
            'circle_efficiency': close_movements / len(distances) if distances else 0,
            'average_distance': sum(distances) / len(distances) if distances else 0
        }

    @staticmethod
    def _analyze_functional_harmony(progression: Progression) -> Dict:
        """Analyze functional harmony (tonic, dominant, subdominant)."""
        chords = progression.chords
        if not chords:
            return {}

        # Detect key (simplified - use first chord)
        key_root = chords[0].root
        is_minor = chords[0].quality.startswith('min')

        # Assign functions
        functions = []
        roman_numerals = []

        numerals = (HarmonicAnalyzer.ROMAN_NUMERALS_MINOR if is_minor
                   else HarmonicAnalyzer.ROMAN_NUMERALS_MAJOR)

        for chord in chords:
            root_semitone = chord.root.semitone % 12
            key_semitone = key_root.semitone % 12

            # Calculate interval from key
            interval = (root_semitone - key_semitone) % 12

            roman_numeral = numerals.get(interval, '?')
            roman_numerals.append(roman_numeral)

            # Determine function
            if roman_numeral in ['I', 'i', 'III', 'iii', 'VI', 'vi']:
                function = 'T'  # Tonic
            elif roman_numeral in ['V', 'v', 'VII', 'vii']:
                function = 'D'  # Dominant
            elif roman_numeral in ['IV', 'iv', 'II', 'ii']:
                function = 'S'  # Subdominant
            else:
                function = 'O'  # Other

            functions.append(function)

        # Function distribution
        function_counts = Counter(functions)

        return {
            'detected_key': key_root.name,
            'is_minor': is_minor,
            'roman_numerals': roman_numerals,
            'functions': functions,
            'function_distribution': dict(function_counts),
            'functional_balance': HarmonicAnalyzer._calculate_functional_balance(function_counts)
        }

    @staticmethod
    def _calculate_functional_balance(function_counts: Counter) -> float:
        """Calculate how well-balanced the functional harmony is."""
        total = sum(function_counts.values())
        if total == 0:
            return 0

        # Ideal balance: 40% T, 30% D, 20% S, 10% O
        ideal = {'T': 0.4, 'D': 0.3, 'S': 0.2, 'O': 0.1}

        balance_score = 0
        for func, ideal_prop in ideal.items():
            actual_prop = function_counts.get(func, 0) / total
            balance_score += 1 - abs(actual_prop - ideal_prop)

        return balance_score / len(ideal)

    @staticmethod
    def _calculate_complexity_metrics(progression: Progression) -> Dict:
        """Calculate various complexity metrics."""
        chords = progression.chords
        if not chords:
            return {}

        # Note density
        all_notes = set()
        for chord in chords:
            all_notes.update(note.semitone % 12 for note in chord.notes)
        note_density = len(all_notes) / 12  # Proportion of chromatic scale used

        # Chord variety
        qualities = set(chord.quality for chord in chords)
        chord_variety = len(qualities) / len(HarmonicAnalyzer.CHORD_TENSION)

        # Rhythmic complexity (assuming equal duration for now)
        # This could be extended with actual rhythm analysis
        rhythmic_complexity = 0.5  # Placeholder

        # Overall complexity score
        complexity_score = (note_density * 0.4 +
                          chord_variety * 0.4 +
                          rhythmic_complexity * 0.2)

        return {
            'note_density': note_density,
            'chord_variety': chord_variety,
            'rhythmic_complexity': rhythmic_complexity,
            'overall_complexity': complexity_score,
            'complexity_description': HarmonicAnalyzer._describe_complexity(complexity_score)
        }

    @staticmethod
    def _describe_complexity(score: float) -> str:
        """Describe complexity level."""
        if score < 0.3:
            return "Very simple - basic harmonic vocabulary"
        elif score < 0.5:
            return "Simple - standard chord progressions"
        elif score < 0.7:
            return "Moderate - some harmonic variety"
        elif score < 0.85:
            return "Complex - advanced harmonic techniques"
        else:
            return "Very complex - sophisticated harmonic language"

    @staticmethod
    def _analyze_voice_leading(progression: Progression) -> Dict:
        """Analyze voice leading efficiency."""
        chords = progression.chords
        if len(chords) < 2:
            return {}

        # Simple voice leading analysis (could be much more sophisticated)
        total_movement = 0
        smooth_transitions = 0

        for i in range(1, len(chords)):
            chord1_notes = [n.semitone % 12 for n in chords[i-1].notes]
            chord2_notes = [n.semitone % 12 for n in chords[i].notes]

            # Calculate minimum movement between chords
            min_movement = float('inf')
            for note1 in chord1_notes:
                for note2 in chord2_notes:
                    movement = min(abs(note2 - note1), 12 - abs(note2 - note1))
                    min_movement = min(min_movement, movement)

            total_movement += min_movement

            # Count smooth transitions (movement ≤ 2 semitones)
            if min_movement <= 2:
                smooth_transitions += 1

        avg_movement = total_movement / (len(chords) - 1)
        smoothness = smooth_transitions / (len(chords) - 1)

        return {
            'average_movement': avg_movement,
            'smooth_transitions': smooth_transitions,
            'total_transitions': len(chords) - 1,
            'smoothness_score': smoothness,
            'voice_leading_efficiency': 1 - (avg_movement / 6)  # 6 semitones = tritone
        }

    @staticmethod
    def _identify_patterns(progression: Progression) -> Dict:
        """Identify common progression patterns."""
        chords = progression.chords
        if len(chords) < 3:
            return {'patterns': [], 'description': 'Too short for pattern analysis'}

        patterns = []

        # Check for common cadences
        if len(chords) >= 2:
            last_two = [chord.quality for chord in chords[-2:]]
            if last_two == ['dom7', 'maj'] or last_two == ['7', 'maj']:
                patterns.append('Authentic Cadence (V-I)')

            if last_two == ['maj7', 'maj'] or last_two == ['7', 'maj']:
                patterns.append('Perfect Authentic Cadence (V7-I)')

        # Check for circle of fifths movement
        roots = [chord.root.semitone % 12 for chord in chords]
        cof_movements = []
        for i in range(1, len(roots)):
            dist = abs(roots[i] - roots[i-1])
            dist = min(dist, 12 - dist)  # Circle distance
            cof_movements.append(dist)

        circle_ratio = sum(1 for d in cof_movements if d == 5 or d == 7) / len(cof_movements)
        if circle_ratio > 0.6:
            patterns.append('Circle of Fifths Movement')

        # Check for repetitive patterns
        if len(chords) >= 4:
            # Look for repeating 2-chord patterns
            for i in range(len(chords) - 3):
                pair1 = (chords[i].root.semitone % 12, chords[i].quality)
                pair2 = (chords[i+2].root.semitone % 12, chords[i+2].quality)
                if pair1 == pair2:
                    patterns.append('Repetitive Structure')
                    break

        return {
            'patterns': patterns,
            'pattern_count': len(patterns),
            'description': '; '.join(patterns) if patterns else 'No common patterns detected'
        }

    @staticmethod
    def _calculate_variance(values: List[float]) -> float:
        """Calculate variance of a list of values."""
        if not values:
            return 0

        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        return variance