"""
Genre Rules Module

Provides genre-specific rules for chord/scale suggestions and adaptations.
Includes Jazz, Pop, Rock, and Blues rules.
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


class GenreRules:
    """
    Base class for genre-specific rules.
    
    Subclasses should implement:
    - preferred_scales: List of preferred scale types
    - preferred_chords: List of preferred chord qualities
    - common_progressions: Common chord progressions
    """
    
    def __init__(self):
        self.preferred_scales = []
        self.preferred_chords = []
        self.common_progressions = []
        self.name = "generic"
    
    def filter_scales(self, scales: List[Dict]) -> List[Dict]:
        """Filter scales based on genre preferences."""
        if not self.preferred_scales:
            return scales
        
        filtered = []
        for scale in scales:
            scale_type = scale.get('type', '')
            if scale_type in self.preferred_scales:
                # Boost priority for preferred scales
                scale_copy = scale.copy()
                scale_copy['priority'] = 1
                filtered.append(scale_copy)
        
        # Add remaining scales with lower priority
        for scale in scales:
            scale_type = scale.get('type', '')
            if scale_type not in self.preferred_scales:
                scale_copy = scale.copy()
                scale_copy['priority'] = 0
                filtered.append(scale_copy)
        
        # Sort by priority
        filtered.sort(key=lambda x: x.get('priority', 0), reverse=True)
        
        return filtered
    
    def filter_chords(self, chords: List[Dict]) -> List[Dict]:
        """Filter chords based on genre preferences."""
        if not self.preferred_chords:
            return chords
        
        filtered = []
        for chord in chords:
            quality = chord.get('quality', '')
            if quality in self.preferred_chords:
                chord_copy = chord.copy()
                chord_copy['priority'] = 1
                filtered.append(chord_copy)
        
        # Add remaining chords
        for chord in chords:
            quality = chord.get('quality', '')
            if quality not in self.preferred_chords:
                chord_copy = chord.copy()
                chord_copy['priority'] = 0
                filtered.append(chord_copy)
        
        filtered.sort(key=lambda x: x.get('priority', 0), reverse=True)
        
        return filtered
    
    def filter_progressions(self, progressions: List[List[str]]) -> List[List[str]]:
        """Filter progressions based on genre preferences."""
        return progressions
    
    def get_progressions_for_scale(self, scale: Scale) -> List[str]:
        """Get common progressions for a scale."""
        return self.common_progressions[:5] if self.common_progressions else []
    
    def get_scale_tips(self, scale: Scale) -> List[str]:
        """Get genre-specific tips for playing a scale."""
        return []
    
    def get_chord_recommendations(self, chord: Chord) -> Dict:
        """Get genre-specific recommendations for a chord."""
        return {}
    
    def analyze_progression(self, progression: Progression) -> Dict:
        """Analyze how well a progression fits the genre."""
        return {
            'fit_score': 50,
            'notes': 'Standard progression',
        }


class JazzRules(GenreRules):
    """
    Jazz-specific rules and preferences.
    
    Jazz characteristics:
    - Extended chords (7th, 9th, 11th, 13th)
    - Complex chord substitutions
    - ii-V-I progressions
    - Modal interchange
    - Bebop scales
    """
    
    def __init__(self):
        super().__init__()
        self.name = "jazz"
        
        # Preferred scales for jazz
        self.preferred_scales = [
            'major',
            'dorian',
            'mixolydian',
            'lydian',
            'minor_natural',
            'minor_melodic',
            'pentatonic_major',
            'pentatonic_minor',
            'blues_minor',
        ]
        
        # Preferred chord qualities
        self.preferred_chords = [
            'maj7',
            'min7',
            'dom7',
            'min7b5',
            'dim7',
            'maj9',
            'min9',
            'dom9',
            'dom13',
        ]
        
        # Common jazz progressions
        self.common_progressions = [
            'Cmaj7 → Dm7 → G7 → Cmaj7',
            'Dm7 → G7 → Cmaj7',
            'Dm7b5 → G7b9 → Cm7',
            'Cmaj7 → Am7 → Dm7 → G7',
            'Fmaj7 → Bdim → Em7 → A7 → Dm7 → G7',
        ]
    
    def get_scale_tips(self, scale: Scale) -> List[str]:
        """Get jazz-specific scale tips."""
        scale_type = scale.scale_type
        
        tips = {
            'major': [
                "Use the major scale over major 7th chords",
                "Try Lydian (#11) for more tension over maj7 chords",
                "Use enclosures and approach patterns",
            ],
            'dorian': [
                "Perfect for minor 7th chords",
                "Practice ii-V-I in minor keys",
                "Use the b9, #9, and #11 as color tones",
            ],
            'mixolydian': [
                "Standard choice for dominant 7th chords",
                "Try altered extensions (b9, #9, #11, b13)",
                "Practice tritone substitutions",
            ],
            'lydian': [
                "Use over major 7th chords for a dreamy sound",
                "The #11 creates tension wanting to resolve",
                "Great for ballads and chill vibes",
            ],
            'minor_natural': [
                "Use for minor 7th chords",
                "Practice relative major/minor movements",
                "Try modal interchange with harmonic minor",
            ],
        }
        
        return tips.get(scale_type, ["Practice improvisation over this scale"])
    
    def get_chord_recommendations(self, chord: Chord) -> Dict:
        """Get jazz-specific chord recommendations."""
        quality = chord.quality
        
        recommendations = {
            'maj7': [
                "Try extending to maj9 or maj13",
                "Consider Lydian mode for more color",
                "Experiment with sus4 voicings",
            ],
            'min7': [
                "Practice Dorian mode over this chord",
                "Try adding the 9th or 11th",
                "Consider minor 6th chords as alternatives",
            ],
            'dom7': [
                "Use Mixolydian or altered scale",
                "Try tritone substitution",
                "Add b9, #9, #11, or b13 extensions",
            ],
            'min7b5': [
                "Use Locrian or half-diminished scale",
                "Practice over m7b5 chords in minor keys",
            ],
        }
        
        return {
            'extensions': recommendations.get(quality, []),
            'substitutions': ['Tritone substitute', 'Diminished substitute'],
            'voice_leading': 'Aim for smooth voice leading',
        }
    
    def analyze_progression(self, progression: Progression) -> Dict:
        """Analyze how well a progression fits jazz."""
        chords = [c.name for c in progression.chords]
        chord_str = ' '.join(chords)
        
        score = 50
        notes = []
        
        # Check for ii-V-I
        if 'Dm7' in chord_str and 'G7' in chord_str:
            score += 20
            notes.append("Classic ii-V-I pattern")
        
        # Check for turnarounds
        if any(t in chord_str for t in ['Cmaj7 → Am7', 'Dm7 → G7']):
            score += 15
            notes.append("Jazz turnaround detected")
        
        # Check for extended chords
        if any('7' in c or '9' in c for c in chords):
            score += 10
            notes.append("Good use of extended harmonies")
        
        return {
            'fit_score': min(100, score),
            'notes': notes,
            'suggestions': ['Try adding more ii-V sequences', 'Consider tritone substitutions'],
        }


class PopRules(GenreRules):
    """
    Pop music-specific rules and preferences.
    
    Pop characteristics:
    - Simple chord progressions
    - Major keys
    - I-V-vi-IV progression
    - Power chords in rock-influenced pop
    """
    
    def __init__(self):
        super().__init__()
        self.name = "pop"
        
        # Preferred scales
        self.preferred_scales = [
            'major',
            'minor_natural',
            'pentatonic_major',
            'pentatonic_minor',
        ]
        
        # Preferred chords
        self.preferred_chords = [
            'maj',
            'min',
            'dom7',
            'maj7',
            'min7',
        ]
        
        # Common pop progressions
        self.common_progressions = [
            'C → G → Am → F',
            'C → F → G → C',
            'Am → F → C → G',
            'C → Am → F → G',
            'I → V → vi → IV',
        ]
    
    def get_scale_tips(self, scale: Scale) -> List[str]:
        """Get pop-specific scale tips."""
        return [
            "Keep it simple - stick to scale notes",
            "Focus on melody over complex lines",
            "Use pentatonic scales for easier melodies",
        ]
    
    def get_chord_recommendations(self, chord: Chord) -> Dict:
        """Get pop-specific chord recommendations."""
        return {
            'simplify': 'Stick to triads or simple 7ths',
            'voicings': 'Use root position voicings',
            'movement': 'Prefer root movement by 4th or 5th',
        }
    
    def analyze_progression(self, progression: Progression) -> Dict:
        """Analyze how well a progression fits pop."""
        chords = [c.name for c in progression.chords]
        
        score = 50
        notes = []
        
        # Check for I-V-vi-IV
        if len(chords) >= 4:
            score += 25
            notes.append("Classic pop progression (I-V-vi-IV)")
        
        # Check for simple progressions
        if len(chords) <= 4:
            score += 15
            notes.append("Short, memorable progression")
        
        return {
            'fit_score': min(100, score),
            'notes': notes,
            'suggestions': ['Great for songwriting', 'Try adding a pre-chorus'],
        }


class RockRules(GenreRules):
    """
    Rock music-specific rules and preferences.
    
    Rock characteristics:
    - Power chords
    - Minor keys
    - Pentatonic scales
    - Blue notes
    """
    
    def __init__(self):
        super().__init__()
        self.name = "rock"
        
        # Preferred scales
        self.preferred_scales = [
            'minor_natural',
            'pentatonic_minor',
            'pentatonic_major',
            'blues_minor',
            'mixolydian',
        ]
        
        # Preferred chords
        self.preferred_chords = [
            'maj',
            'min',
            'dom7',
            '5',  # Power chord
            'sus4',
        ]
        
        # Common rock progressions
        self.common_progressions = [
            'E → A → B → E',
            'Am → G → F → E',
            'Cm → Ab → G',
            'i → VII → VI → V',
            'Power chord riff patterns',
        ]
    
    def get_scale_tips(self, scale: Scale) -> List[str]:
        """Get rock-specific scale tips."""
        scale_type = scale.scale_type
        
        tips = {
            'pentatonic_minor': [
                "The go-to scale for rock guitar",
                "Use blue notes for that rock edge",
                "Practice bending and vibrato",
            ],
            'blues_minor': [
                "Classic blues rock sound",
                "Try the blue note (b5) for tension",
                "Great for soloing",
            ],
            'mixolydian': [
                "Use for dominant 7th chords in rock",
                "Perfect for hard rock and metal",
                "Try the b7 for a darker feel",
            ],
        }
        
        return tips.get(scale_type, ["Practice power chords and palm muting"])
    
    def get_chord_recommendations(self, chord: Chord) -> Dict:
        """Get rock-specific chord recommendations."""
        return {
            'voicings': 'Try power chords for distortion',
            'effects': 'Use overdrive and distortion',
            'movement': 'Use chromatic runs between chords',
        }
    
    def analyze_progression(self, progression: Progression) -> Dict:
        """Analyze how well a progression fits rock."""
        chords = [c.name for c in progression.chords]
        
        score = 50
        notes = []
        
        # Check for power chord compatible
        if any(c.endswith('5') or c.endswith('sus4') for c in chords):
            score += 20
            notes.append("Power chord compatible")
        
        # Check for minor key
        if any('m' in c and 'm7' not in c for c in chords):
            score += 15
            notes.append("Minor key rock progression")
        
        return {
            'fit_score': min(100, score),
            'notes': notes,
            'suggestions': ['Add distortion', 'Try power chords'],
        }


class BluesRules(GenreRules):
    """
    Blues music-specific rules and preferences.
    
    Blues characteristics:
    - 12-bar blues structure
    - Dominant 7th chords
    - Blues scale
    - Pentatonic minor
    """
    
    def __init__(self):
        super().__init__()
        self.name = "blues"
        
        # Preferred scales
        self.preferred_scales = [
            'pentatonic_minor',
            'blues_minor',
            'minor_natural',
            'mixolydian',
        ]
        
        # Preferred chords
        self.preferred_chords = [
            'dom7',
            'maj7',
            'min7',
        ]
        
        # Common blues progressions
        self.common_progressions = [
            '12-bar blues: I7 → IV7 → I7 → V7 → IV7 → I7',
            'Quick change blues',
            'Minor blues',
            'Jazz blues',
        ]
    
    def get_scale_tips(self, scale: Scale) -> List[str]:
        """Get blues-specific scale tips."""
        return [
            "Use the blue note (b5) for authentic blues",
            "Practice call and response",
            "Try bending the b3rd and b7th",
            "Use the pentatonic minor scale",
        ]
    
    def get_chord_recommendations(self, chord: Chord) -> Dict:
        """Get blues-specific chord recommendations."""
        return {
            'voicings': 'Use dominant 7th chords',
            'movement': 'Try the shuffle rhythm pattern',
            'turnarounds': 'Learn classic 12-bar blues endings',
        }
    
    def analyze_progression(self, progression: Progression) -> Dict:
        """Analyze how well a progression fits blues."""
        chords = [c.name for c in progression.chords]
        
        score = 50
        notes = []
        
        # Check for 12-bar structure
        if len(chords) >= 12:
            score += 30
            notes.append("12-bar blues structure detected")
        
        # Check for dominant 7th
        if all('7' in c for c in chords):
            score += 15
            notes.append("All dominant 7th - classic blues")
        
        return {
            'fit_score': min(100, score),
            'notes': notes,
            'suggestions': ['Practice shuffle patterns', 'Learn blues turnarounds'],
        }


class GenreDetector:
    """
    Detects the genre from input or context.
    
    Uses heuristics based on:
    - Chord qualities
    - Scale types
    - Progression patterns
    """
    
    # Genre keywords for detection
    GENRE_KEYWORDS = {
        'jazz': ['jazz', 'bebop', 'swing', 'cool', 'fusion', 'modal'],
        'pop': ['pop', 'commercial', 'mainstream', 'singer-songwriter'],
        'rock': ['rock', 'metal', 'punk', 'grunge', 'alternative'],
        'blues': ['blues', 'rhythm and blues', 'r&b', 'blue'],
    }
    
    # Chord patterns for genre detection
    GENRE_PATTERNS = {
        'jazz': ['maj7', 'min7', 'dom7', 'm7b5', 'dim7'],
        'pop': ['maj', 'min', 'sus4'],
        'rock': ['5', 'sus4', 'power'],
        'blues': ['7', 'dom7'],
    }
    
    def detect_from_input(self, input_str: str) -> str:
        """
        Detect genre from input string.
        
        Args:
            input_str: Input string (could contain genre hints)
            
        Returns:
            Detected genre or 'jazz' as default
        """
        input_lower = input_str.lower()
        
        # Check keywords
        for genre, keywords in self.GENRE_KEYWORDS.items():
            for keyword in keywords:
                if keyword in input_lower:
                    return genre
        
        # Check chord patterns
        for genre, patterns in self.GENRE_PATTERNS.items():
            for pattern in patterns:
                if pattern in input_str:
                    return genre
        
        # Default to jazz (most versatile)
        return 'jazz'
    
    def detect_from_progression(self, progression: Progression) -> str:
        """
        Detect genre from a chord progression.
        
        Args:
            progression: Chord progression
            
        Returns:
            Detected genre
        """
        chords = [c.name for c in progression.chords]
        chord_str = ' '.join(chords)
        
        # Check for blues
        if len(chords) >= 12:
            return 'blues'
        
        # Check for rock/pop (simple triads)
        if all('7' not in c for c in chords):
            return 'pop'
        
        # Check for jazz (extended chords)
        if any(p in chord_str for p in ['maj7', 'min7', 'm7b5']):
            return 'jazz'
        
        # Default
        return 'pop'


# Convenience functions
def get_genre_rules(genre: str) -> GenreRules:
    """Get genre rules for a specific genre."""
    rules_map = {
        'jazz': JazzRules,
        'pop': PopRules,
        'rock': RockRules,
        'blues': BluesRules,
    }
    
    return rules_map.get(genre, JazzRules)()


def detect_genre(input_str: str) -> str:
    """Detect genre from input string."""
    detector = GenreDetector()
    return detector.detect_from_input(input_str)

