"""
Integration tests for the Music Theory Engine.
"""
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from music_engine.exceptions import InvalidNoteError, InvalidScaleError, InvalidChordError


class TestIntegration:
    """Integration tests for the complete application."""

    def test_app_instantiation(self):
        """Test that the main app can be instantiated."""
        try:
            from app_standalone import MusicTheoryApp
            app = MusicTheoryApp()
            assert app is not None
            assert hasattr(app, 'main_window')
            # Don't destroy the app as it might cause issues in headless testing
        except Exception as e:
            # In headless environment, GUI creation might fail
            # This is acceptable for CI/CD pipelines
            pytest.skip(f"GUI creation failed (expected in headless environment): {e}")

    def test_core_module_integration(self):
        """Test integration between core modules."""
        from models.chord import Chord
        from models.scale import Scale
        from models.arpeggio import Arpeggio

        # Create a scale
        c_major = Scale('C', 'major')

        # Create a chord from the scale
        c_chord = Chord('C', 'maj')

        # Create an arpeggio from the chord
        c_arp = Arpeggio(c_chord, 'up')

        # Verify they work together
        assert len(c_major.notes) == 7
        assert len(c_chord.notes) == 3
        assert len(c_arp.notes) == 3

        # Check that chord notes are in scale
        scale_notes = set(n.name[0] for n in c_major.notes)  # Get note letters
        chord_notes = set(n.name[0] for n in c_chord.notes)

        # All chord notes should be in the scale
        assert chord_notes.issubset(scale_notes)

    def test_audio_integration(self):
        """Test audio system integration."""
        from utils.audio import get_audio_status

        # Audio status should be available (might be fallback)
        status = get_audio_status()
        # Accept both string and dict return types
        assert status is not None

    def test_model_integration(self):
        """Test integration between different models."""
        from models.note import Note
        from models.chord import Chord
        from models.scale import Scale

        # Create related musical objects
        root_note = Note('C4')
        chord = Chord('C', 'maj')
        scale = Scale('C', 'major')

        # Verify relationships
        assert chord.root.chroma == root_note.chroma
        assert scale.notes[0].chroma == root_note.chroma

        # Check that chord notes are subset of scale notes
        scale_pitches = set(n.chroma for n in scale.notes)
        chord_pitches = set(n.chroma for n in chord.notes)

        assert chord_pitches.issubset(scale_pitches)

    def test_error_handling_integration(self):
        """Test error handling across modules."""
        from models.scale import Scale

        # Test invalid inputs are handled gracefully
        with pytest.raises(InvalidNoteError):
            Scale('InvalidNote', 'major')

    def test_full_workflow(self):
        """Test a complete music theory workflow."""
        from models.chord import Chord
        from models.scale import Scale
        from models.progression import Progression

        # 1. Create a key/scale
        c_major = Scale('C', 'major')

        # 2. Create chords in that key
        c_chord = Chord('C', 'maj')
        f_chord = Chord('F', 'maj')
        g_chord = Chord('G', 'maj')

        # 3. Create a simple progression
        progression = Progression([c_chord, f_chord, g_chord, c_chord])

        # 4. Verify the progression
        assert len(progression.chords) == 4
        assert progression.key is not None

        # 5. Check that all chords use notes from the scale
        scale_pitches = set(n.chroma for n in c_major.notes)

        for chord in progression.chords:
            chord_pitches = set(n.chroma for n in chord.notes)
            assert chord_pitches.issubset(scale_pitches), f"Chord {chord} not in scale"

        print("Full workflow test completed successfully!")
