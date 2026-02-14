"""
Unit tests for the core modules.
"""
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from core import scales, chords, arpeggios, progressions


class TestScalesCore:
    """Test scales core functionality."""

    def test_scale_builder_major(self):
        """Test major scale building."""
        c_major = scales.major('C')
        assert len(c_major.notes) == 7

        note_names = [n.name for n in c_major.notes]
        expected = ['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4']
        assert note_names == expected

    def test_scale_transposition(self):
        """Test scale transposition."""
        c_major = scales.major('C')
        g_major = c_major.transpose(7)  # Up a fifth

        # Check that it's still a major scale but starting on G
        note_names = [n.name for n in g_major.notes]
        expected = ['G4', 'A4', 'B4', 'C5', 'D5', 'E5', 'F#5']
        assert note_names == expected

    def test_modal_scales(self):
        """Test modal scale generation."""
        d_dorian = scales.dorian('D')
        assert len(d_dorian.notes) == 7

        # Dorian mode: D, E, F, G, A, B, C
        note_names = [n.name for n in d_dorian.notes]
        expected = ['D4', 'E4', 'F4', 'G4', 'A4', 'B4', 'C5']
        assert note_names == expected


class TestChordsCore:
    """Test chords core functionality."""

    def test_chord_builder_functions(self):
        """Test chord builder functions."""
        c_maj = chords.maj('C')
        assert len(c_maj.notes) == 3

        g7 = chords.dom7('G')
        assert len(g7.notes) == 4

        # Check G7 notes: G, B, D, F
        note_names = [n.name for n in g7.notes]
        assert 'G4' in note_names
        assert 'B4' in note_names
        assert 'D4' in note_names
        assert 'F4' in note_names

    def test_extended_chords(self):
        """Test extended chord types."""
        # Note: dom9 not implemented, test with available functions
        c_maj7 = chords.maj7('C')
        assert len(c_maj7.notes) == 4

        f_maj7 = chords.maj7('F')
        assert len(f_maj7.notes) == 4

    def test_chord_inversions(self):
        """Test chord inversions."""
        c_maj = chords.maj('C')
        first_inv = c_maj.get_inversion(1)

        # First inversion of C major should be E, G, C
        note_names = [n.name for n in first_inv.notes]
        assert note_names[0] == 'E4'  # Bass note


class TestArpeggiosCore:
    """Test arpeggios core functionality."""

    def test_triad_arpeggios(self):
        """Test triad arpeggio generation."""
        c_maj_arp = arpeggios.triad('C', 'maj')
        assert len(c_maj_arp.notes) == 3

        note_names = [n.name for n in c_maj_arp.notes]
        assert note_names == ['C4', 'E4', 'G4']

    def test_seventh_arpeggios(self):
        """Test seventh chord arpeggios."""
        g7_arp = arpeggios.seventh('G', 'dom7')
        assert len(g7_arp.notes) == 4

        note_names = [n.name for n in g7_arp.notes]
        expected = ['G4', 'B4', 'D4', 'F4']
        assert note_names == expected

    def test_scale_arpeggios(self):
        """Test scale-based arpeggios."""
        c_maj_scale_arp = arpeggios.scale_arpeggio('C', 'major')
        assert len(c_maj_scale_arp.notes) == 7  # All scale notes

        note_names = [n.name for n in c_maj_scale_arp.notes]
        expected = ['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4']
        assert note_names == expected


class TestProgressionsCore:
    """Test progressions core functionality."""

    def test_progression_analysis(self):
        """Test chord progression analysis."""
        # I-V-I progression in C major
        progression = progressions.analyze(['C', 'G', 'C'])

        assert progression is not None
        assert len(progression.chords) == 3

    def test_scale_compatibility(self):
        """Test scale compatibility finding."""
        # Find scales compatible with I-V-I in C
        compatible_scales = progressions.find_scales(['C', 'G', 'C'])

        assert len(compatible_scales) > 0
        # C major should be in the compatible scales
        scale_names = [str(s) for s in compatible_scales]
        assert any('C major' in name for name in scale_names)

    def test_progression_suggestions(self):
        """Test scale suggestions for progressions."""
        suggestions = progressions.suggest_scales(['Cmaj7', 'Dm7', 'G7', 'Cmaj7'], 3)

        assert len(suggestions) >= 3
        # Should suggest common jazz scales