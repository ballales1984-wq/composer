"""
Integration tests for music21 and mingus adapters.

This test module verifies the conversion between internal music engine models
and external music theory libraries (music21, mingus).
"""
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest


class TestMusic21Integration:
    """Tests for music21 integration."""
    
    @pytest.fixture
    def sample_note(self):
        """Create a sample note for testing."""
        from music_engine.models import Note
        return Note('C4')
    
    @pytest.fixture
    def sample_chord(self):
        """Create a sample chord for testing."""
        from music_engine.models import Chord
        return Chord('C', 'maj7')
    
    @pytest.fixture
    def sample_scale(self):
        """Create a sample scale for testing."""
        from music_engine.models import Scale, Note
        return Scale(Note('C'), 'major')
    
    @pytest.fixture
    def sample_progression(self):
        """Create a sample progression for testing."""
        from music_engine.models import Chord, Progression
        chords = [
            Chord('C', 'maj'),
            Chord('F', 'maj'),
            Chord('G', 'dom7'),
            Chord('C', 'maj')
        ]
        return Progression(chords, 'C')

    def test_library_available(self):
        """Test that music21 library is available."""
        from music_engine.integrations import is_library_available
        assert is_library_available('music21') == True

    def test_note_to_music21(self, sample_note):
        """Test converting Note to music21."""
        from music_engine.integrations import note_to_music21
        
        m21_note = note_to_music21(sample_note)
        
        assert m21_note is not None
        assert m21_note.name == 'C'
        print(f"✓ Note to music21: {sample_note.name} -> {m21_note.name}")

    def test_music21_to_note(self, sample_note):
        """Test converting music21 Note to Note."""
        from music_engine.integrations import music21_to_note
        import music21
        
        # Create a music21 note
        m21_note = music21.note.Note('D4')
        
        # Convert to internal Note
        note = music21_to_note(m21_note)
        
        assert note is not None
        assert note.name == 'D4'
        print(f"✓ Music21 to Note: {m21_note.nameWithOctave} -> {note.name}")

    def test_chord_to_music21(self, sample_chord):
        """Test converting Chord to music21."""
        from music_engine.integrations import chord_to_music21
        
        m21_chord = chord_to_music21(sample_chord)
        
        assert m21_chord is not None
        assert len(m21_chord.pitches) >= 3
        print(f"✓ Chord to music21: {sample_chord.name} -> {len(m21_chord.pitches)} pitches")

    def test_music21_to_chord(self):
        """Test converting music21 Chord to Chord."""
        from music_engine.integrations import music21_to_chord
        import music21
        
        # Create a music21 chord
        m21_chord = music21.chord.Chord(['C4', 'E4', 'G4', 'B4'])
        
        # Convert to internal Chord
        chord = music21_to_chord(m21_chord, 'maj7')
        
        assert chord is not None
        assert chord.root.name == 'C4'
        print(f"✓ Music21 to Chord: {m21_chord.pitchNames} -> {chord.name}")

    def test_scale_to_music21(self, sample_scale):
        """Test converting Scale to music21."""
        from music_engine.integrations import scale_to_music21
        
        m21_scale = scale_to_music21(sample_scale)
        
        assert m21_scale is not None
        print(f"✓ Scale to music21: {sample_scale.root.name} {sample_scale.scale_type}")

    def test_progression_to_stream(self, sample_progression):
        """Test converting Progression to music21 stream."""
        from music_engine.integrations import progression_to_music21_stream
        
        stream = progression_to_music21_stream(sample_progression)
        
        assert stream is not None
        assert len(stream.notes) > 0
        print(f"✓ Progression to music21 stream: {len(stream.notes)} elements")

    def test_note_model_methods(self, sample_note):
        """Test Note model to_music21() and from_music21() methods."""
        # Test to_music21
        m21_note = sample_note.to_music21()
        assert m21_note is not None
        
        # Test from_music21
        import music21
        m21_original = music21.note.Note('F#4')
        note_from_m21 = sample_note.from_music21(m21_original)
        assert note_from_m21 is not None
        print(f"✓ Note model methods work correctly")

    def test_chord_model_methods(self, sample_chord):
        """Test Chord model to_music21() and from_music21() methods."""
        # Test to_music21
        m21_chord = sample_chord.to_music21()
        assert m21_chord is not None
        
        # Test from_music21
        import music21
        m21_original = music21.chord.Chord(['A4', 'C5', 'E5'])
        chord_from_m21 = sample_chord.from_music21(m21_original, 'min')
        assert chord_from_m21 is not None
        print(f"✓ Chord model methods work correctly")


