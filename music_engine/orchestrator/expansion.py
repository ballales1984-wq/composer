"""
Expansion Module

Provides progression expansion, continuation generation, and chord substitution.
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


class ProgressionExpander:
    """
    Expands short progressions into longer ones.
    
    Provides methods for:
    - Expanding 2-3 chord progressions
    - Adding passing chords
    - Creating variations
    """
    
    def __init__(self, harmony_engine: HarmonyEngine):
        self.harmony_engine = harmony_engine
    
    def expand(self, chords: List[Chord], target_length: int = 8) -> List[List[str]]:
        """
        Expand a short progression to a longer one.
        
        Args:
            chords: Starting chords
            target_length: Target number of chords
            
        Returns:
            List of possible expanded progressions
        """
        if len(chords) < 2:
            return [[c.name for c in chords]]
        
        results = []
        
        # Method 1: Add ii-V-I before dominant chords
        results.extend(self._expand_with_ii_v_i(chords))
        
        # Method 2: Add passing chords
        results.extend(self._expand_with_passing_chords(chords))
        
        # Method 3: Add tritone substitutes
        results.extend(self._expand_with_tritone_substitutes(chords))
        
        # Method 4: Add modal interchanges
        results.extend(self._expand_with_modal_interchange(chords))
        
        # Filter to target length
        filtered = []
        for prog in results:
            if len(prog) <= target_length:
                filtered.append(prog)
            else:
                filtered.append(prog[:target_length])
        
        return filtered[:10]  # Return top 10
    
    def _expand_with_ii_v_i(self, chords: List[Chord]) -> List[List[str]]:
        """Add ii-V-I sequences before dominant chords."""
        results = []
        
        for i, chord in enumerate(chords):
            if '7' in chord.quality and 'min' not in chord.quality:
                # This is a dominant chord, add ii-V before it
                expanded = []
                
                # Add all chords before this one
                for c in chords[:i]:
                    expanded.append(c.name)
                
                # Try to add ii-V
                try:
                    # Get the root of the dominant chord
                    root = chord.root
                    
                    # ii is a minor 2nd above the root of V
                    ii_root = root.transpose(-10)  # Whole step down from V
                    ii = Chord(ii_root.name, 'min7')
                    
                    # V is the original chord
                    v = chord
                    
                    expanded.append(ii.name)
                    expanded.append(v.name)
                    
                    # Add remaining chords
                    for c in chords[i+1:]:
                        expanded.append(c.name)
                    
                    if len(expanded) > len(chords):
                        results.append(expanded)
                except:
                    pass
        
        return results
    
    def _expand_with_passing_chords(self, chords: List[Chord]) -> List[List[str]]:
        """Add passing chords between chords."""
        results = []
        
        for i in range(len(chords) - 1):
            from_chord = chords[i]
            to_chord = chords[i + 1]
            
            # Try to find a passing chord
            passing = self._find_passing_chord(from_chord, to_chord)
            
            if passing:
                expanded = [c.name for c in chords]
                # Insert after from_chord, before to_chord
                expanded.insert(i + 1, passing.name)
                results.append(expanded)
        
        return results
    
    def _find_passing_chord(self, from_chord: Chord, to_chord: Chord) -> Optional[Chord]:
        """Find a passing chord between two chords."""
        from_semitone = from_chord.root.semitone
        to_semitone = to_chord.root.semitone
        
        # Calculate distance
        distance = (to_semitone - from_semitone) % 12
        
        # If there's a gap of 2 or more semitones, add passing chord
        if distance >= 2:
            passing_semitone = (from_semitone + distance // 2) % 12
            
            # Find note name
            notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
            passing_note = notes[passing_semitone]
            
            try:
                return Chord(passing_note, 'min')
            except:
                return None
        
        return None
    
    def _expand_with_tritone_substitutes(self, chords: List[Chord]) -> List[List[str]]:
        """Add tritone substitutes for dominant chords."""
        results = []
        
        for i, chord in enumerate(chords):
            if '7' in chord.quality and 'min' not in chord.quality:
                # This is a dominant chord, add tritone substitute
                expanded = []
                
                # Add all chords before this one
                for c in chords[:i]:
                    expanded.append(c.name)
                
                # Add tritone substitute
                try:
                    sub_root = chord.root.transpose(6)  # Tritone up
                    sub_chord = Chord(sub_root.name, 'min7')  # Usually minor 7
                    expanded.append(sub_chord.name)
                    expanded.append(chord.name)
                except:
                    expanded.append(chord.name)
                
                # Add remaining chords
                for c in chords[i+1:]:
                    expanded.append(c.name)
                
                if len(expanded) > len(chords):
                    results.append(expanded)
        
        return results
    
    def _expand_with_modal_interchange(self, chords: List[Chord]) -> List[List[str]]:
        """Add modal interchange chords."""
        results = []
        
        # Try borrowing from parallel minor/major
        for i, chord in enumerate(chords):
            if chord.quality == 'maj':
                # Borrow from parallel minor
                try:
                    minor_chord = Chord(chord.root.name, 'min7')
                    expanded = [c.name for c in chords]
                    expanded.insert(i + 1, minor_chord.name)
                    results.append(expanded)
                except:
                    pass
            elif 'min' in chord.quality:
                # Borrow from parallel major
                try:
                    major_chord = Chord(chord.root.name, 'maj7')
                    expanded = [c.name for c in chords]
                    expanded.insert(i + 1, major_chord.name)
                    results.append(expanded)
                except:
                    pass
        
        return results


class ContinuationGenerator:
    """
    Generates continuations for chord progressions.
    
    Provides methods for:
    - Generating next chords
    - Suggesting endings
    - Creating variations
    """
    
    def __init__(self, harmony_engine: HarmonyEngine):
        self.harmony_engine = harmony_engine
    
    def generate_continuations(self, chords: List[Chord], num_chords: int = 4) -> List[List[str]]:
        """
        Generate possible continuations for a progression.
        
        Args:
            chords: Current progression
            num_chords: Number of chords to generate
            
        Returns:
            List of possible continuations
        """
        if not chords:
            return []
        
        last_chord = chords[-1]
        results = []
        
        # Get compatible chords
        from .solver import ChordSolver
        solver = ChordSolver(self.harmony_engine)
        
        next_chords = solver.suggest_next_chords(last_chord)
        
        for next_chord in next_chords[:5]:
            try:
                next_obj = Chord(next_chord['name'].replace('maj7', 'maj').replace('min7', 'min').replace('dom7', '7')[:2], 
                                next_chord.get('quality', 'maj'))
                
                continuation = [c.name for c in chords]
                continuation.append(next_obj.name)
                
                # Recursively add more chords
                if num_chords > 1:
                    more = self._extend_continuation(continuation, num_chords - 1)
                    results.extend(more)
                else:
                    results.append(continuation)
            except:
                pass
        
        return results
    
    def _extend_continuation(self, current: List[str], remaining: int) -> List[List[str]]:
        """Extend a continuation with more chords."""
        if remaining <= 0:
            return [current]
        
        results = []
        
        try:
            last = Chord(current[-1].replace('maj7', 'maj').replace('min7', 'min').replace('dom7', '7')[:2], 'maj')
            
            from .solver import ChordSolver
            solver = ChordSolver(self.harmony_engine)
            next_chords = solver.suggest_next_chords(last)
            
            for next_chord in next_chords[:3]:
                try:
                    next_obj = Chord(next_chord['name'].replace('maj7', 'maj').replace('min7', 'min').replace('dom7', '7')[:2],
                                    next_chord.get('quality', 'maj'))
                    
                    extended = current + [next_obj.name]
                    further = self._extend_continuation(extended, remaining - 1)
                    results.extend(further)
                except:
                    pass
        except:
            pass
        
        return results
    
    def suggest_endings(self, chords: List[Chord]) -> List[Dict]:
        """
        Suggest appropriate endings for a progression.
        
        Args:
            chords: Current progression
            
        Returns:
            List of ending suggestions
        """
        if not chords:
            return []
        
        suggestions = []
        
        # Get the last chord
        last = chords[-1]
        
        # Common jazz endings
        if last.quality == 'dom7':
            # Authentic cadence
            try:
                tonic = last.root.transpose(-5)
                suggestions.append({
                    'chord': f"{tonic.name}maj7",
                    'type': 'authentic_cadence',
                    'description': 'Resolve to tonic major 7th',
                })
            except:
                pass
            
            # Half cadence
            try:
                subdom = last.root.transpose(-2)
                suggestions.append({
                    'chord': f"{subdom.name}7",
                    'type': 'half_cadence',
                    'description': 'Half cadence on secondary dominant',
                })
            except:
                pass
        
        # plagal cadence
        if '7' in last.quality:
            try:
                subdom = last.root.transpose(-5)
                suggestions.append({
                    'chord': f"{subdom.name}",
                    'type': 'plagal_cadence',
                    'description': 'Plagal cadence (IV-I)',
                })
            except:
                pass
        
        return suggestions


class SubstitutionHandler:
    """
    Handles chord substitutions.
    
    Provides methods for:
    - Tritone substitutions
    - Diminished substitutions
    - Modal interchange
    - Secondary dominants
    """
    
    def __init__(self, harmony_engine: HarmonyEngine):
        self.harmony_engine = harmony_engine
    
    def get_tritone_substitute(self, chord: Chord) -> Optional[Chord]:
        """
        Get the tritone substitute for a dominant chord.
        
        Args:
            chord: Dominant 7th chord
            
        Returns:
            Tritone substitute chord
        """
        if 'dom7' not in chord.quality:
            return None
        
        try:
            # Tritone is 6 semitones up
            new_root = chord.root.transpose(6)
            return Chord(new_root.name, 'min7')
        except:
            return None
    
    def get_diminished_substitute(self, chord: Chord) -> List[Chord]:
        """
        Get diminished chord substitutes.
        
        Args:
            chord: The chord to substitute
            
        Returns:
            List of possible diminished substitutes
        """
        substitutes = []
        
        # Any chord can be preceded by a diminished chord
        try:
            # Root a semitone above
            new_root = chord.root.transpose(1)
            substitutes.append(Chord(new_root.name, 'dim7'))
        except:
            pass
        
        # For dominant chords, can use diminished on any of the first 3 notes
        if 'dom7' in chord.quality:
            for offset in [1, 3, 6]:
                try:
                    new_root = chord.root.transpose(offset)
                    substitutes.append(Chord(new_root.name, 'dim7'))
                except:
                    pass
        
        return substitutes
    
    def get_secondary_dominants(self, key: str = 'C') -> List[Chord]:
        """
        Get secondary dominants for a key.
        
        Args:
            key: The tonal key
            
        Returns:
            List of secondary dominant chords
        """
        dominants = []
        
        # V/V, V/vi, V/ii, V/iv
        secondary_roots = ['D', 'A', 'E', 'G']
        
        for root in secondary_roots:
            try:
                dominants.append(Chord(f"{root}7", 'dom7'))
            except:
                pass
        
        return dominants
    
    def apply_substitution(self, chord: Chord, sub_type: str) -> Optional[Chord]:
        """
        Apply a specific type of substitution.
        
        Args:
            chord: Original chord
            sub_type: Type of substitution
            
        Returns:
            Substituted chord
        """
        if sub_type == 'tritone':
            return self.get_tritone_substitute(chord)
        elif sub_type == 'diminished':
            subs = self.get_diminished_substitute(chord)
            return subs[0] if subs else None
        elif sub_type == 'relative_minor':
            try:
                minor = chord.root.transpose(-3)
                return Chord(minor.name, 'min7')
            except:
                return None
        elif sub_type == 'relative_major':
            try:
                major = chord.root.transpose(3)
                return Chord(major.name, 'maj7')
            except:
                return None
        
        return None


# Convenience functions
def create_expander() -> ProgressionExpander:
    """Create and return a ProgressionExpander instance."""
    return ProgressionExpander(HarmonyEngine())


def create_continuation_generator() -> ContinuationGenerator:
    """Create and return a ContinuationGenerator instance."""
    return ContinuationGenerator(HarmonyEngine())


def create_substitution_handler() -> SubstitutionHandler:
    """Create and return a SubstitutionHandler instance."""
    return SubstitutionHandler(HarmonyEngine())

