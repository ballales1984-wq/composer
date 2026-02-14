"""
Unit tests for the models module.
"""
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from models.note import Note
from models.chord import Chord
from models.scale import Scale
from models.arpeggio import Arpeggio


class TestNote:
    """Test Note model functionality."""

    def test_note_creation(self):
        """Test basic note creation."""
        note = Note('C4')
        assert note.name == 'C4'
        assert note.letter == 'C'
        assert note.octave == 4
        assert note.semitone == 60  # C4 = 60 semitones from C0

    def test_note_transposition(self):
        """Test note transposition."""
        c4 = Note('C4')
        d4 = c4.transpose(2)
        assert d4.name == 'D4'

        b3 = c4.transpose(-1)
        assert b3.name == 'B3'

    def test_note_enharmonic_equivalence(self):
        """Test enharmonic equivalents."""
        c_sharp = Note('C#4')
        d_flat = Note('Db4')
        assert c_sharp.semitone == d_flat.semitone
        assert c_sharp.name != d_flat.name  # Different names, same pitch

    def test_invalid_note(self):
        """Test invalid note handling."""
        with pytest.raises(ValueError):
            Note('H4')  # H is not a valid note letter

        with pytest.raises(ValueError):
            Note('C')   # Missing octave


class TestChord:
    """Test Chord model functionality."""

    def test_major_chord_creation(self):
        """Test major chord creation."""
        c_maj = Chord('C', 'maj')
        assert c_maj.root.name == 'C4'
        assert len(c_maj.notes) == 3

        # Check notes are correct
        note_names = [n.name for n in c_maj.notes]
        assert 'C4' in note_names
        assert 'E4' in note_names
        assert 'G4' in note_names

    def test_minor_chord_creation(self):
        """Test minor chord creation."""
        a_min = Chord('A', 'min')
        note_names = [n.name for n in a_min.notes]
        assert 'A4' in note_names
        assert 'C5' in note_names
        assert 'E5' in note_names

    def test_dominant_seventh_chord(self):
        """Test dominant seventh chord."""
        g7 = Chord('G', 'dom7')
        assert len(g7.notes) == 4

        note_names = [n.name for n in g7.notes]
        assert 'G4' in note_names
        assert 'B4' in note_names
        assert 'D5' in note_names
        assert 'F5' in note_names


class TestScale:
    """Test Scale model functionality."""

    def test_major_scale_creation(self):
        """Test major scale creation."""
        c_major = Scale('C', 'major')
        assert len(c_major.notes) == 7

        # Check scale notes
        expected_notes = ['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4']
        actual_notes = [n.name for n in c_major.notes]
        assert actual_notes == expected_notes

    def test_minor_scale_creation(self):
        """Test natural minor scale creation."""
        a_minor = Scale('A', 'minor')
        assert len(a_minor.notes) == 7

        expected_notes = ['A4', 'B4', 'C5', 'D5', 'E5', 'F5', 'G5']
        actual_notes = [n.name for n in a_minor.notes]
        assert actual_notes == expected_notes

    def test_scale_degree_access(self):
        """Test accessing scale degrees."""
        c_major = Scale('C', 'major')

        # Test get_degree method
        third_degree = c_major.get_degree(3)
        assert third_degree.name == 'E4'

        seventh_degree = c_major.get_degree(7)
        assert seventh_degree.name == 'B4'

    def test_invalid_scale(self):
        """Test invalid scale handling."""
        with pytest.raises(ValueError):
            Scale('C', 'nonexistent_scale_type')


class TestArpeggio:
    """Test Arpeggio model functionality."""

    def test_triad_arpeggio_creation(self):
        """Test triad arpeggio creation."""
        c_maj_arp = Arpeggio('C', 'maj', 'up')
        assert len(c_maj_arp.notes) == 3

        note_names = [n.name for n in c_maj_arp.notes]
        assert note_names == ['C4', 'E4', 'G4']

    def test_arpeggio_direction(self):
        """Test arpeggio direction patterns."""
        c_maj_up = Arpeggio('C', 'maj', 'up')
        c_maj_down = Arpeggio('C', 'maj', 'down')

        up_notes = [n.name for n in c_maj_up.notes]
        down_notes = [n.name for n in c_maj_down.notes]

        assert up_notes == ['C4', 'E4', 'G4']
        assert down_notes == ['G4', 'E4', 'C4']  # Reversed

    def test_arpeggio_patterns(self):
        """Test different arpeggio patterns."""
        c_maj_updown = Arpeggio('C', 'maj', 'up_down')
        notes = [n.name for n in c_maj_updown.notes]
        # Should be: C, E, G, G, E, C
        expected = ['C4', 'E4', 'G4', 'G4', 'E4', 'C4']
        assert notes == expected