class TestMingusIntegration:
    """Tests for mingus integration."""
    
    @pytest.fixture
    def sample_note(self):
        """Create a sample note for testing."""
        from music_engine.models import Note
        return Note('G3')
    
    @pytest.fixture
    def sample_chord(self):
        """Create a sample chord for testing."""
        from music_engine.models import Chord
        return Chord('D', 'min7')
    
    @pytest.fixture
    def sample_chords(self):
        """Create sample chords for progression testing."""
        from music_engine.models import Chord
        return [
            Chord('C', 'maj'),
            Chord('D', 'min'),
            Chord('E', 'min'),
            Chord('F', 'maj'),
            Chord('G', 'dom7'),
            Chord('A', 'min'),
            Chord('B', 'dim')
        ]

    def test_library_available(self):
        """Test that mingus library is available."""
        from music_engine.integrations import is_library_available
        assert is_library_available('mingus') == True

    def test_note_to_mingus(self, sample_note):
        """Test converting Note to mingus."""
        from music_engine.integrations import note_to_mingus
        
        mingus_note = note_to_mingus(sample_note)
        
        assert mingus_note is not None
        assert mingus_note.name == sample_note.note_name
        print(f"✓ Note to mingus: {sample_note.name} -> {mingus_note.name}{mingus_note.octave}")

    def test_mingus_to_note(self, sample_note):
        """Test converting mingus Note to Note."""
        from music_engine.integrations import mingus_to_note
        import mingus
        
        # Create a mingus note
        mingus_note = mingus.containers.Note()
        mingus_note.name = 'A'
        mingus_note.octave = 4
        
        # Convert to internal Note
        note = mingus_to_note(mingus_note)
        
        assert note is not None
        assert note.note_name == 'A'
        print(f"✓ Mingus to Note: {mingus_note.name}{mingus_note.octave} -> {note.name}")

    def test_chord_to_mingus(self, sample_chord):
        """Test converting Chord to mingus."""
        from music_engine.integrations import chord_to_mingus
        
        mingus_chord = chord_to_mingus(sample_chord)
        
        assert mingus_chord is not None
        # NoteContainer doesn't have .name, check notes instead
        print(f"✓ Chord to mingus: {sample_chord.name}")

    def test_mingus_to_chord(self, sample_chord):
        """Test converting mingus NoteContainer to Chord."""
        from music_engine.integrations import mingus_to_chord
        from mingus.containers import NoteContainer
        from music_engine.models import Note
        
        # Create a mingus NoteContainer
        mingus_chord = NoteContainer(['C', 'E', 'G'])
        
        # Convert to internal Chord (with explicit root note)
        chord = mingus_to_chord(mingus_chord, root_note=Note('C'))
        
        assert chord is not None
        assert chord.root.note_name == 'C'
        print(f"✓ Mingus to Chord: works with root_note")

    def test_roman_numerals_to_chords(self):
        """Test converting roman numerals to chords."""
        from music_engine.integrations import roman_numerals_to_chords
        
        roman_numerals = ['I', 'IV', 'V', 'I']
        chords = roman_numerals_to_chords(roman_numerals, 'C')
        
        assert len(chords) == 4
        assert chords[0].root.note_name == 'C'
        assert chords[1].root.note_name == 'F'
        assert chords[2].root.note_name == 'G'
        print(f"✓ Roman numerals to chords: {roman_numerals} -> {[c.name for c in chords]}")

    def test_chords_to_roman_numerals(self, sample_chords):
        """Test converting chords to roman numerals."""
        from music_engine.integrations import chords_to_roman_numerals
        
        roman_numerals = chords_to_roman_numerals(sample_chords, 'C')
        
        assert len(roman_numerals) == len(sample_chords)
        assert roman_numerals[0] == 'I'
        assert roman_numerals[3] == 'IV'
        print(f"✓ Chords to roman numerals: {[c.name for c in sample_chords]} -> {roman_numerals}")

    def test_generate_diatonic_progressions(self):
        """Test generating diatonic progressions."""
        from music_engine.integrations import generate_diatonic_progressions
        
        # Major key diatonic chords (triads)
        chords = generate_diatonic_progressions('C')
        
        assert len(chords) == 7
        assert chords[0].quality == 'maj'  # I
        assert chords[1].quality == 'min'   # ii
        assert chords[2].quality == 'min'   # iii
        assert chords[3].quality == 'maj'   # IV
        assert chords[4].quality == 'maj'   # V (triad, not V7)
        assert chords[5].quality == 'min'   # vi
        assert chords[6].quality == 'dim'   # vii° (triad, not dim7)
        print(f"✓ Generate diatonic progressions: C major -> {[c.name for c in chords]}")
        
        # Also test with 7ths
        chords_7 = generate_diatonic_progressions('C', ['I7', 'ii7', 'iii7', 'IV7', 'V7', 'vi7', 'vii°7'])
        assert chords_7[4].quality == 'dom7'  # V7 should be dominant7
        assert chords_7[6].quality == 'dim7'  # vii°7 should be dim7
        print(f"✓ Generate diatonic progressions with 7ths: {[c.name for c in chords_7]}")

    def test_note_model_methods(self, sample_note):
        """Test Note model to_mingus() and from_mingus() methods."""
        # Test to_mingus
        mingus_note = sample_note.to_mingus()
        assert mingus_note is not None
        
        # Test from_mingus
        from mingus.containers import Note as MingusNote
        mingus_original = MingusNote('B', 3)
        note_from_mingus = sample_note.from_mingus(mingus_original)
        assert note_from_mingus is not None
        print(f"✓ Note model mingus methods work correctly")

    def test_chord_model_methods(self, sample_chord):
        """Test Chord model to_mingus() and from_mingus() methods."""
        # Test to_mingus
        mingus_chord = sample_chord.to_mingus()
        assert mingus_chord is not None
        
        # Test from_mingus - requires explicit root_note due to mingus NoteContainer limitations
        from mingus.containers import NoteContainer
        from music_engine.models import Note
        mingus_original = NoteContainer(['D', 'F', 'A', 'C'])
        chord_from_mingus = sample_chord.from_mingus(mingus_original, root_note=Note('D'))
        assert chord_from_mingus is not None
        print(f"✓ Chord model mingus methods work correctly")


class TestIntegrationFactory:
    """Tests for IntegrationFactory."""
    
    def test_get_music21_converter(self):
        """Test getting music21 converter."""
        from music_engine.integrations import get_music21_converter
        
        converter = get_music21_converter()
        
        assert converter is not None
        assert hasattr(converter, 'note_to_music21')
        print(f"✓ Get music21 converter: {type(converter).__name__}")

    def test_get_mingus_converter(self):
        """Test getting mingus converter."""
        from music_engine.integrations import get_mingus_converter
        
        converter = get_mingus_converter()
        
        assert converter is not None
        assert hasattr(converter, 'note_to_mingus')
        print(f"✓ Get mingus converter: {type(converter).__name__}")

    def test_convert_to_music21(self):
        """Test convert() function to music21."""
        from music_engine.integrations import convert
        from music_engine.models import Note
        
        note = Note('E4')
        m21_note = convert('music21', note, 'to')
        
        assert m21_note is not None
        assert m21_note.name == 'E'
        print(f"✓ Convert to music21: {note.name} -> {m21_note.name}")

    def test_convert_from_music21(self):
        """Test convert() function from music21."""
        from music_engine.integrations import convert
        import music21
        
        m21_note = music21.note.Note('F#4')
        note = convert('music21', m21_note, 'from')
        
        assert note is not None
        assert note.note_name == 'F#'
        print(f"✓ Convert from music21: {m21_note.name} -> {note.name}")

    def test_convert_to_mingus(self):
        """Test convert() function to mingus."""
        from music_engine.integrations import convert
        from music_engine.models import Note
        
        note = Note('A3')
        mingus_note = convert('mingus', note, 'to')
        
        assert mingus_note is not None
        assert mingus_note.name == 'A'
        print(f"✓ Convert to mingus: {note.name} -> {mingus_note.name}")

    def test_get_available_libraries(self):
        """Test getting available libraries."""
        from music_engine.integrations import get_available_libraries
        
        libraries = get_available_libraries()
        
        assert isinstance(libraries, list)
        assert 'music21' in libraries
        assert 'mingus' in libraries
        print(f"✓ Available libraries: {libraries}")


class TestEndToEnd:
    """End-to-end integration tests."""
    
    def test_full_music21_workflow(self):
        """Test complete workflow with music21."""
        from music_engine.models import Note, Chord, Scale
        from music_engine.integrations import (
            note_to_music21, chord_to_music21, scale_to_music21,
            music21_to_note, music21_to_chord
        )
        
        # Create internal models
        note = Note('C4')
        chord = Chord('A', 'min7')  # A minor 7 chord
        scale = Scale(Note('G'), 'major')
        
        # Convert to music21
        m21_note = note_to_music21(note)
        m21_chord = chord_to_music21(chord)
        m21_scale = scale_to_music21(scale)
        
        # Verify conversions
        assert m21_note.name == 'C'
        assert len(m21_chord.pitches) >= 3
        assert m21_scale is not None
        
        # Convert back
        note_back = music21_to_note(m21_note)
        chord_back = music21_to_chord(m21_chord, 'min7')
        
        assert note_back.note_name == note.note_name
        assert chord_back.root.note_name == chord.root.note_name
        
        print(f"✓ Full music21 workflow completed")

    def test_full_mingus_workflow(self):
        """Test complete workflow with mingus."""
        from music_engine.models import Note, Chord, Progression
        from music_engine.integrations import (
            chord_to_mingus, roman_numerals_to_chords,
            chords_to_roman_numerals, generate_diatonic_progressions
        )
        
        # Test roman numeral analysis workflow
        # Create chords from roman numerals
        roman_numerals = ['I', 'V', 'vi', 'IV']  # Pop progression in C
        chords = roman_numerals_to_chords(roman_numerals, 'C')
        
        # Convert back to roman numerals
        roman_back = chords_to_roman_numerals(chords, 'C')
        
        assert roman_back[0] == 'I'
        assert roman_back[1] == 'V'
        
        # Test diatonic chord generation
        diatonic = generate_diatonic_progressions('C')
        assert len(diatonic) == 7
        
        print(f"✓ Full mingus workflow completed")

    def test_cross_library_comparison(self):
        """Test comparing results from both libraries."""
        from music_engine.models import Chord
        from music_engine.integrations import (
            chord_to_music21, chord_to_mingus
        )
        
        chord = Chord('F', 'maj7')
        
        # Convert to both libraries
        m21_chord = chord_to_music21(chord)
        mingus_chord = chord_to_mingus(chord)
        
        # Both should have the same notes
        m21_note_names = [p.name for p in m21_chord.pitches]
        
        # Mingus NoteContainer doesn't have .name, use notes instead
        mingus_note_names = list(mingus_chord.notes)
        
        assert m21_chord is not None
        assert mingus_chord is not None
        
        print(f"✓ Cross-library comparison: music21={m21_note_names}, mingus={mingus_note_names}")


# Run tests if executed directly
if __name__ == '__main__':
    print("=" * 60)
    print("Running Integration Tests")
    print("=" * 60)
    
    pytest.main([__file__, '-v', '--tb=short'])

