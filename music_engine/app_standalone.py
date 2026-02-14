#!/usr/bin/env python3
"""
Standalone Music Theory Engine Application
No complex imports, everything in one file for easy execution.
"""

import sys
import os
import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
import time
import winsound  # Windows audio fallback
import threading

# MIDI support
try:
    import mido
    MIDI_AVAILABLE = True
except ImportError:
    MIDI_AVAILABLE = False
    print("MIDI support not available - install mido: pip install mido")

# Set appearance - modern design inspired by professional music apps
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# Professional color scheme with modern gradients
COLORS = {
    # Primary actions (Play, Music)
    'primary': '#6366F1',      # Modern indigo
    'primary_hover': '#4F46E5', # Darker indigo
    'hover_primary': '#4F46E5', # Alias for primary_hover
    'primary_light': '#E0E7FF', # Light indigo background

    # Secondary actions (Learn, Analyze)
    'secondary': '#F59E0B',    # Warm amber
    'secondary_hover': '#D97706', # Darker amber
    'secondary_light': '#FEF3C7', # Light amber background

    # Creative actions (Build, Create)
    'accent': '#EC4899',       # Vibrant pink
    'accent_hover': '#DB2777', # Darker pink
    'accent_light': '#FCE7F3', # Light pink background

    # Status colors
    'success': '#10B981',      # Emerald success
    'success_hover': '#059669', # Darker emerald
    'warning': '#F97316',      # Orange warning
    'danger': '#EF4444',       # Red danger
    'danger_hover': '#DC2626', # Darker red

    # Neutral tones
    'neutral': '#64748B',      # Slate for text
    'neutral_light': '#94A3B8', # Light slate
    'neutral_lighter': '#E2E8F0', # Very light slate

    # Surfaces and backgrounds
    'background': '#FEFEFE',   # Pure white
    'bg_surface': '#FEFEFE',   # Background surface (alias)
    'bg_elevated': '#FFFFFF',  # Elevated background (alias for surface)
    'surface': '#FFFFFF',      # Card surfaces
    'surface_hover': '#F8FAFC', # Hover surfaces
    'border': '#E2E8F0',       # Subtle borders
    'shadow': '#F1F5F9',       # Shadow color

    # Text hierarchy
    'text_primary': '#1E293B',  # Dark slate for headings
    'text_secondary': '#64748B', # Medium slate for body
    'text_muted': '#94A3B8',   # Light slate for muted text

    # Special colors for UI elements
    'music_blue': '#00D4AA',   # Teal for music elements
    'music_purple': '#6C5CE7', # Purple for music elements
    'highlight': '#FDCB6E',    # Yellow highlight

    # Button gradients (legacy support)
    'button_primary_start': '#6366F1',
    'button_primary_end': '#4F46E5',
    'button_secondary_start': '#F59E0B',
    'button_secondary_end': '#D97706'
}

# Gradient definitions for special effects
GRADIENTS = {
    'primary': ['#6366F1', '#4F46E5'],    # Indigo gradient
    'success': ['#10B981', '#059669'],    # Green gradient
    'accent': ['#EC4899', '#DB2777'],     # Pink gradient
    'warm': ['#F59E0B', '#D97706']       # Gold gradient
}

# Tooltip definitions for better UX
TOOLTIPS = {
    # Scale Explorer
    'scale_menu': 'Seleziona una scala dalla libreria completa',
    'transpose_up': 'Aumenta la tonalità di un semitono',
    'transpose_down': 'Diminuisci la tonalità di un semitono',
    'relative_scale': 'Passa alla scala relativa (Maggiore ↔ Minore)',
    'play_scale': 'Ascolta la scala con la modalità selezionata',
    'scale_positions': 'Cicla tra le posizioni sul manico della chitarra',
    'scale_patterns': 'Visualizza diversi patterns per suonare la scala',
    'save_scale': 'Salva questa scala nei preferiti',

    # Chord Builder
    'chord_menu': 'Seleziona un accordo dalla libreria completa',
    'play_chord': 'Ascolta l\'accordo simultaneamente',

    # Progression Analyzer
    'progression_menu': 'Scegli una progressione comune',
    'play_progression': 'Ascolta la progressione completa',
    'analyze_progression': 'Analizza la compatibilità delle scale',

    # Metronome
    'bpm_slider': 'Regola il tempo in battiti per minuto (60-200 BPM)',
    'start_metronome': 'Avvia il metronomo',
    'tap_tempo': 'Tocca per impostare il BPM',

    # Fretboard Viewer
    'update_fretboard': 'Aggiorna la visualizzazione dal tab corrente',
    'clear_fretboard': 'Cancella tutte le evidenziazioni',
    'tuning_menu': 'Cambia l\'accordatura della chitarra',

    # Exercises
    'exercise_menu': 'Scegli il tipo di esercizio',
    'start_exercise': 'Inizia l\'esercizio selezionato',

    # General
    'test_audio': 'Verifica che l\'audio funzioni correttamente'
}

# Note transposition utilities
NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
NOTES_FLAT = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']

def transpose_note(note, semitones):
    """Transpose a note by given semitones"""
    if note[-1].isdigit():
        octave = int(note[-1])
        note_name = note[:-1]
    else:
        octave = 4
        note_name = note

    # Handle sharps and flats
    if note_name in NOTES_FLAT:
        note_idx = NOTES_FLAT.index(note_name)
    elif note_name in NOTES:
        note_idx = NOTES.index(note_name)
    else:
        return note  # Unknown note

    new_idx = (note_idx + semitones) % 12
    new_note = NOTES_FLAT[new_idx] if note_name in NOTES_FLAT else NOTES[new_idx]

    # Calculate octave change
    octave_change = (note_idx + semitones) // 12
    new_octave = octave + octave_change

    return f"{new_note}{new_octave}"

def transpose_chord(chord_notes, semitones):
    """Transpose a chord by given semitones"""
    return [transpose_note(note, semitones) for note in chord_notes]

def generate_all_chords():
    """Generate complete chord database for all keys"""
    # Base chords in C - mapping chord suffixes to note patterns
    base_chords = {
        'Major': ['C4', 'E4', 'G4'],
        'Minor': ['C4', 'Eb4', 'G4'],
        'Diminished': ['C4', 'Eb4', 'Gb4'],
        'Augmented': ['C4', 'E4', 'G#4'],
        '7': ['C4', 'E4', 'G4', 'Bb4'],
        'maj7': ['C4', 'E4', 'G4', 'B4'],
        'm7': ['C4', 'Eb4', 'G4', 'Bb4'],
        'dim7': ['C4', 'Eb4', 'Gb4', 'Bbb4'],
        '9': ['C4', 'E4', 'G4', 'Bb4', 'D4'],
        'm9': ['C4', 'Eb4', 'G4', 'Bb4', 'D4'],
        'maj9': ['C4', 'E4', 'G4', 'B4', 'D4'],
        '6': ['C4', 'E4', 'G4', 'A4'],
        'm6': ['C4', 'Eb4', 'G4', 'A4'],
        'sus2': ['C4', 'D4', 'G4'],
        'sus4': ['C4', 'F4', 'G4'],
        '5': ['C4', 'G4'],  # Power chord
        '11': ['C4', 'E4', 'G4', 'Bb4', 'D4', 'F4'],
        'm11': ['C4', 'Eb4', 'G4', 'Bb4', 'D4', 'F4'],
        'maj11': ['C4', 'E4', 'G4', 'B4', 'D4', 'F4'],
        '13': ['C4', 'E4', 'G4', 'Bb4', 'D4', 'F4', 'A4'],
        'm13': ['C4', 'Eb4', 'G4', 'Bb4', 'D4', 'F4', 'A4'],
        'maj13': ['C4', 'E4', 'G4', 'B4', 'D4', 'F4', 'A4']
    }

    # Special chord types that need spaces in names
    spaced_types = ['6/9', '7#11', 'Quartal', 'Quintal']

    # Add spaced chord types
    base_chords.update({
        '6/9': ['C4', 'E4', 'G4', 'A4', 'D4'],
        '7#11': ['C4', 'E4', 'G4', 'Bb4', 'F#4'],
        'Quartal': ['C4', 'F4', 'Bb4', 'Eb4'],
        'Quintal': ['C4', 'G4', 'D4', 'A4']
    })

    all_chords = {}

    # Generate chords for all 12 keys
    for root_idx, root in enumerate(NOTES_FLAT):
        for chord_type, notes in base_chords.items():
            if chord_type in spaced_types:
                chord_name = f"{root} {chord_type}"
            else:
                chord_name = f"{root}{chord_type}"
            all_chords[chord_name] = transpose_chord(notes, root_idx)

    # Add aliases for common chord names (with spaces and short forms)
    aliases = {}
    for chord_name in list(all_chords.keys()):
        # Add spaced versions
        if 'Major' in chord_name:
            alias = chord_name.replace('Major', ' Major')
            aliases[alias] = all_chords[chord_name]
        elif 'Minor' in chord_name:
            alias = chord_name.replace('Minor', ' Minor')
            aliases[alias] = all_chords[chord_name]
            # Add short minor alias (Gm, Am, etc.)
            root = chord_name.replace('Minor', '')
            short_minor = f"{root}m"
            aliases[short_minor] = all_chords[chord_name]
        elif 'Diminished' in chord_name:
            alias = chord_name.replace('Diminished', ' Diminished')
            aliases[alias] = all_chords[chord_name]
        elif 'Augmented' in chord_name:
            alias = chord_name.replace('Augmented', ' Augmented')
            aliases[alias] = all_chords[chord_name]

    all_chords.update(aliases)

    # Add special chords that are missing
    special_chords = {}

    # Minor chords with sharps
    sharp_minors = ['F#', 'C#', 'G#']
    for root in sharp_minors:
        root_idx = NOTES.index(root) if root in NOTES else NOTES_FLAT.index(root)
        special_chords[f'{root} Minor'] = transpose_chord(['C4', 'Eb4', 'G4'], root_idx)

    # Diminished 7ths with sharps
    sharp_dim7ths = ['C#', 'D#', 'F#', 'G#', 'A#']
    for root in sharp_dim7ths:
        root_idx = NOTES.index(root)
        special_chords[f'{root}dim7'] = transpose_chord(['C4', 'Eb4', 'Gb4', 'Bb4'], root_idx)

    # Generate 6/9 and 7#11 chords for all keys (both with and without spaces)
    extended_chords = {
        '6/9': ['C4', 'E4', 'G4', 'A4', 'D4'],
        'm6/9': ['C4', 'Eb4', 'G4', 'A4', 'D4'],  # Minor 6/9
        '7#11': ['C4', 'E4', 'G4', 'Bb4', 'F#4']
    }

    for root_idx, root in enumerate(NOTES_FLAT):
        for chord_type, notes in extended_chords.items():
            # Add with space
            chord_name_spaced = f"{root} {chord_type}"
            special_chords[chord_name_spaced] = transpose_chord(notes, root_idx)
            # Add without space (for menu compatibility)
            chord_name_compact = f"{root}{chord_type}"
            special_chords[chord_name_compact] = transpose_chord(notes, root_idx)

    all_chords.update(special_chords)

    return all_chords

# Modern styling constants
STYLES = {
    'corner_radius': 12,
    'border_width': 2,
    'font_title': ('Arial', 18, 'bold'),
    'font_subtitle': ('Arial', 14, 'bold'),
    'font_body': ('Arial', 12),
    'font_small': ('Arial', 10),
    'shadow_offset': 2,
    'animation_duration': 300
}

# Advanced audio player with polyphony support
class SimpleAudioPlayer:
    def __init__(self):
        self.is_available = True
        self.polyphony_available = False

        # Try to enable polyphony with numpy and simpleaudio
        try:
            import numpy as np
            self.np = np
            # Test simpleaudio availability
            import simpleaudio as sa
            self.sa = sa
            self.polyphony_available = True
            print("Polyphony enabled with numpy + simpleaudio synthesis!")
        except ImportError as e:
            print(f"⚠️  Polyphony not available ({e}) - using sequential playback")
            self.polyphony_available = False

    def play_note(self, note_name, duration=0.5):
        """Play a simple beep for the note"""
        try:
            # Standard note frequencies (A4 = 440Hz)
            note_freqs = {
                'C': 261.63, 'C#': 277.18, 'D': 293.66, 'D#': 311.13,
                'E': 329.63, 'F': 349.23, 'F#': 369.99, 'G': 392.00,
                'G#': 415.30, 'A': 440.00, 'A#': 466.16, 'B': 493.88
            }

            # Parse note (support formats: "C", "C4", "C#", "C#4")
            note_name = note_name.strip().upper()

            # Extract octave if present
            if note_name[-1].isdigit():
                octave = int(note_name[-1])
                note = note_name[:-1]
            else:
                octave = 4
                note = note_name

            # Validate note
            if note not in note_freqs:
                return False

            # Calculate frequency for the specific octave
            # A4 = 440Hz, each octave doubles/halves the frequency
            freq = note_freqs[note] * (2 ** (octave - 4))

            # Play beep (clamp frequency to valid range)
            freq = max(37, min(32767, int(freq)))  # Windows Beep limits
            winsound.Beep(freq, int(duration * 1000))
            return True
        except Exception as e:
            print(f"Audio error: {e}")
            return False

    def generate_chord_wave(self, notes, duration=2.0, sample_rate=44100):
        """Generate a polyphonic chord wave using additive synthesis"""
        if not self.polyphony_available:
            return None

        try:
            # Convert note names to frequencies
            frequencies = []
            for note in notes:
                freq = self._note_to_frequency(note)
                if freq:
                    frequencies.append(freq)

            if not frequencies:
                return None

            # Generate time array
            t = self.np.linspace(0, duration, int(sample_rate * duration), False)

            # Generate chord wave by summing sine waves
            chord_wave = self.np.zeros_like(t)
            for freq in frequencies:
                # Add sine wave for each note with slight amplitude variation
                amplitude = 0.3 / len(frequencies)  # Normalize amplitude
                chord_wave += amplitude * self.np.sin(2 * self.np.pi * freq * t)

            # Apply envelope for smoother sound (attack/decay)
            envelope = self._apply_envelope(t, duration)
            chord_wave *= envelope

            # Convert to 16-bit PCM
            chord_wave = (chord_wave * 32767).astype(self.np.int16)

            return chord_wave

        except Exception as e:
            print(f"Error generating chord wave: {e}")
            return None

    def _note_to_frequency(self, note_name):
        """Convert note name to frequency"""
        try:
            note_freqs = {
                'C': 261.63, 'C#': 277.18, 'D': 293.66, 'D#': 311.13,
                'E': 329.63, 'F': 349.23, 'F#': 369.99, 'G': 392.00,
                'G#': 415.30, 'A': 440.00, 'A#': 466.16, 'B': 493.88
            }

            note_name = note_name.strip().upper()

            # Extract octave if present
            if note_name[-1].isdigit():
                octave = int(note_name[-1])
                note = note_name[:-1]
            else:
                octave = 4
                note = note_name

            if note in note_freqs:
                return note_freqs[note] * (2 ** (octave - 4))

            return None
        except:
            return None

    def _apply_envelope(self, t, duration):
        """Apply ADSR envelope to smooth the sound"""
        # Simple attack-decay envelope
        attack_time = 0.1  # 100ms attack
        decay_time = 0.2   # 200ms decay

        envelope = self.np.ones_like(t)

        # Attack phase
        attack_samples = int(attack_time * len(t) / duration)
        if attack_samples > 0:
            envelope[:attack_samples] = self.np.linspace(0, 1, attack_samples)

        # Decay phase
        decay_samples = int(decay_time * len(t) / duration)
        if decay_samples > 0 and attack_samples + decay_samples < len(envelope):
            start_decay = attack_samples
            end_decay = attack_samples + decay_samples
            envelope[start_decay:end_decay] = self.np.linspace(1, 0.7, decay_samples)

        return envelope

    def play_chord(self, notes, duration=2.0):
        """Play chord with true polyphony using additive synthesis"""
        if not notes:
            return

        print(f"Playing chord with {len(notes)} notes: {notes}")

        # Normalize octaves to ensure chord sounds harmonious
        normalized_notes = self._normalize_chord_octaves(notes)
        print(f"Normalized notes: {normalized_notes}")

        # Try polyphonic synthesis first (if numpy + simpleaudio available)
        if self.polyphony_available:
            try:
                print("Using polyphonic synthesis!")
                chord_wave = self.generate_chord_wave(normalized_notes, duration)

                if chord_wave is not None:
                    # Play the synthesized chord
                    self._play_synthesized_chord(chord_wave)
                    return
                else:
                    print("Synthesis failed, falling back to sequential playback")

            except Exception as e:
                print(f"Polyphony synthesis error: {e}, falling back to sequential")

        # Fallback: Rapid sequential playback to simulate harmony
        print("🔄 Using rapid sequential playback to simulate chord...")
        self._play_chord_rapid(normalized_notes, duration)

    def _play_synthesized_chord(self, chord_wave):
        """Play a pre-synthesized chord wave"""
        try:
            # Use pre-imported simpleaudio
            play_obj = self.sa.play_buffer(chord_wave, 1, 2, 44100)
            play_obj.wait_done()
        except Exception as e:
            print(f"SimpleAudio playback failed: {e}")
            # Fallback: rapid sequential playback
            self._play_chord_rapid([], duration=1.0)

    def _play_chord_rapid(self, notes, duration=2.0):
        """Play chord notes in very rapid succession to simulate harmony"""
        if not notes:
            return

        # Play each note in very rapid succession
        note_duration = 0.05  # Very short notes
        overlap_delay = 0.02  # Slight overlap for richer sound

        threads = []
        for i, note in enumerate(notes):
            # Stagger the start times slightly for richer harmony
            delay = i * overlap_delay

            def play_note_with_delay(note_name, delay_time):
                time.sleep(delay_time)
                self.play_note(note_name, note_duration)

            thread = threading.Thread(target=play_note_with_delay, args=(note, delay))
            thread.daemon = True
            threads.append(thread)
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

    def _play_chord_sequential(self, notes, duration=2.0):
        """Fallback method: play chord notes in ultra-fast sequence"""
        # Try to create true simultaneity effect with minimal delay
        min_delay = 0.005  # 5ms - as close to simultaneous as possible
        note_duration = 0.8  # Shorter notes for faster playback

        # Method 1: Ultra-fast sequential playback
        print("Playing chord with ultra-fast sequential method...")
        for i, note in enumerate(notes):
            if i > 0:
                time.sleep(min_delay)  # Minimal delay between notes
            # Use threading for potential overlap
            thread = threading.Thread(target=self.play_note, args=(str(note), note_duration))
            thread.daemon = True
            thread.start()

        # Method 2: Layered approach for richer sound
        time.sleep(0.1)  # Brief pause
        for layer in range(2):  # 2 layers for richer sound
            for note in notes:
                thread = threading.Thread(target=self.play_note, args=(str(note), 0.4))
                thread.daemon = True
                thread.start()
                time.sleep(0.008)  # Very small stagger
            time.sleep(0.03)  # Pause between layers

    def _normalize_chord_octaves(self, notes):
        """Normalize chord notes to optimal octaves for harmonious playback"""
        if not notes:
            return notes

        normalized = []
        base_octave = 4  # Base octave for chord root

        for note in notes:
            # Parse note and octave
            if len(note) >= 2 and note[-1].isdigit():
                note_name = note[:-1]
                octave = int(note[-1])
            else:
                note_name = note
                octave = base_octave

            # For complex chords, ensure notes are within 1-2 octaves of root
            # This prevents extremely high or low notes that sound discordant
            if octave < base_octave - 1:
                octave = base_octave - 1
            elif octave > base_octave + 1:
                octave = base_octave + 1

            normalized.append(f"{note_name}{octave}")

        return normalized

    def _play_single_note(self, note_name, duration, delay=0):
        """Play a single note with optional delay"""
        try:
            if delay > 0:
                time.sleep(delay)

            print(f"Playing note: {note_name} for {duration}s")
            self.play_note(note_name, duration)
        except Exception as e:
            print(f"Error playing note {note_name}: {e}")

    def _play_note_async(self, note_name, duration):
        """Helper function to play a note asynchronously (legacy)"""
        self._play_single_note(note_name, duration)

# Global audio player
audio_player = SimpleAudioPlayer()

# MIDI Manager for guitar fretboard MIDI output
class MIDIManager:
    """Manager for MIDI output functionality"""

    def __init__(self):
        self.midi_available = MIDI_AVAILABLE
        self.midi_port = None
        self.velocity = 100  # Default MIDI velocity
        self.available_ports = []

        if self.midi_available:
            try:
                import mido
                self.available_ports = mido.get_output_names()
                if self.available_ports:
                    # Try to open the first available port
                    try:
                        self.midi_port = mido.open_output(self.available_ports[0])
                        print(f"MIDI port opened: {self.available_ports[0]}")
                    except:
                        print("Could not open default MIDI port")
                        self.midi_port = None
                else:
                    print("No MIDI output ports available")
            except Exception as e:
                print(f"MIDI initialization error: {e}")
                self.midi_available = False
        else:
            print("MIDI support not available - install 'mido' for MIDI functionality: pip install mido")

    def set_port(self, port_name):
        """Set the MIDI output port"""
        if not self.midi_available:
            print("MIDI not available")
            return False

        try:
            import mido
            if self.midi_port:
                self.midi_port.close()
            self.midi_port = mido.open_output(port_name)
            return True
        except Exception as e:
            print(f"Could not open MIDI port {port_name}: {e}")
            return False

    def play_note(self, midi_note_number, duration=0.5, velocity=None):
        """Play a MIDI note"""
        if not self.midi_available or not self.midi_port:
            return

        if velocity is None:
            velocity = self.velocity

        try:
            import mido
            # Send note on
            note_on = mido.Message('note_on', note=midi_note_number, velocity=velocity)
            self.midi_port.send(note_on)

            # Schedule note off
            def note_off():
                try:
                    off_msg = mido.Message('note_off', note=midi_note_number, velocity=0)
                    self.midi_port.send(off_msg)
                except:
                    pass

            threading.Timer(duration, note_off).start()

        except Exception as e:
            print(f"MIDI playback error: {e}")

    def stop_all_notes(self):
        """Stop all playing MIDI notes"""
        if not self.midi_available or not self.midi_port:
            return

        try:
            import mido
            # Send all notes off for all channels
            for channel in range(16):
                all_notes_off = mido.Message('control_change', control=123, value=0, channel=channel)
                self.midi_port.send(all_notes_off)
        except Exception as e:
            print(f"MIDI stop error: {e}")

    def close(self):
        """Close the MIDI port"""
        if self.midi_port:
            try:
                self.midi_port.close()
            except:
                pass
            self.midi_port = None

# Global MIDI manager
midi_manager = MIDIManager()

# Simple data classes
class Note:
    def __init__(self, name, octave=4):
        self.name = name
        self.octave = octave

    def __str__(self):
        return f"{self.name}{self.octave}"

class Scale:
    def __init__(self, root, scale_type, notes=None):
        self.root = root
        self.scale_type = scale_type
        self.notes = notes or []
        self.name = f"{root} {scale_type}"

class Chord:
    def __init__(self, root, quality, notes=None):
        self.root = root
        self.quality = quality
        self.notes = notes or []
        self.name = f"{root}{quality}"

# Constants for harmonization and roman numerals
ROMAN_NUMERALS = {
    1: 'I', 2: 'II', 3: 'III', 4: 'IV', 5: 'V', 6: 'VI', 7: 'VII'
}

ROMAN_QUALITY_SYMBOLS = {
    'major': '', 'minor': 'm', 'diminished': 'dim', 'augmented': 'aug'
}

# Scale interval names for educational display
SCALE_INTERVALS = {
    1: 'Tonica (Root)',
    2: 'Seconda Maggiore',
    3: 'Terza Maggiore',
    4: 'Quarta Perfetta',
    5: 'Quinta Perfetta',
    6: 'Sesta Maggiore',
    7: 'Settima Maggiore',
    8: 'Ottava (Root)',
    # Minor scale intervals
    '1b': 'Tonica (Root)',
    '2b': 'Seconda Minore',
    '3b': 'Terza Minore',
    '4b': 'Quarta Perfetta',
    '5b': 'Quinta Diminuita',
    '6b': 'Sesta Minore',
    '7b': 'Settima Minore',
    # Other intervals
    '4+': 'Quarta Aumentata',
    '5+': 'Quinta Aumentata',
    '6+': 'Sesta Aumentata',
    '7+': 'Settima Aumentata',
    '7--': 'Settima Diminuita'
}

# Scale type to interval pattern mapping
SCALE_INTERVAL_PATTERNS = {
    'major': [1, 2, 3, 4, 5, 6, 7, 8],
    'minor': [1, 2, '3b', 4, 5, '6b', '7b', 8],
    'harmonic_minor': [1, 2, '3b', 4, 5, '6b', 7, 8],
    'melodic_minor': [1, 2, '3b', 4, 5, 6, 7, 8],  # ascending
    'dorian': [1, 2, '3b', 4, 5, 6, '7b', 8],
    'phrygian': [1, '2b', '3b', 4, 5, '6b', '7b', 8],
    'lydian': [1, 2, 3, '4+', 5, 6, 7, 8],
    'mixolydian': [1, 2, 3, 4, 5, 6, '7b', 8],
    'aeolian': [1, 2, '3b', 4, 5, '6b', '7b', 8],
    'locrian': [1, '2b', '3b', 4, '5b', '6b', '7b', 8],
    'whole_tone': [1, 2, 3, '4+', '5+', '6+', 8],  # 6 notes
    'chromatic': [1, '2b', 2, '3b', 3, 4, '4+', 5, '5+', 6, '6+', 7, 8],  # 12 notes
    'diminished': [1, 2, '3b', 4, '5b', '5+', 6, 7, 8],  # 8 notes
    'augmented': [1, '2b', 3, 5, '5+', 7, 8],  # 6 notes

    # Additional exotic scales
    'bebop_dominant': [1, 2, 3, 4, 5, 6, '7b', 7, 8],  # 8 notes - chromatic approach
    'bebop_major': [1, 2, 3, 4, 5, '6b', 6, 7, 8],  # 8 notes
    'enigmatic': [1, '2b', 3, '4+', '5+', '6+', 7, 8],  # 7 notes - mysterious sound
    'hirajoshi': [1, 2, '3b', 5, '6b', 8],  # 5 notes - Japanese scale
    'in_sen': [1, '2b', 4, 5, '7b', 8],  # 5 notes - Japanese scale
    'iwato': [1, '2b', 4, '5b', '7b', 8],  # 5 notes - Japanese scale
    'kumoi': [1, 3, 4, 5, 7, 8],  # 5 notes - Japanese scale
    'pelog': [1, '2b', '3b', 5, '6b', 7, 8],  # 6 notes - Indonesian
    'slendro': [1, 2, '3b', 5, 6, 8],  # 5 notes - Indonesian
    'yo': [1, 3, 4, 5, 6, 8]  # 5 notes - Japanese
}

# Harmonization patterns for different scale types (1-3-5-7 voicing)
HARMONIZATION_PATTERNS = {
    'major': {
        1: 'maj7',   # I - Cmaj7
        2: 'm7',     # ii - Dm7
        3: 'm7',     # iii - Em7
        4: 'maj7',   # IV - Fmaj7
        5: '7',      # V - G7
        6: 'm7',     # vi - Am7
        7: 'dim7'    # vii° - Bdim7 (corrected from m7b5)
    },
    'minor': {
        1: 'm7',     # i - Cm7
        2: 'dim7',   # ii° - Ddim7 (corrected from m7b5)
        3: 'maj7',   # III - Ebmaj7
        4: 'm7',     # iv - Fm7
        5: 'm7',     # v - Gm7
        6: 'maj7',   # VI - Abmaj7
        7: '7'       # VII - Bb7
    },
    'harmonic_minor': {
        1: 'm7',     # i - Cm7
        2: 'dim7',   # ii° - Ddim7 (corrected from m7b5)
        3: 'maj7',   # III - Eb+maj7 (simplified)
        4: 'm7',     # iv - Fm7
        5: '7',      # V - G7
        6: 'maj7',   # VI - Abmaj7
        7: 'dim7'    # vii° - Bdim7
    }
}

# Complete data - ordered logically following Circle of Fifths
scales_data = {
    # Major scales (Complete Circle of Fifths)
    'C Major': ['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4'],
    'G Major': ['G4', 'A4', 'B4', 'C5', 'D5', 'E5', 'F#5'],
    'D Major': ['D4', 'E4', 'F#4', 'G4', 'A4', 'B4', 'C#5'],
    'A Major': ['A4', 'B4', 'C#5', 'D5', 'E5', 'F#5', 'G#5'],
    'E Major': ['E4', 'F#4', 'G#4', 'A4', 'B4', 'C#5', 'D#5'],
    'B Major': ['B4', 'C#5', 'D#5', 'E5', 'F#5', 'G#5', 'A#5'],
    'F# Major': ['F#4', 'G#4', 'A#4', 'B4', 'C#5', 'D#5', 'F5'],
    'C# Major': ['C#4', 'D#4', 'F4', 'F#4', 'G#4', 'A#4', 'C5'],
    'F Major': ['F4', 'G4', 'A4', 'Bb4', 'C5', 'D5', 'E5'],
    'Bb Major': ['Bb4', 'C5', 'D5', 'Eb5', 'F5', 'G5', 'A5'],
    'Eb Major': ['Eb4', 'F4', 'G4', 'Ab4', 'Bb4', 'C5', 'D5'],
    'Ab Major': ['Ab4', 'Bb4', 'C5', 'Db5', 'Eb5', 'F5', 'G5'],
    'Db Major': ['Db4', 'Eb4', 'F4', 'Gb4', 'Ab4', 'Bb4', 'C5'],

    # Natural Minor scales (Relative minors in Circle of Fifths order)
    'A Minor': ['A4', 'B4', 'C5', 'D5', 'E5', 'F5', 'G5'],
    'E Minor': ['E4', 'F#4', 'G4', 'A4', 'B4', 'C5', 'D5'],
    'B Minor': ['B4', 'C#5', 'D5', 'E5', 'F#5', 'G5', 'A5'],
    'F# Minor': ['F#4', 'G#4', 'A4', 'B4', 'C#5', 'D5', 'E5'],
    'C# Minor': ['C#4', 'D#4', 'E4', 'F#4', 'G#4', 'A4', 'B4'],
    'G# Minor': ['G#4', 'A#4', 'B4', 'C#5', 'D#5', 'E5', 'F#5'],
    'D# Minor': ['D#4', 'F4', 'F#4', 'G#4', 'A#4', 'B4', 'C#5'],
    'Bb Minor': ['Bb4', 'C5', 'Db5', 'Eb5', 'F5', 'Gb5', 'Ab5'],
    'F Minor': ['F4', 'G4', 'Ab4', 'Bb4', 'C5', 'Db5', 'Eb5'],
    'C Minor': ['C4', 'D4', 'Eb4', 'F4', 'G4', 'Ab4', 'Bb4'],
    'G Minor': ['G4', 'A4', 'Bb4', 'C5', 'D5', 'Eb5', 'F5'],
    'D Minor': ['D4', 'E4', 'F4', 'G4', 'A4', 'Bb4', 'C5'],

    # Harmonic Minor scales (Circle of Fifths order)
    'A Harmonic Minor': ['A4', 'B4', 'C5', 'D5', 'E5', 'F5', 'G#5'],
    'E Harmonic Minor': ['E4', 'F#4', 'G4', 'A4', 'B4', 'C5', 'D#5'],
    'B Harmonic Minor': ['B4', 'C#5', 'D5', 'E5', 'F#5', 'G5', 'A#5'],
    'F# Harmonic Minor': ['F#4', 'G#4', 'A4', 'B4', 'C#5', 'D5', 'F5'],
    'C# Harmonic Minor': ['C#4', 'D#4', 'E4', 'F#4', 'G#4', 'A4', 'C5'],
    'G# Harmonic Minor': ['G#4', 'A#4', 'B4', 'C#5', 'D#5', 'E5', 'G5'],
    'Eb Harmonic Minor': ['Eb4', 'F4', 'Gb4', 'Ab4', 'Bb4', 'Cb5', 'D5'],
    'Bb Harmonic Minor': ['Bb4', 'C5', 'Db5', 'Eb5', 'F5', 'Gb5', 'A5'],
    'F Harmonic Minor': ['F4', 'G4', 'Ab4', 'Bb4', 'C5', 'Db5', 'E5'],

    # Melodic Minor scales (ascending, Circle of Fifths order)
    'A Melodic Minor': ['A4', 'B4', 'C5', 'D5', 'E5', 'F#5', 'G#5'],
    'E Melodic Minor': ['E4', 'F#4', 'G4', 'A4', 'B4', 'C#5', 'D#5'],
    'B Melodic Minor': ['B4', 'C#5', 'D5', 'E5', 'F#5', 'G#5', 'A#5'],
    'F# Melodic Minor': ['F#4', 'G#4', 'A4', 'B4', 'C#5', 'D#5', 'F5'],
    'C# Melodic Minor': ['C#4', 'D#4', 'E4', 'F#4', 'G#4', 'A#4', 'C5'],
    'G# Melodic Minor': ['G#4', 'A#4', 'B4', 'C#5', 'D#5', 'F5', 'G5'],
    'Eb Melodic Minor': ['Eb4', 'F4', 'Gb4', 'Ab4', 'Bb4', 'C5', 'D5'],
    'Bb Melodic Minor': ['Bb4', 'C5', 'Db5', 'Eb5', 'F5', 'G5', 'A5'],
    'F Melodic Minor': ['F4', 'G4', 'Ab4', 'Bb4', 'C5', 'D5', 'E5'],

    # Modal scales (Church modes) - organized by root following Circle of Fifths
    'C Ionian': ['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4'],
    'G Mixolydian': ['G4', 'A4', 'B4', 'C5', 'D5', 'E5', 'F5'],
    'D Dorian': ['D4', 'E4', 'F4', 'G4', 'A4', 'B4', 'C5'],
    'A Aeolian': ['A4', 'B4', 'C5', 'D5', 'E5', 'F5', 'G5'],
    'E Phrygian': ['E4', 'F4', 'G4', 'A4', 'B4', 'C5', 'D5'],
    'B Locrian': ['B4', 'C5', 'D5', 'E5', 'F5', 'G5', 'A5'],
    'F Lydian': ['F4', 'G4', 'A4', 'B4', 'C5', 'D5', 'E5'],
    'Bb Dorian': ['Bb4', 'C5', 'Db5', 'Eb5', 'F5', 'Gb5', 'Ab5'],
    'F Dorian': ['F4', 'G4', 'Ab4', 'Bb4', 'C5', 'Db5', 'Eb5'],
    'C Dorian': ['C4', 'D4', 'Eb4', 'F4', 'G4', 'Ab4', 'Bb4'],
    'G Dorian': ['G4', 'A4', 'Bb4', 'C5', 'D5', 'Eb5', 'F5'],
    'D Mixolydian': ['D4', 'E4', 'F#4', 'G4', 'A4', 'B4', 'C5'],

    # Pentatonic scales (organized by root following Circle of Fifths)
    'C Major Pentatonic': ['C4', 'D4', 'E4', 'G4', 'A4'],
    'G Major Pentatonic': ['G4', 'A4', 'B4', 'D5', 'E5'],
    'D Major Pentatonic': ['D4', 'E4', 'F#4', 'A4', 'B4'],
    'A Major Pentatonic': ['A4', 'B4', 'C#5', 'E5', 'F#5'],
    'E Major Pentatonic': ['E4', 'F#4', 'G#4', 'B4', 'C#5'],
    'B Major Pentatonic': ['B4', 'C#5', 'D#5', 'F#5', 'G#5'],
    'F# Major Pentatonic': ['F#4', 'G#4', 'A#4', 'C#5', 'D#5'],
    'F Major Pentatonic': ['F4', 'G4', 'A4', 'C5', 'D5'],
    'Bb Major Pentatonic': ['Bb4', 'C5', 'D5', 'F5', 'G5'],
    'Eb Major Pentatonic': ['Eb4', 'F4', 'G4', 'Bb4', 'C5'],
    'Ab Major Pentatonic': ['Ab4', 'Bb4', 'C5', 'Eb5', 'F5'],

    # Blues scales (organized by root)
    'C Blues': ['C4', 'Eb4', 'F4', 'F#4', 'G4', 'Bb4'],
    'G Blues': ['G4', 'Bb4', 'C5', 'C#5', 'D5', 'F5'],
    'D Blues': ['D4', 'F4', 'G4', 'Ab4', 'A4', 'C5'],
    'A Blues': ['A4', 'C5', 'D5', 'D#5', 'E5', 'G5'],
    'E Blues': ['E4', 'G4', 'A4', 'A#4', 'B4', 'D5'],
    'B Blues': ['B4', 'D5', 'E5', 'F5', 'F#5', 'A5'],
    'F Blues': ['F4', 'Ab4', 'Bb4', 'B4', 'C5', 'Eb5'],
    'Bb Blues': ['Bb4', 'Db5', 'Eb5', 'E5', 'F5', 'Ab5'],

    # Other common scales
}

# Ordered list of scales for the menu (Circle of Fifths order)
# Scale selection menus - separated for better UX
scale_roots = [
    'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'
]

scale_types = [
    # Basic scales
    'Major', 'Minor', 'Harmonic Minor', 'Melodic Minor',

    # Modal scales
    'Ionian', 'Dorian', 'Phrygian', 'Lydian', 'Mixolydian', 'Aeolian', 'Locrian',

    # Pentatonic scales
    'Major Pentatonic', 'Minor Pentatonic',

    # Blues scales
    'Blues',

    # Other scales
    'Whole Tone', 'Diminished', 'Augmented'
]

# Legacy menu for backward compatibility (kept for any external references)
scales_menu_order = [
    # Major scales (Complete Circle of Fifths)
    'C Major', 'G Major', 'D Major', 'A Major', 'E Major', 'B Major', 'F# Major', 'C# Major',
    'F Major', 'Bb Major', 'Eb Major', 'Ab Major', 'Db Major',

    # Natural Minor scales (Relative minors in same order)
    'A Minor', 'E Minor', 'B Minor', 'F# Minor', 'C# Minor', 'G# Minor', 'D# Minor', 'Bb Minor',
    'F Minor', 'C Minor', 'G Minor', 'D Minor',

    # Harmonic Minor scales
    'A Harmonic Minor', 'E Harmonic Minor', 'B Harmonic Minor', 'F# Harmonic Minor', 'C# Harmonic Minor',
    'G# Harmonic Minor', 'Eb Harmonic Minor', 'Bb Harmonic Minor', 'F Harmonic Minor',

    # Melodic Minor scales
    'A Melodic Minor', 'E Melodic Minor', 'B Melodic Minor', 'F# Melodic Minor', 'C# Melodic Minor',
    'G# Melodic Minor', 'Eb Melodic Minor', 'Bb Melodic Minor', 'F Melodic Minor',

    # Modal scales (organized by root following Circle of Fifths)
    'C Ionian', 'G Mixolydian', 'D Dorian', 'A Aeolian', 'E Phrygian', 'B Locrian', 'F Lydian',
    'Bb Dorian', 'F Dorian', 'C Dorian', 'G Dorian', 'D Mixolydian',

    # Pentatonic scales (organized by root)
    'C Major Pentatonic', 'G Major Pentatonic', 'D Major Pentatonic', 'A Major Pentatonic',
    'E Major Pentatonic', 'B Major Pentatonic', 'F# Major Pentatonic', 'F Major Pentatonic',
    'Bb Major Pentatonic', 'Eb Major Pentatonic', 'Ab Major Pentatonic',

    # Blues scales
    'C Blues', 'G Blues', 'D Blues', 'A Blues', 'E Blues', 'B Blues', 'F Blues', 'Bb Blues',

    # Other scales
    'C Whole Tone', 'C Diminished', 'C Augmented'
]

# Chord selection menus - separated for better UX
chord_roots = [
    'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'
]

chord_types = [
    # Basic triads
    'Major', 'Minor', 'Diminished', 'Augmented',

    # Seventh chords
    '7', 'maj7', 'm7', 'dim7', 'm7b5', 'maj7b5', '7sus4', '7b9',

    # Extended chords
    '9', 'm9', 'maj9', '11', 'm11', 'maj11', '13', 'm13', 'maj13',

    # Added tone chords
    '6', 'm6', '6/9', '7#11',

    # Suspended chords
    'sus2', 'sus4',

    # Quartal and quintal
    'Quartal', 'Quintal',

    # Power chords
    '5'
]

# Legacy menu for backward compatibility (kept for any external references)
chords_menu_order = [
    # TRIADS (Circle of Fifths order)
    'C Major', 'C Minor', 'C Diminished', 'C Augmented', 'A Minor', 'A Diminished',
    'G Major', 'G Minor', 'E Minor', 'E Diminished',
    'D Major', 'D Minor', 'D Diminished', 'B Minor', 'B Diminished',
    'A Major', 'F# Minor',
    'E Major', 'C# Minor',
    'B Major', 'G# Minor',
    'F Major', 'F Minor', 'D Minor',
    'Bb Major', 'Bb Minor', 'G Minor',
    'Eb Major', 'Eb Minor', 'C Minor',
    'Ab Major', 'Ab Minor', 'F Minor',
    'Db Major', 'Db Minor', 'Bb Minor',

    # SEVENTH CHORDS
    # Dominant 7ths
    'C7', 'D7', 'E7', 'G7', 'A7', 'B7', 'F7', 'Bb7', 'Eb7', 'Ab7', 'Db7',
    # Major 7ths
    'Cmaj7', 'Dmaj7', 'Emaj7', 'Gmaj7', 'Amaj7', 'Bmaj7', 'Fmaj7', 'Bbmaj7', 'Ebmaj7', 'Abmaj7', 'Dbmaj7',
    # Minor 7ths
    'Cm7', 'Dm7', 'Em7', 'Gm7', 'Am7', 'Bm7', 'Fm7', 'Bbm7', 'Ebm7', 'Abm7', 'Dbm7',
    # Diminished 7ths
    'Cdim7', 'C#dim7', 'Ddim7', 'D#dim7', 'Edim7', 'Fdim7', 'F#dim7', 'Gdim7', 'G#dim7', 'Adim7', 'A#dim7', 'Bdim7',

    # EXTENDED CHORDS
    # 9ths
    'C9', 'Cm9', 'Cmaj9', 'D9', 'Dm9', 'Dmaj9', 'E9', 'Em9', 'Emaj9',
    'G9', 'Gm9', 'Gmaj9', 'A9', 'Am9', 'Amaj9', 'B9', 'Bm9', 'Bmaj9',

    # ADDED TONE CHORDS
    # 6ths
    'C6', 'Cm6', 'D6', 'Dm6', 'E6', 'Em6', 'G6', 'Gm6', 'A6', 'Am6', 'B6', 'Bm6',
    # 6/9 chords
    'C6/9', 'Cm6/9', 'D6/9', 'G6/9', 'A6/9',
    # 7#11 chords
    'C7#11', 'D7#11', 'G7#11', 'A7#11',

    # SPECIAL CHORDS
    # Suspended chords
    'Csus2', 'Csus4', 'Dsus2', 'Dsus4', 'Esus2', 'Esus4', 'Gsus2', 'Gsus4', 'Asus2', 'Asus4', 'Bsus2', 'Bsus4',
    # Quartal harmonies
    'C Quartal', 'D Quartal', 'E Quartal', 'F Quartal', 'G Quartal', 'A Quartal',
    # Quintal harmonies
    'C Quintal', 'D Quintal', 'E Quintal', 'F Quintal', 'G Quintal', 'A Quintal',
    # Power chords
    'C5', 'D5', 'E5', 'F5', 'G5', 'A5', 'B5'
]

# Generate complete chord database dynamically
chords_data = generate_all_chords()

# Common chord progressions
progressions_data = {
    'I-IV-V-I': ['C Major', 'F Major', 'G Major', 'C Major'],
    'ii-V-I': ['D Minor', 'G Dominant 7', 'C Major'],
    'I-vi-IV-V': ['C Major', 'A Minor', 'F Major', 'G Major'],
    'I-V-vi-IV': ['C Major', 'G Major', 'A Minor', 'F Major'],
    'vi-IV-I-V': ['A Minor', 'F Major', 'C Major', 'G Major'],
    'Blues I-IV-V': ['C Major', 'F Major', 'G Major'],
    'Jazz ii-V-I': ['D Minor 7', 'G Dominant 7', 'C Major 7'],
    'Classical I-VI-IV-V': ['C Major', 'A Minor', 'F Major', 'G Major'],
    'Pop I-VI-III-VII': ['C Major', 'A Minor', 'E Minor', 'B Diminished'],
    'Rock I-bVII-IV': ['C Major', 'Bb Major', 'F Major']
}

# Main Application
# Main Application
class MusicTheoryApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configure window with modern styling
        self.geometry("1200x800")
        self.minsize(1000, 700)

        # Modern window styling
        self.configure(fg_color=COLORS['bg_surface'])
        self.title("🎸 Music Theory Engine - Professional Edition")

        # Set window icon (if available)
        try:
            self.iconbitmap("music_icon.ico")
        except:
            pass

        # Initialize tooltip system
        self.current_tooltip = None
        self.tooltip_window = None
        pass  # Icon optional

        # Data
        self.current_scale = None
        self.current_chord = None
        self.current_progression = None
        self.custom_progression = []

        # Audio system
        self.audio_player = audio_player

        # MIDI system
        self.midi_manager = midi_manager
        self.midi_enabled = MIDI_AVAILABLE

        # Presets data
        self.presets = {
            'scales': {},
            'chords': {},
            'progressions': {}
        }

        # Metronome data
        self.metronome_running = False
        self.metronome_bpm = 120
        self.metronome_thread = None
        self.tap_times = []
        
        # Scale position tracking
        self.current_scale_position = 0

        # Setup UI
        self.setup_ui()

        # Welcome message
        self.show_welcome()

    def create_tooltip(self, widget, text):
        """Create a tooltip for a widget"""
        def show_tooltip(event):
            if self.tooltip_window:
                self.hide_tooltip()

            # Create tooltip window
            self.tooltip_window = ctk.CTkToplevel(self)
            self.tooltip_window.overrideredirect(True)
            self.tooltip_window.attributes('-topmost', True)
            self.tooltip_window.configure(fg_color=COLORS['text_primary'])

            # Tooltip label
            label = ctk.CTkLabel(
                self.tooltip_window,
                text=text,
                font=ctk.CTkFont(size=10),
                fg_color=COLORS['text_primary'],
                text_color=COLORS['background'],
                corner_radius=4
            )
            label.pack(padx=8, pady=4)

            # Position tooltip near mouse
            x = event.x_root + 10
            y = event.y_root + 10
            self.tooltip_window.geometry(f"+{x}+{y}")

        def hide_tooltip(event=None):
            if self.tooltip_window:
                self.tooltip_window.destroy()
                self.tooltip_window = None

        # Bind events
        widget.bind("<Enter>", show_tooltip)
        widget.bind("<Leave>", hide_tooltip)
        widget.bind("<Button-1>", hide_tooltip)  # Hide on click

    def setup_ui(self):
        """Setup the modern user interface"""
        # Main container with improved styling
        self.main_frame = ctk.CTkFrame(self, fg_color=COLORS['bg_surface'])
        self.main_frame.pack(fill="both", expand=True, padx=25, pady=25)

        # Modern header section
        header_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color=["#6366F1", "#8B5CF6"],  # Beautiful gradient
            height=90,
            corner_radius=15
        )
        header_frame.pack(fill="x", pady=(0, 25))
        header_frame.pack_propagate(False)

        # Header content
        header_content = ctk.CTkFrame(header_frame, fg_color="transparent")
        header_content.pack(expand=True, fill="both", padx=25, pady=15)

        # Left side - Logo and title
        left_section = ctk.CTkFrame(header_content, fg_color="transparent")
        left_section.pack(side="left")

        # Modern logo with gradient background
        logo_container = ctk.CTkFrame(
            left_section,
            fg_color=["#10B981", "#059669"],  # Green gradient
            width=60,
            height=60,
            corner_radius=30
        )
        logo_container.pack(side="left", padx=(0, 20))
        logo_container.pack_propagate(False)

        logo_label = ctk.CTkLabel(
            logo_container,
            text="🎸",
            font=ctk.CTkFont(size=28),
            text_color="white"
        )
        logo_label.place(relx=0.5, rely=0.5, anchor="center")

        # Title and subtitle
        title_section = ctk.CTkFrame(left_section, fg_color="transparent")
        title_section.pack(side="left")

        title_label = ctk.CTkLabel(
            title_section,
            text="Music Theory Engine",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="white"
        )
        title_label.pack(anchor="w")

        subtitle_label = ctk.CTkLabel(
            title_section,
            text="Professional Guitar Learning Companion • v2.0",
            font=ctk.CTkFont(size=11),
            text_color="#E8E8E8"
        )
        subtitle_label.pack(anchor="w")

        # Right side - Audio status
        right_section = ctk.CTkFrame(header_content, fg_color="transparent")
        right_section.pack(side="right")

        # Audio status with modern styling
        audio_frame = ctk.CTkFrame(
            right_section,
            fg_color=COLORS['surface_hover'],
            corner_radius=10
        )
        audio_frame.pack(pady=5)

        audio_label = ctk.CTkLabel(
            audio_frame,
            text="🔊 Audio: Windows Beeps",
            font=ctk.CTkFont(size=11),
            text_color="#E8E8E8"
        )
        audio_label.pack(side="left", padx=15, pady=8)

        status_indicator = ctk.CTkLabel(
            audio_frame,
            text="●",
            font=ctk.CTkFont(size=12),
            text_color="#10B981"  # Green for active
        )
        status_indicator.pack(side="left", padx=(0, 15))

        # Tab view with improved sizing
        self.tabview = ctk.CTkTabview(
            self.main_frame,
            width=1100,
            height=650,
            fg_color=COLORS['bg_surface'],
            segmented_button_fg_color=COLORS['bg_elevated'],
            segmented_button_selected_color=COLORS['primary'],
            segmented_button_selected_hover_color=COLORS['hover_primary']
        )
        self.tabview.pack(pady=(15, 25))

        # Create tabs
        self.tabview.add("Scale Explorer")
        self.tabview.add("Chord Builder")
        self.tabview.add("Progression Analyzer")
        self.tabview.add("Metronome")
        self.tabview.add("Fretboard Viewer")
        self.tabview.add("🎯 Theory Exercises")

        # Setup tab contents
        self.setup_scale_explorer()
        self.setup_chord_builder()
        self.setup_progression_analyzer()
        self.setup_metronome()
        self.setup_fretboard_viewer()
        self.setup_exercises()
        self.setup_exercises()

        # Load default scale after all components are initialized
        self.update_current_scale()

    def setup_scale_explorer(self):
        """Setup the scale explorer tab"""
        tab = self.tabview.tab("Scale Explorer")

        # Modern title section with improved layout
        title_frame = ctk.CTkFrame(tab, fg_color="transparent", height=80)
        title_frame.pack(fill="x", pady=(25, 20))
        title_frame.pack_propagate(False)

        # Left side - Icon and title
        title_left = ctk.CTkFrame(title_frame, fg_color="transparent")
        title_left.pack(side="left", padx=(25, 0))

        # Icon with modern styling
        icon_bg = ctk.CTkFrame(
            title_left,
            fg_color=COLORS['music_blue'],
            width=50,
            height=50,
            corner_radius=25
        )
        icon_bg.pack(side="left", padx=(0, 15))
        icon_bg.pack_propagate(False)

        title_icon = ctk.CTkLabel(
            icon_bg,
            text="🎼",
            font=ctk.CTkFont(size=24),
            text_color="white"
        )
        title_icon.place(relx=0.5, rely=0.5, anchor="center")

        # Title and subtitle
        title_text_frame = ctk.CTkFrame(title_left, fg_color="transparent")
        title_text_frame.pack(side="left")

        title = ctk.CTkLabel(
            title_text_frame,
            text="Scale Explorer",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=COLORS['text_primary']
        )
        title.pack(anchor="w")

        subtitle = ctk.CTkLabel(
            tab,
            text="Esplora scale, posizioni e patterns sul manico",
            font=ctk.CTkFont(size=12),
            text_color=COLORS['neutral']
        )
        subtitle.pack(pady=(0, 20))

        # Controls with modern styling
        controls_frame = ctk.CTkFrame(
            tab,
            corner_radius=STYLES['corner_radius'],
            border_width=1,
            border_color=COLORS['neutral_light']
        )
        controls_frame.pack(fill="x", padx=20, pady=(0, 20))

        # Scale selection with improved spacing
        scale_section = ctk.CTkFrame(controls_frame, fg_color="transparent")
        scale_section.pack(side="left", padx=(20, 15), pady=15)

        scale_label = ctk.CTkLabel(
            scale_section,
            text="🎼 Scale:",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=COLORS['text_primary']
        )
        scale_label.pack(anchor="w", pady=(0, 5))

        # Root note selection
        self.scale_root_var = ctk.StringVar(value="C")
        root_menu = ctk.CTkOptionMenu(
            scale_section,
            values=scale_roots,
            variable=self.scale_root_var,
            command=self.on_scale_root_change,
            width=80
        )
        root_menu.pack(side="left", padx=(0, 10))

        # Scale type selection
        self.scale_type_var = ctk.StringVar(value="Major")
        type_menu = ctk.CTkOptionMenu(
            scale_section,
            values=scale_types,
            variable=self.scale_type_var,
            command=self.on_scale_type_change,
            width=140
        )
        type_menu.pack(side="left", padx=(0, 10))

        # Combined scale name (for backward compatibility)
        self.scale_var = ctk.StringVar(value="C Major")

        # Transpose buttons
        transpose_down = ctk.CTkButton(
            controls_frame,
            text="⬇️",
            command=lambda: self.transpose_scale(-1),
            width=40,
            fg_color="#8B4513"
        )
        transpose_down.pack(side="right", padx=(0, 5))
        self.create_tooltip(transpose_down, TOOLTIPS['transpose_down'])

        transpose_label = ctk.CTkLabel(controls_frame, text="Transpose")
        transpose_label.pack(side="right", padx=(0, 5))

        transpose_up = ctk.CTkButton(
            controls_frame,
            text="⬆️",
            command=lambda: self.transpose_scale(1),
            width=40,
            fg_color="#8B4513"
        )
        transpose_up.pack(side="right", padx=(0, 10))
        self.create_tooltip(transpose_up, TOOLTIPS['transpose_up'])

        # Relative scale button
        relative_btn = ctk.CTkButton(
            controls_frame,
            text="Relative",
            command=self.show_relative_scale,
            fg_color=COLORS['accent']
        )
        relative_btn.pack(side="right", padx=(0, 10))
        self.create_tooltip(relative_btn, TOOLTIPS['relative_scale'])

        # Save to favorites button
        save_fav_btn = ctk.CTkButton(
            controls_frame,
            text="💾 Save",
            command=self.save_scale_favorite,
            fg_color=COLORS['secondary'],
            width=60
        )
        save_fav_btn.pack(side="right", padx=(0, 10))
        self.create_tooltip(save_fav_btn, TOOLTIPS['save_scale'])

        # Show patterns button
        patterns_btn = ctk.CTkButton(
            controls_frame,
            text="🎸 Patterns",
            command=self.show_scale_patterns,
            fg_color=COLORS['accent'],
            hover_color=COLORS['accent_hover'],
            border_width=STYLES['border_width'],
            corner_radius=STYLES['corner_radius'],
            font=ctk.CTkFont(size=11, weight="bold"),
            height=35,
            width=100
        )
        patterns_btn.pack(side="right", padx=(0, 10))
        self.create_tooltip(patterns_btn, TOOLTIPS['scale_patterns'])

        # Show positions button
        positions_btn = ctk.CTkButton(
            controls_frame,
            text="📍 Positions",
            command=self.show_scale_positions,
            fg_color=COLORS['secondary'],
            hover_color=COLORS['secondary_hover'],
            border_width=STYLES['border_width'],
            corner_radius=STYLES['corner_radius'],
            font=ctk.CTkFont(size=11, weight="bold"),
            height=35,
            width=100
        )
        positions_btn.pack(side="right", padx=(0, 10))
        self.create_tooltip(positions_btn, TOOLTIPS['scale_positions'])

        # Playback mode selector
        self.playback_mode_var = ctk.StringVar(value="Ascending")
        playback_menu = ctk.CTkOptionMenu(
            controls_frame,
            values=["Ascending", "Descending", "Ascending + Descending", "Arpeggio"],
            variable=self.playback_mode_var,
            width=120
        )
        playback_menu.pack(side="right", padx=(0, 10))

        # Play button - modern gradient styling
        play_btn = ctk.CTkButton(
            controls_frame,
            text="🎵 Play Scale",
            command=self.play_current_scale,
            fg_color=COLORS['button_primary_start'],
            hover_color=COLORS['primary_hover'],
            border_width=STYLES['border_width'],
            corner_radius=STYLES['corner_radius'],
            font=ctk.CTkFont(size=12, weight="bold"),
            height=40,
            width=130
        )
        play_btn.pack(side="right", padx=(0, 10))
        self.create_tooltip(play_btn, TOOLTIPS['play_scale'])

        # Info display
        self.scale_info = ctk.CTkLabel(tab, text="", font=ctk.CTkFont(size=14))
        self.scale_info.pack(pady=(10, 20))

        # Harmonization section with modern styling
        harmonization_title = ctk.CTkLabel(
            tab,
            text="🎼 Harmonized Chords",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=COLORS['secondary']
        )
        harmonization_title.pack(pady=(20, 10))

        harmonization_subtitle = ctk.CTkLabel(
            tab,
            text="Accordi generati automaticamente dalla scala selezionata",
            font=ctk.CTkFont(size=11),
            text_color=COLORS['neutral_light']
        )
        harmonization_subtitle.pack(pady=(0, 15))

        self.harmonization_frame = ctk.CTkFrame(
            tab,
            corner_radius=STYLES['corner_radius'],
            border_width=1,
            border_color=COLORS['neutral_light']
        )
        self.harmonization_frame.pack(fill="x", padx=20, pady=(0, 20))

        # Favorites section with modern styling
        favorites_title = ctk.CTkLabel(
            tab,
            text="⭐ Favorite Scales",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=COLORS['warning']
        )
        favorites_title.pack(pady=(20, 10))

        favorites_subtitle = ctk.CTkLabel(
            tab,
            text="Le tue scale preferite salvate per accesso rapido",
            font=ctk.CTkFont(size=11),
            text_color=COLORS['neutral_light']
        )
        favorites_subtitle.pack(pady=(0, 15))

        self.favorites_frame = ctk.CTkFrame(
            tab,
            corner_radius=STYLES['corner_radius'],
            border_width=1,
            border_color=COLORS['neutral_light']
        )
        self.favorites_frame.pack(fill="x", padx=20, pady=(0, 20))

        self.update_favorites_display()

        # Load default scale (deferred to end of initialization)
        # self.update_current_scale()  # Called at the end of __init__

    def setup_chord_builder(self):
        """Setup the chord builder tab"""
        tab = self.tabview.tab("Chord Builder")

        # Modern title section
        title_frame = ctk.CTkFrame(tab, fg_color="transparent", height=80)
        title_frame.pack(fill="x", pady=(25, 20))
        title_frame.pack_propagate(False)

        title_left = ctk.CTkFrame(title_frame, fg_color="transparent")
        title_left.pack(side="left", padx=(25, 0))

        # Purple icon for chords
        icon_bg = ctk.CTkFrame(
            title_left,
            fg_color=COLORS['music_purple'],
            width=50,
            height=50,
            corner_radius=25
        )
        icon_bg.pack(side="left", padx=(0, 15))
        icon_bg.pack_propagate(False)

        title_icon = ctk.CTkLabel(
            icon_bg,
            text="🎸",
            font=ctk.CTkFont(size=24),
            text_color="white"
        )
        title_icon.place(relx=0.5, rely=0.5, anchor="center")

        title_text_frame = ctk.CTkFrame(title_left, fg_color="transparent")
        title_text_frame.pack(side="left")

        title = ctk.CTkLabel(
            title_text_frame,
            text="Chord Builder",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=COLORS['text_primary']
        )
        title.pack(anchor="w")

        subtitle = ctk.CTkLabel(
            tab,
            text="Costruisci accordi e visualizzali sul fretboard",
            font=ctk.CTkFont(size=12),
            text_color=COLORS['neutral']
        )
        subtitle.pack(pady=(0, 20))

        # Modern controls section
        controls_frame = ctk.CTkFrame(
            tab,
            fg_color=COLORS['bg_elevated'],
            corner_radius=12
        )
        controls_frame.pack(fill="x", padx=25, pady=(0, 25))

        # Chord selection with separate menus
        # Root note selection
        self.chord_root_var = ctk.StringVar(value="C")
        root_menu = ctk.CTkOptionMenu(
            controls_frame,
            values=chord_roots,
            variable=self.chord_root_var,
            command=self.on_chord_root_change,
            width=80
        )
        root_menu.pack(side="left", padx=(10, 5))

        # Chord type selection
        self.chord_type_var = ctk.StringVar(value="Major")
        type_menu = ctk.CTkOptionMenu(
            controls_frame,
            values=chord_types,
            variable=self.chord_type_var,
            command=self.on_chord_type_change,
            width=120
        )
        type_menu.pack(side="left", padx=(0, 20))

        # Combined chord name (for backward compatibility)
        self.chord_var = ctk.StringVar(value="C Major")

        # Transpose buttons
        transpose_down = ctk.CTkButton(
            controls_frame,
            text="⬇️",
            command=lambda: self.transpose_chord(-1),
            width=40,
            fg_color="#8B4513"
        )
        transpose_down.pack(side="right", padx=(0, 5))

        transpose_label = ctk.CTkLabel(controls_frame, text="Transpose")
        transpose_label.pack(side="right", padx=(0, 5))

        transpose_up = ctk.CTkButton(
            controls_frame,
            text="⬆️",
            command=lambda: self.transpose_chord(1),
            width=40,
            fg_color="#8B4513"
        )
        transpose_up.pack(side="right", padx=(0, 10))

        # Play button
        play_btn = ctk.CTkButton(
            controls_frame,
            text="🎵 Play Chord",
            command=self.play_current_chord,
            fg_color="#4CAF50"
        )
        play_btn.pack(side="right", padx=(0, 10))

        # Info display
        self.chord_info = ctk.CTkLabel(tab, text="", font=ctk.CTkFont(size=14))
        self.chord_info.pack(pady=(10, 20))

        # Load default chord
        self.update_current_chord()

    def on_chord_root_change(self, root):
        """Handle root note selection for chords"""
        self.update_current_chord()

    def on_chord_type_change(self, chord_type):
        """Handle chord type selection"""
        self.update_current_chord()

    def update_current_chord(self):
        """Update the current chord based on root and type selection"""
        root = self.chord_root_var.get()
        chord_type = self.chord_type_var.get()
        chord_name = f"{root}{chord_type}" if chord_type in ['7', 'maj7', 'm7', 'dim7', '9', 'm9', 'maj9', '6', 'm6', 'sus2', 'sus4', '5'] else f"{root} {chord_type}"

        # Update the combined chord variable for compatibility
        self.chord_var.set(chord_name)

        # Try to create chord from database first
        if chord_name in chords_data:
            notes = chords_data[chord_name]
            self.current_chord = Chord(root, chord_type, notes)
            self.update_chord_display()
        else:
            # Try to create chord dynamically using standard chord types
            try:
                # Map chord type to standard format
                type_mapping = {
                    'Major': 'maj',
                    'Minor': 'min',
                    'Diminished': 'dim',
                    'Augmented': 'aug',
                    '7': '7',
                    'maj7': 'maj7',
                    'm7': 'm7',
                    'dim7': 'dim7',
                    'm7b5': 'm7b5',
                    'maj7b5': 'maj7b5',
                    '7sus4': '7sus4',
                    '7b9': '7b9',
                    '9': '9',
                    'm9': 'm9',
                    'maj9': 'maj9',
                    '11': '11',
                    'm11': 'm11',
                    'maj11': 'maj11',
                    '13': '13',
                    'm13': 'm13',
                    'maj13': 'maj13',
                    '6': '6',
                    'm6': 'm6',
                    '6/9': '6/9',
                    '7#11': '7#11',
                    'sus2': 'sus2',
                    'sus4': 'sus4',
                    'Quartal': 'quartal',
                    'Quintal': 'quintal',
                    '5': '5'
                }

                standard_type = type_mapping.get(chord_type, chord_type.lower())

                # Try alternative naming (without space)
                alt_chord_name = f"{root}{standard_type}"
                if alt_chord_name in chords_data:
                    notes = chords_data[alt_chord_name]
                    self.current_chord = Chord(root, standard_type, notes)
                else:
                    # Create chord using standard intervals
                    self.current_chord = Chord(root, standard_type)

                self.update_chord_display()

            except Exception as e:
                print(f"Could not create chord {chord_name}: {e}")
                # Fallback to C Major
                self.chord_root_var.set("C")
                self.chord_type_var.set("Major")
                self.update_current_chord()

    def update_chord_display(self):
        """Update the chord information display"""
        if self.current_chord:
            if hasattr(self, 'chord_info'):
                # Handle root as both Note object and string
                if hasattr(self.current_chord.root, 'name'):
                    root_name = self.current_chord.root.name
                else:
                    root_name = str(self.current_chord.root)

                chord_name = f"{root_name}{self.current_chord.quality}"

                # Handle both Note objects and strings in notes
                if self.current_chord.notes and len(self.current_chord.notes) > 0:
                    if hasattr(self.current_chord.notes[0], 'name'):
                        # Note objects
                        notes_str = " ".join([note.name for note in self.current_chord.notes])
                    else:
                        # String notes
                        notes_str = " ".join(self.current_chord.notes)
                else:
                    notes_str = "No notes"
                self.chord_info.configure(text=f"Chord: {chord_name} - Notes: {notes_str}")

    def setup_progression_analyzer(self):
        """Setup the progression analyzer tab"""
        tab = self.tabview.tab("Progression Analyzer")

        # Title
        title = ctk.CTkLabel(tab, text="Chord Progression Analyzer", font=ctk.CTkFont(size=18, weight="bold"))
        title.pack(pady=(20, 10))

        # Custom progression builder section
        builder_title = ctk.CTkLabel(
            tab,
            text="🎼 Build Your Progression",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        builder_title.pack(pady=(20, 10))

        # Drag & drop zone
        drop_frame = ctk.CTkFrame(tab, height=80)
        drop_frame.pack(fill="x", padx=20, pady=(0, 20))

        drop_title = ctk.CTkLabel(
            drop_frame,
            text="Drop Zone - Drag chords here to build progression",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        drop_title.pack(pady=(10, 5))

        self.progression_builder = ctk.CTkFrame(drop_frame, fg_color="#2B2B2B")
        self.progression_builder.pack(fill="x", padx=10, pady=(0, 10))

        # Initialize custom progression
        self.custom_progression = []

        # Controls for custom progression
        controls_frame = ctk.CTkFrame(tab)
        controls_frame.pack(fill="x", padx=20, pady=(0, 20))

        # Clear progression button
        clear_btn = ctk.CTkButton(
            controls_frame,
            text="🗑️ Clear",
            command=self.clear_custom_progression,
            fg_color="#DC143C",
            width=80
        )
        clear_btn.pack(side="left", padx=(10, 10))

        # Play custom progression button
        self.play_custom_btn = ctk.CTkButton(
            controls_frame,
            text="🎵 Play Progression",
            command=self.play_custom_progression,
            fg_color="#4CAF50",
            state="disabled"  # Initially disabled
        )
        self.play_custom_btn.pack(side="right", padx=(0, 10))

        # Analyze custom progression button
        self.analyze_custom_btn = ctk.CTkButton(
            controls_frame,
            text="📊 Analyze",
            command=self.analyze_custom_progression,
            fg_color="#FF8C00",
            state="disabled"  # Initially disabled
        )
        self.analyze_custom_btn.pack(side="right", padx=(0, 10))

        # Alternative: Common progressions section
        common_title = ctk.CTkLabel(
            tab,
            text="📚 Or Choose Common Progressions:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        common_title.pack(pady=(10, 5))

        common_frame = ctk.CTkFrame(tab)
        common_frame.pack(fill="x", padx=20, pady=(0, 20))

        self.progression_var = ctk.StringVar(value="I-IV-V-I")
        progression_menu = ctk.CTkOptionMenu(
            common_frame,
            values=list(progressions_data.keys()),
            variable=self.progression_var,
            command=self.on_progression_change
        )
        progression_menu.pack(side="left", padx=(10, 20))

        # Info display
        self.progression_info = ctk.CTkLabel(tab, text="", font=ctk.CTkFont(size=14))
        self.progression_info.pack(pady=(10, 20))

        # Compatible scales display
        scales_frame = ctk.CTkFrame(tab)
        scales_frame.pack(fill="x", padx=20, pady=(0, 20))

        scales_title = ctk.CTkLabel(scales_frame, text="Compatible Scales:", font=ctk.CTkFont(weight="bold"))
        scales_title.pack(anchor="w", padx=10, pady=(10, 5))

        self.compatible_scales = ctk.CTkLabel(scales_frame, text="", font=ctk.CTkFont(size=12))
        self.compatible_scales.pack(anchor="w", padx=10, pady=(0, 10))

        # Load default progression
        self.on_progression_change("I-IV-V-I")

    def setup_metronome(self):
        """Setup the metronome tab"""
        tab = self.tabview.tab("Metronome")

        # Title
        title = ctk.CTkLabel(tab, text="Metronome", font=ctk.CTkFont(size=18, weight="bold"))
        title.pack(pady=(20, 10))

        # BPM control
        bpm_frame = ctk.CTkFrame(tab)
        bpm_frame.pack(fill="x", padx=20, pady=(0, 20))

        bpm_label = ctk.CTkLabel(bpm_frame, text="BPM (Beats Per Minute):")
        bpm_label.pack(side="left", padx=(10, 10))

        # BPM slider
        self.bpm_slider = ctk.CTkSlider(
            bpm_frame,
            from_=60,
            to=200,
            number_of_steps=140,
            command=self.on_bpm_change
        )
        self.bpm_slider.set(120)
        self.bpm_slider.pack(side="left", padx=(0, 10), fill="x", expand=True)

        # BPM display
        self.bpm_display = ctk.CTkLabel(bpm_frame, text="120 BPM", width=80)
        self.bpm_display.pack(side="right", padx=(0, 10))

        # Control buttons
        controls_frame = ctk.CTkFrame(tab)
        controls_frame.pack(fill="x", padx=20, pady=(0, 20))

        # Start/Stop button
        self.metronome_btn = ctk.CTkButton(
            controls_frame,
            text="▶️ Start Metronome",
            command=self.toggle_metronome,
            fg_color="#4CAF50",
            width=150
        )
        self.metronome_btn.pack(side="left", padx=(10, 10))

        # Tap tempo button
        tap_btn = ctk.CTkButton(
            controls_frame,
            text="👆 Tap Tempo",
            command=self.tap_tempo,
            fg_color="#FF8C00",
            width=120
        )
        tap_btn.pack(side="left", padx=(0, 10))

        # Visual beat indicator
        self.beat_indicator = ctk.CTkLabel(
            tab,
            text="●",
            font=ctk.CTkFont(size=48),
            text_color="#666666"
        )
        self.beat_indicator.pack(pady=40)

        # Instructions
        instructions = ctk.CTkLabel(
            tab,
            text="🎵 Instructions:\n"
                 "• Adjust BPM with the slider\n"
                 "• Click 'Start Metronome' to begin\n"
                 "• Use 'Tap Tempo' to set BPM by tapping\n"
                 "• Visual indicator shows the beat",
            font=ctk.CTkFont(size=12),
            justify="left"
        )
        instructions.pack(pady=(20, 10))

        # Tap tempo data
        self.tap_times = []

    def setup_fretboard_viewer(self):
        """Setup the fretboard viewer tab"""
        tab = self.tabview.tab("Fretboard Viewer")

        # Title
        title = ctk.CTkLabel(tab, text="Guitar Fretboard", font=ctk.CTkFont(size=18, weight="bold"))
        title.pack(pady=(20, 10))

        # Controls
        controls_frame = ctk.CTkFrame(tab)
        controls_frame.pack(fill="x", padx=20, pady=(0, 10))

        # Update button
        update_btn = ctk.CTkButton(
            controls_frame,
            text="🔄 Update from Tabs",
            command=self.update_fretboard_from_tabs,
            fg_color="#4CAF50"
        )
        update_btn.pack(side="left", padx=(10, 10))

        # Clear button
        clear_btn = ctk.CTkButton(
            controls_frame,
            text="🧹 Clear",
            command=self.clear_fretboard,
            fg_color="#DC143C"
        )
        clear_btn.pack(side="left", padx=(0, 10))

        # Tuning selection
        tuning_label = ctk.CTkLabel(controls_frame, text="Tuning:")
        tuning_label.pack(side="left", padx=(20, 5))

        self.tuning_var = ctk.StringVar(value="Standard")
        tuning_menu = ctk.CTkOptionMenu(
            controls_frame,
            values=["Standard", "Drop D", "DADGAD"],
            variable=self.tuning_var,
            command=self.change_tuning
        )
        tuning_menu.pack(side="left", padx=(0, 10))

        # MIDI controls (only show if MIDI is available)
        if self.midi_enabled:
            midi_label = ctk.CTkLabel(controls_frame, text="MIDI:")
            midi_label.pack(side="left", padx=(20, 5))

            # MIDI enable checkbox
            self.midi_enabled_var = ctk.BooleanVar(value=True)  # MIDI is available, so enable by default
            midi_checkbox = ctk.CTkCheckBox(
                controls_frame,
                text="Enable",
                variable=self.midi_enabled_var,
                command=self.toggle_midi
            )
            midi_checkbox.pack(side="left", padx=(0, 10))

            # MIDI device selection
            if self.midi_manager.available_ports:
                self.midi_port_var = ctk.StringVar(value=self.midi_manager.available_ports[0] if self.midi_manager.available_ports else "None")
                midi_device_menu = ctk.CTkOptionMenu(
                    controls_frame,
                    values=self.midi_manager.available_ports if self.midi_manager.available_ports else ["None"],
                    variable=self.midi_port_var,
                    command=self.change_midi_port,
                    width=150
                )
                midi_device_menu.pack(side="left", padx=(0, 10))

            # MIDI velocity control
            velocity_label = ctk.CTkLabel(controls_frame, text="Velocity:")
            velocity_label.pack(side="left", padx=(10, 5))

            self.midi_velocity_var = ctk.IntVar(value=self.midi_manager.velocity)
            velocity_slider = ctk.CTkSlider(
                controls_frame,
                from_=1,
                to=127,
                variable=self.midi_velocity_var,
                command=self.change_midi_velocity,
                width=80
            )
            velocity_slider.pack(side="left", padx=(0, 10))

            velocity_value = ctk.CTkLabel(controls_frame, textvariable=self.midi_velocity_var, width=30)
            velocity_value.pack(side="left", padx=(0, 10))
        else:
            # Show MIDI unavailable message
            midi_info = ctk.CTkLabel(
                controls_frame,
                text="MIDI: Not Available (install 'mido': pip install mido)",
                text_color="orange"
            )
            midi_info.pack(side="left", padx=(20, 10))

            # Set default values for MIDI variables
            self.midi_enabled_var = ctk.BooleanVar(value=False)

        # Main container for fretboard and piano
        instruments_frame = ctk.CTkFrame(tab)
        instruments_frame.pack(fill="both", expand=True, padx=20, pady=(10, 10))

        # Fretboard section
        fretboard_section = ctk.CTkFrame(instruments_frame)
        fretboard_section.pack(side="left", fill="both", expand=True, padx=(0, 10))

        fretboard_title = ctk.CTkLabel(
            fretboard_section,
            text="🎸 Guitar Fretboard",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        fretboard_title.pack(pady=(10, 5))

        self.fretboard_frame = ctk.CTkScrollableFrame(fretboard_section, height=280)
        self.fretboard_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # Piano section
        piano_section = ctk.CTkFrame(instruments_frame)
        piano_section.pack(side="right", fill="both", expand=True, padx=(10, 0))

        piano_title = ctk.CTkLabel(
            piano_section,
            text="🎹 Piano Keyboard",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        piano_title.pack(pady=(10, 5))

        self.piano_frame = ctk.CTkFrame(piano_section, height=280)
        self.piano_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # Legend
        legend = ctk.CTkLabel(
            tab,
            text="🎸 Legend: 🔴 Root Notes | 🔵 Chord Tones | 🟢 Scale Notes | ⚪ Open Strings",
            font=ctk.CTkFont(size=12)
        )
        legend.pack(pady=(0, 10))

        # Initialize fretboard and piano
        self.fretboard_data = {}
        self.piano_keys = {}
        self.tunings = {
            "Standard": ["E", "A", "D", "G", "B", "E"],
            "Drop D": ["D", "A", "D", "G", "B", "E"],
            "DADGAD": ["D", "A", "D", "G", "A", "D"]
        }
        self.current_tuning = self.tunings["Standard"]
        self.highlighted_notes = set()
        self.current_scale_position = 0  # Track which position to show
        self.create_fretboard()
        self.create_piano_keyboard()

        # Load initial data
        self.update_fretboard_from_tabs()

    def on_scale_root_change(self, root):
        """Handle root note selection"""
        self.update_current_scale()

    def on_scale_type_change(self, scale_type):
        """Handle scale type selection"""
        self.update_current_scale()

    def update_current_scale(self):
        """Update the current scale based on root and type selection"""
        root = self.scale_root_var.get()
        scale_type = self.scale_type_var.get()
        scale_name = f"{root} {scale_type}"

        # Update the combined scale variable for compatibility
        self.scale_var.set(scale_name)

        # Create the scale if it exists
        if scale_name in scales_data:
            notes = scales_data[scale_name]
            self.current_scale = Scale(root, scale_type, notes)
            self.update_scale_display()
            self.highlight_scale_on_fretboard()
            # Piano update will be handled by tab changes
        else:
            # Try to create scale dynamically
            try:
                scale_type_key = scale_type.lower().replace(' ', '_')
                if scale_type_key in ['major', 'minor', 'harmonic_minor', 'melodic_minor']:
                    if scale_type_key == 'major':
                        self.current_scale = ScaleBuilder.major(root)
                    elif scale_type_key == 'minor':
                        self.current_scale = ScaleBuilder.minor(root)
                    elif scale_type_key == 'harmonic_minor':
                        self.current_scale = ScaleBuilder.minor(root, 'harmonic')
                    elif scale_type_key == 'melodic_minor':
                        self.current_scale = ScaleBuilder.minor(root, 'melodic')
                else:
                    # For modal and other scales, try to create from available types
                    scale_type_map = {
                        'ionian': 'major',
                        'aeolian': 'minor_natural',
                        'dorian': lambda r: ScaleBuilder.dorian(r),
                        'phrygian': lambda r: ScaleBuilder.phrygian(r),
                        'lydian': lambda r: ScaleBuilder.lydian(r),
                        'mixolydian': lambda r: ScaleBuilder.mixolydian(r),
                        'locrian': lambda r: ScaleBuilder.locrian(r),
                        'major_pentatonic': lambda r: ScaleBuilder.pentatonic_major(r),
                        'minor_pentatonic': lambda r: ScaleBuilder.pentatonic_minor(r),
                        'blues': lambda r: ScaleBuilder.blues(r),
                        'whole_tone': lambda r: ScaleBuilder.whole_tone(r),
                        'diminished': lambda r: ScaleBuilder.diminished(r),
                        'augmented': lambda r: ScaleBuilder.augmented(r)
                    }

                    if scale_type_key in scale_type_map:
                        if callable(scale_type_map[scale_type_key]):
                            self.current_scale = scale_type_map[scale_type_key](root)
                        else:
                            self.current_scale = Scale(root, scale_type_map[scale_type_key])
                    else:
                        self.current_scale = ScaleBuilder.major(root)  # fallback

                self.update_scale_display()
                self.highlight_scale_on_fretboard()
                # Piano update will be handled by tab changes

            except Exception as e:
                print(f"Could not create scale {scale_name}: {e}")
                # Fallback to C Major
                self.scale_root_var.set("C")
                self.scale_type_var.set("Major")
                self.update_current_scale()

    def update_scale_display(self):
        """Update the scale information display"""
        if self.current_scale:
            # Update scale name display if it exists
            if hasattr(self, 'scale_info'):
                self.scale_info.configure(text=f"Scale: {self.current_scale.name}")
            # Update piano keys if the method exists
            if hasattr(self, 'update_piano_keys'):
                self.update_piano_keys()

    def on_scale_change(self, scale_name):
        """Handle scale selection"""
        if scale_name in scales_data:
            notes = scales_data[scale_name]
            self.current_scale = Scale(scale_name.split()[0], " ".join(scale_name.split()[1:]), notes)

            # Update display with intervals
            notes_with_intervals = self.get_scale_notes_with_intervals(scale_name, notes)
            self.scale_info.configure(text=f"Scale: {scale_name}\n{notes_with_intervals}")

            # Generate and display harmonized chords
            self.update_harmonized_chords(scale_name)

            # Reset scale position when changing scale
            self.current_scale_position = 0

    def get_scale_notes_with_intervals(self, scale_name, notes):
        """Get formatted string showing scale notes with their intervals"""
        try:
            # Determine scale type from name
            scale_type = self.get_scale_type_from_name(scale_name)

            # Get interval pattern for this scale type
            if scale_type in SCALE_INTERVAL_PATTERNS:
                intervals = SCALE_INTERVAL_PATTERNS[scale_type]
            else:
                # Default to major for unknown types
                intervals = SCALE_INTERVAL_PATTERNS['major']

            # Build the display string
            result_lines = []

            # Add notes with intervals
            notes_line = "Notes: "
            intervals_line = "Intervals: "

            for i, note in enumerate(notes):
                if i < len(intervals):
                    interval_key = intervals[i]
                    interval_name = SCALE_INTERVALS.get(interval_key, f"Interval {interval_key}")

                    notes_line += f"{note} "
                    intervals_line += f"{interval_name} "

            result_lines.append(notes_line.rstrip())
            result_lines.append(intervals_line.rstrip())

            return "\n".join(result_lines)

        except Exception as e:
            # Fallback to simple display
            notes_str = " ".join(notes)
            return f"Notes: {notes_str}\nIntervals: Could not determine intervals"

    def get_scale_type_from_name(self, scale_name):
        """Extract scale type from scale name"""
        scale_name_lower = scale_name.lower()

        # Check for specific scale types
        if 'harmonic minor' in scale_name_lower:
            return 'harmonic_minor'
        elif 'melodic minor' in scale_name_lower:
            return 'melodic_minor'
        elif 'dorian' in scale_name_lower:
            return 'dorian'
        elif 'phrygian' in scale_name_lower:
            return 'phrygian'
        elif 'lydian' in scale_name_lower:
            return 'lydian'
        elif 'mixolydian' in scale_name_lower:
            return 'mixolydian'
        elif 'aeolian' in scale_name_lower:
            return 'aeolian'
        elif 'locrian' in scale_name_lower:
            return 'locrian'
        elif 'whole tone' in scale_name_lower:
            return 'whole_tone'
        elif 'chromatic' in scale_name_lower:
            return 'chromatic'
        elif 'diminished' in scale_name_lower:
            return 'diminished'
        elif 'augmented' in scale_name_lower:
            return 'augmented'
        elif 'bebop' in scale_name_lower:
            if 'major' in scale_name_lower:
                return 'bebop_major'
            else:
                return 'bebop_dominant'
        elif 'enigmatic' in scale_name_lower:
            return 'enigmatic'
        elif any(exotic in scale_name_lower for exotic in ['hirajoshi', 'insen', 'iwato', 'kumoi', 'pelog', 'slendro', 'yo']):
            # Return the specific exotic scale name
            for exotic in ['hirajoshi', 'insen', 'iwato', 'kumoi', 'pelog', 'slendro', 'yo']:
                if exotic in scale_name_lower:
                    return exotic.replace(' ', '_')
        elif 'minor' in scale_name_lower:
            return 'minor'
        else:
            return 'major'

    def update_harmonized_chords(self, scale_name):
        """Generate and display harmonized chords for the selected scale"""
        try:
            # Determine scale type
            scale_type = 'major'  # default
            if 'minor' in scale_name.lower():
                if 'harmonic' in scale_name.lower():
                    scale_type = 'harmonic_minor'
                else:
                    scale_type = 'minor'
            elif 'dorian' in scale_name.lower() or 'phrygian' in scale_name.lower() or 'lydian' in scale_name.lower() or 'mixolydian' in scale_name.lower():
                scale_type = 'major'  # modal scales use major harmonization

            # Get harmonization pattern
            if scale_type not in HARMONIZATION_PATTERNS:
                scale_type = 'major'  # fallback

            pattern = HARMONIZATION_PATTERNS[scale_type]

            # Get scale root
            root_note = scale_name.split()[0]

            # Generate harmonized chords
            self.harmonized_chords = {}
            note_letters = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

            root_index = note_letters.index(root_note)
            for degree, quality in pattern.items():
                # Calculate chord root
                chord_root_index = (root_index + (degree - 1)) % 12
                chord_root = note_letters[chord_root_index]

                # Create chord name and check if it exists
                chord_name = f"{chord_root}{quality}"

                # Fallback to simpler chord if complex one doesn't exist
                if chord_name not in chords_data:
                    # Try simplified versions
                    if 'maj7' in quality:
                        chord_name = f"{chord_root}maj7"
                    elif 'm7' in quality:
                        chord_name = f"{chord_root}m7"
                    elif '7' in quality and quality != '7':
                        chord_name = f"{chord_root}7"
                    elif 'dim7' in quality:
                        chord_name = f"{chord_root}dim7"
                    else:
                        # Ultimate fallback to triad
                        chord_name = f"{chord_root} Major" if quality.startswith('maj') else f"{chord_root} Minor"

                # Store with roman numeral
                roman_numeral = ROMAN_NUMERALS[degree]
                if scale_type == 'minor' and degree in [1, 3, 4, 5, 6, 7]:
                    roman_numeral = roman_numeral.lower()
                elif scale_type == 'harmonic_minor' and degree in [1, 4, 5, 7]:
                    roman_numeral = roman_numeral.lower()

                self.harmonized_chords[roman_numeral] = {
                    'name': chord_name,
                    'degree': degree,
                    'roman': roman_numeral
                }

            # Update harmonization display
            self.update_harmonization_display()

        except Exception as e:
            print(f"Error generating harmonized chords: {e}")
            # Clear harmonization display on error
            if hasattr(self, 'harmonization_frame'):
                for widget in self.harmonization_frame.winfo_children():
                    widget.destroy()

    def update_harmonization_display(self):
        """Update the harmonization display with chord buttons"""
        if not hasattr(self, 'harmonization_frame'):
            return

        # Clear existing content
        for widget in self.harmonization_frame.winfo_children():
            widget.destroy()

        if not hasattr(self, 'harmonized_chords') or not self.harmonized_chords:
            no_chords_label = ctk.CTkLabel(
                self.harmonization_frame,
                text="No harmonized chords available",
                font=ctk.CTkFont(size=12)
            )
            no_chords_label.pack(pady=20)
            return

        # Create title
        title = ctk.CTkLabel(
            self.harmonization_frame,
            text="🎸 Harmonized Chords (1-3-5-7)",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        title.pack(pady=(10, 15))

        # Create chord buttons grid
        chords_frame = ctk.CTkFrame(self.harmonization_frame)
        chords_frame.pack(fill="x", padx=10)

        # Sort by degree
        sorted_chords = sorted(self.harmonized_chords.items(), key=lambda x: x[1]['degree'])

        for i, (roman, chord_data) in enumerate(sorted_chords):
            # Create chord button with drag hint
            chord_button = ctk.CTkButton(
                chords_frame,
                text=f"{roman}° {chord_data['name']}\n👆 Click to add to progression",
                command=lambda c=chord_data['name']: self.select_harmonized_chord(c),
                width=120,
                height=45,
                font=ctk.CTkFont(size=10),
                fg_color="#4CAF50",
                hover_color="#45a049"
            )

            # Position in grid (2 columns)
            row = i // 2
            col = i % 2
            chord_button.grid(row=row, column=col, padx=5, pady=3, sticky="ew")

            # Configure grid weights
            chords_frame.grid_columnconfigure(col, weight=1)

        # Info text
        info_text = ctk.CTkLabel(
            self.harmonization_frame,
            text="Click chords to add them to your custom progression",
            font=ctk.CTkFont(size=10),
            text_color="gray"
        )
        info_text.pack(pady=(15, 10))

    def update_custom_progression_display(self):
        """Update the display of the custom progression"""
        # Clear existing content
        for widget in self.progression_builder.winfo_children():
            widget.destroy()

        if not self.custom_progression:
            empty_label = ctk.CTkLabel(
                self.progression_builder,
                text="No chords added yet. Click harmonized chords above to build your progression!",
                font=ctk.CTkFont(size=12),
                text_color="gray"
            )
            empty_label.pack(pady=20)
            return

        # Create progression display
        progression_frame = ctk.CTkFrame(self.progression_builder)
        progression_frame.pack(fill="x", padx=10, pady=10)

        # Title
        title = ctk.CTkLabel(
            progression_frame,
            text=f"Your Progression ({len(self.custom_progression)} chords):",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        title.pack(anchor="w", pady=(5, 10))

        # Chord sequence
        chords_text = " → ".join(self.custom_progression)
        chords_label = ctk.CTkLabel(
            progression_frame,
            text=chords_text,
            font=ctk.CTkFont(size=14),
            wraplength=600
        )
        chords_label.pack(anchor="w", pady=(0, 10))

        # Individual chord buttons with remove option
        chords_container = ctk.CTkFrame(progression_frame)
        chords_container.pack(fill="x", pady=(5, 0))

        for i, chord_name in enumerate(self.custom_progression):
            chord_frame = ctk.CTkFrame(chords_container)
            chord_frame.pack(side="left", padx=2)

            # Chord button
            chord_btn = ctk.CTkButton(
                chord_frame,
                text=chord_name,
                width=60,
                height=30,
                font=ctk.CTkFont(size=10),
                command=lambda idx=i: self.remove_chord_from_progression(idx)
            )
            chord_btn.pack(side="left")

            # Remove button
            remove_btn = ctk.CTkButton(
                chord_frame,
                text="❌",
                width=25,
                height=30,
                font=ctk.CTkFont(size=8),
                fg_color="#DC143C",
                command=lambda idx=i: self.remove_chord_from_progression(idx)
            )
            remove_btn.pack(side="left")

    def remove_chord_from_progression(self, index):
        """Remove a chord from the custom progression"""
        if 0 <= index < len(self.custom_progression):
            self.custom_progression.pop(index)
            self.update_custom_progression_display()

            # Disable buttons if no chords left
            if not self.custom_progression:
                if hasattr(self, 'play_custom_btn'):
                    self.play_custom_btn.configure(state="disabled")
                if hasattr(self, 'analyze_custom_btn'):
                    self.analyze_custom_btn.configure(state="disabled")

    def clear_custom_progression(self):
        """Clear the entire custom progression"""
        self.custom_progression = []
        self.update_custom_progression_display()

        # Disable buttons
        if hasattr(self, 'play_custom_btn'):
            self.play_custom_btn.configure(state="disabled")
        if hasattr(self, 'analyze_custom_btn'):
            self.analyze_custom_btn.configure(state="disabled")

    def play_custom_progression(self):
        """Play the custom progression"""
        if self.custom_progression:
            print(f"Playing custom progression: {' → '.join(self.custom_progression)}")

            # Create a virtual progression object for playback
            virtual_progression = {
                'name': 'Custom Progression',
                'chords': self.custom_progression
            }

            # Store temporarily and play
            old_progression = getattr(self, 'current_progression', None)
            self.current_progression = virtual_progression
            self.play_current_progression()
            self.current_progression = old_progression

    def analyze_custom_progression(self):
        """Analyze the custom progression"""
        if self.custom_progression:
            print(f"Analyzing custom progression: {' → '.join(self.custom_progression)}")

            # Create a virtual progression object for analysis
            virtual_progression = {
                'name': 'Custom Progression',
                'chords': self.custom_progression
            }

            # Store temporarily and analyze
            old_progression = getattr(self, 'current_progression', None)
            self.current_progression = virtual_progression
            self.analyze_progression()
            self.current_progression = old_progression

    def save_scale_favorite(self):
        """Save current scale to favorites"""
        if self.current_scale:
            # Create favorites file if it doesn't exist
            favorites_file = "scale_favorites.json"
            try:
                import json
                try:
                    with open(favorites_file, 'r') as f:
                        favorites = json.load(f)
                except FileNotFoundError:
                    favorites = []

                # Check if already saved
                scale_name = f"{self.current_scale.root} {self.current_scale.scale_type}"
                if scale_name not in [f['name'] for f in favorites]:
                    favorite = {
                        'name': scale_name,
                        'root': self.current_scale.root,
                        'type': self.current_scale.scale_type,
                        'notes': self.current_scale.notes,
                        'timestamp': time.strftime("%Y-%m-%d %H:%M:%S")
                    }
                    favorites.append(favorite)

                    with open(favorites_file, 'w') as f:
                        json.dump(favorites, f, indent=2)

                    self.update_favorites_display()
                    messagebox.showinfo("Success", f"Scale '{scale_name}' saved to favorites!")
                else:
                    messagebox.showinfo("Info", "This scale is already in your favorites.")

            except Exception as e:
                messagebox.showerror("Error", f"Failed to save favorite: {e}")

    def load_scale_favorite(self, favorite_name):
        """Load a scale from favorites"""
        try:
            import json
            with open("scale_favorites.json", 'r') as f:
                favorites = json.load(f)

            for fav in favorites:
                if fav['name'] == favorite_name:
                    # Set the scale
                    self.scale_var.set(fav['name'])
                    self.on_scale_change(fav['name'])
                    break

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load favorite: {e}")

    def delete_scale_favorite(self, favorite_name):
        """Delete a scale from favorites"""
        try:
            import json
            with open("scale_favorites.json", 'r') as f:
                favorites = json.load(f)

            favorites = [f for f in favorites if f['name'] != favorite_name]

            with open("scale_favorites.json", 'w') as f:
                json.dump(favorites, f, indent=2)

            self.update_favorites_display()
            messagebox.showinfo("Success", f"Scale '{favorite_name}' removed from favorites.")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete favorite: {e}")

    def update_favorites_display(self):
        """Update the favorites display"""
        if not hasattr(self, 'favorites_frame'):
            return

        # Clear existing content
        for widget in self.favorites_frame.winfo_children():
            widget.destroy()

        try:
            import json
            with open("scale_favorites.json", 'r') as f:
                favorites = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            favorites = []

        if not favorites:
            empty_label = ctk.CTkLabel(
                self.favorites_frame,
                text="No favorite scales yet. Save some scales using the 💾 Save button!",
                font=ctk.CTkFont(size=12),
                text_color="gray"
            )
            empty_label.pack(pady=20)
            return

        # Create favorites grid
        for i, fav in enumerate(favorites[-6:]):  # Show last 6 favorites
            fav_frame = ctk.CTkFrame(self.favorites_frame)
            fav_frame.pack(fill="x", padx=10, pady=2)

            # Scale name button
            name_btn = ctk.CTkButton(
                fav_frame,
                text=fav['name'],
                command=lambda n=fav['name']: self.load_scale_favorite(n),
                font=ctk.CTkFont(size=11),
                fg_color=COLORS['highlight'],
                text_color="black",
                height=30
            )
            name_btn.pack(side="left", fill="x", expand=True, padx=(5, 2))

            # Delete button
            delete_btn = ctk.CTkButton(
                fav_frame,
                text="🗑️",
                command=lambda n=fav['name']: self.delete_scale_favorite(n),
                width=30,
                height=30,
                fg_color=COLORS['danger'],
                font=ctk.CTkFont(size=10)
            )
            delete_btn.pack(side="right", padx=(2, 5))

    def select_harmonized_chord(self, chord_name):
        """Handle selection of harmonized chord - adds to custom progression"""
        # Add chord to custom progression
        if chord_name not in self.custom_progression:
            self.custom_progression.append(chord_name)
            self.update_custom_progression_display()

            # Enable buttons
            if hasattr(self, 'play_custom_btn'):
                self.play_custom_btn.configure(state="normal")
            if hasattr(self, 'analyze_custom_btn'):
                self.analyze_custom_btn.configure(state="normal")

        # Also set the chord in the chord builder tab
        if hasattr(self, 'chord_var'):
            # Try to find the chord in our chord database
            # Use the global chords_menu_order list instead of widget
            for available_chord in chords_menu_order:
                if chord_name.lower() in available_chord.lower() or available_chord.lower() in chord_name.lower():
                    self.chord_var.set(available_chord)
                    self.on_chord_change(available_chord)
                    # Switch to chord builder tab
                    self.tabview.set("Chord Builder")
                    break

    def on_chord_change(self, chord_name):
        """Handle chord selection"""
        if chord_name in chords_data:
            notes = chords_data[chord_name]
            root = chord_name.split()[0]
            quality = " ".join(chord_name.split()[1:])
            self.current_chord = Chord(root, quality, notes)

            # Update display
            notes_str = " ".join(notes)
            self.chord_info.configure(text=f"Chord: {chord_name}\nNotes: {notes_str}")

    def play_current_scale(self):
        """Play the current scale based on selected mode"""
        if not self.current_scale or not self.current_scale.notes:
            messagebox.showinfo("Info", "No scale selected!")
            return

        playback_mode = self.playback_mode_var.get()
        notes = self.current_scale.notes.copy()

        print(f"Playing scale: {self.current_scale.name} ({playback_mode})")

        if playback_mode == "Ascending":
            self._play_scale_sequence(notes)
        elif playback_mode == "Descending":
            self._play_scale_sequence(list(reversed(notes)))
        elif playback_mode == "Ascending + Descending":
            self._play_scale_sequence(notes)
            time.sleep(0.3)  # Brief pause
            self._play_scale_sequence(list(reversed(notes[:-1])))  # Skip the octave note
        elif playback_mode == "Arpeggio":
            self._play_scale_arpeggio(notes)

    def _play_scale_sequence(self, notes):
        """Play notes in sequence"""
        for note in notes:
            audio_player.play_note(note, 0.3)
            time.sleep(0.15)  # Faster for sequences

    def _play_scale_arpeggio(self, notes):
        """Play scale as arpeggio (every other note)"""
        # Play root, third, fifth, seventh, etc.
        arpeggio_indices = [0, 2, 4, 6]  # Common arpeggio pattern
        for i in arpeggio_indices:
            if i < len(notes):
                audio_player.play_note(notes[i], 0.4)
                time.sleep(0.2)

    def transpose_scale(self, semitones):
        """Transpose the current scale"""
        if self.current_scale:
            try:
                # Simple transposition by changing the root note
                notes = self.current_scale.notes
                if notes:
                    # Get current root
                    current_root = notes[0]
                    root_note = current_root[0]  # Get note letter
                    root_octave = int(current_root[1]) if len(current_root) > 1 else 4

                    # Calculate new root
                    note_letters = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
                    current_index = note_letters.index(root_note)
                    new_index = (current_index + semitones) % 12
                    new_root = note_letters[new_index]

                    # Adjust octave if necessary
                    octave_adjust = (current_index + semitones) // 12
                    new_octave = root_octave + octave_adjust

                    # Find a scale with the new root
                    new_scale_name = f"{new_root} {self.current_scale.scale_type}"
                    if new_scale_name in scales_data:
                        self.scale_var.set(new_scale_name)
                        self.on_scale_change(new_scale_name)
                        print(f"Transposed to: {new_scale_name}")
                    else:
                        messagebox.showinfo("Info", f"No {new_scale_name} scale available")
            except Exception as e:
                messagebox.showerror("Error", f"Transpose failed: {e}")
        else:
            messagebox.showinfo("Info", "No scale to transpose!")

    def show_relative_scale(self):
        """Show the relative major/minor scale"""
        if self.current_scale:
            try:
                scale_name = self.current_scale.name
                parts = scale_name.split()

                if len(parts) >= 2:
                    root = parts[0]
                    scale_type = " ".join(parts[1:])

                    # Define relative relationships
                    relatives = {
                        'C Major': 'A Minor',
                        'G Major': 'E Minor',
                        'D Major': 'B Minor',
                        'A Major': 'F# Minor',
                        'E Major': 'C# Minor',
                        'A Minor': 'C Major',
                        'E Minor': 'G Major',
                        'B Minor': 'D Major',
                        'F# Minor': 'A Major',
                        'C# Minor': 'E Major'
                    }

                    if scale_name in relatives:
                        relative_name = relatives[scale_name]
                        if relative_name in scales_data:
                            self.scale_var.set(relative_name)
                            self.on_scale_change(relative_name)
                            print(f"Switched to relative: {relative_name}")
                        else:
                            messagebox.showinfo("Info", f"Relative scale {relative_name} not available")
                    else:
                        messagebox.showinfo("Info", "No relative scale defined for this scale")
            except Exception as e:
                messagebox.showerror("Error", f"Relative scale failed: {e}")
        else:
            messagebox.showinfo("Info", "No scale selected!")

    def show_scale_positions(self):
        """Show different positions of the current scale on fretboard"""
        if not self.current_scale:
            messagebox.showinfo("Info", "No scale selected!")
            return

        # Cycle through positions (0-5 for a typical guitar scale)
        self.current_scale_position = (self.current_scale_position + 1) % 6

        # Clear current highlighting
        self.clear_fretboard()

        # Show scale in current position
        self.highlight_scale_in_position(self.current_scale_position)

        # Update status
        position_names = ["Open", "1st", "2nd", "3rd", "5th", "7th"]
        position_name = position_names[self.current_scale_position]
        print(f"Showing {self.current_scale.name} in {position_name} position")

    def highlight_scale_in_position(self, position):
        """Highlight scale notes in a specific position on fretboard"""
        if not self.current_scale or not self.current_scale.notes:
            return

        # Normalize scale notes
        scale_notes = set()
        for note in self.current_scale.notes:
            if note[-1].isdigit():
                note_name = note[:-1]
            else:
                note_name = note
            scale_notes.add(note_name)

        # Get root note
        root_note_full = self.current_scale.notes[0]
        if root_note_full[-1].isdigit():
            root_note = root_note_full[:-1]
        else:
            root_note = root_note_full

        # Define fret ranges for each position (typical guitar scale positions)
        position_ranges = {
            0: (0, 4),    # Open position
            1: (1, 5),    # 1st position
            2: (3, 7),    # 2nd position
            3: (5, 9),    # 3rd position
            4: (7, 11),   # 5th position
            5: (9, 13),   # 7th position
        }

        start_fret, end_fret = position_ranges.get(position, (0, 4))

        for string_idx in range(5, -1, -1):
            for fret in range(start_fret, min(end_fret + 1, 13)):  # Don't go beyond fret 12
                note_at_pos = self.get_note_at_fret(self.current_tuning[string_idx], fret)

                pos_key = f"{string_idx}_{fret}"
                if pos_key in self.fretboard_positions:
                    label = self.fretboard_positions[pos_key]

                    if note_at_pos == root_note:
                        # Root note - red
                        label.configure(fg_color="#DC143C", text_color="white")
                    elif note_at_pos in scale_notes:
                        # Scale note - green
                        label.configure(fg_color="#4CAF50", text_color="white")
                    else:
                        # Not in scale - dark
                        label.configure(fg_color="#2B2B2B", text_color="gray")

    def show_scale_patterns(self):
        """Show different scale patterns on fretboard"""
        if not self.current_scale:
            messagebox.showinfo("Info", "No scale selected!")
            return

        # Create a pattern selection dialog
        pattern_window = ctk.CTkToplevel(self)
        pattern_window.title("Scale Patterns")
        pattern_window.geometry("400x300")
        pattern_window.grab_set()  # Make modal

        title = ctk.CTkLabel(pattern_window, text=f"Patterns for {self.current_scale.name}",
                           font=ctk.CTkFont(size=16, weight="bold"))
        title.pack(pady=20)

        # Pattern buttons
        patterns = [
            ("3 Notes Per String", lambda: self.show_pattern("3nps")),
            ("CAGED System", lambda: self.show_pattern("caged")),
            ("Diagonal Pattern", lambda: self.show_pattern("diagonal")),
            ("Horizontal Pattern", lambda: self.show_pattern("horizontal"))
        ]

        for pattern_name, pattern_func in patterns:
            btn = ctk.CTkButton(
                pattern_window,
                text=pattern_name,
                command=pattern_func,
                width=200,
                height=35
            )
            btn.pack(pady=5)

        # Close button
        close_btn = ctk.CTkButton(
            pattern_window,
            text="Close",
            command=pattern_window.destroy,
            fg_color="#666666"
        )
        close_btn.pack(pady=(20, 10))

    def show_pattern(self, pattern_type):
        """Show a specific scale pattern"""
        if not self.current_scale:
            return

        # Clear fretboard
        self.clear_fretboard()

        # Get scale notes (normalized)
        scale_notes = set()
        for note in self.current_scale.notes:
            if note[-1].isdigit():
                note_name = note[:-1]
            else:
                note_name = note
            scale_notes.add(note_name)

        root_note = self.current_scale.notes[0]
        if root_note[-1].isdigit():
            root_note = root_note[:-1]

        # Switch to fretboard tab
        self.tabview.set("Fretboard Viewer")

        if pattern_type == "3nps":
            self.show_3nps_pattern(scale_notes, root_note)
        elif pattern_type == "caged":
            self.show_caged_pattern(scale_notes, root_note)
        elif pattern_type == "diagonal":
            self.show_diagonal_pattern(scale_notes, root_note)
        elif pattern_type == "horizontal":
            self.show_horizontal_pattern(scale_notes, root_note)

    def show_3nps_pattern(self, scale_notes, root_note):
        """Show 3 Notes Per String pattern"""
        # 3NPS pattern starting from fret 5
        pattern_positions = [
            # High E string
            (0, 5), (0, 7), (0, 9),
            # B string
            (1, 5), (1, 7), (1, 9),
            # G string
            (2, 5), (2, 7), (2, 9),
            # D string
            (3, 5), (3, 7), (3, 9),
            # A string
            (4, 5), (4, 7), (4, 9),
            # Low E string
            (5, 5), (5, 7), (5, 9)
        ]

        self.apply_pattern_positions(pattern_positions, scale_notes, root_note, "3 Notes Per String")

    def show_caged_pattern(self, scale_notes, root_note):
        """Show CAGED system pattern"""
        # CAGED pattern for C major (can be extended for other keys)
        caged_positions = [
            # C shape (open position + 1st position)
            (5, 0), (4, 3), (3, 2), (2, 0), (1, 1), (0, 0),
            (5, 8), (4, 10), (3, 9), (2, 7), (1, 8), (0, 8)
        ]

        self.apply_pattern_positions(caged_positions, scale_notes, root_note, "CAGED System")

    def show_diagonal_pattern(self, scale_notes, root_note):
        """Show diagonal scale pattern"""
        # Diagonal connections across strings
        diagonal_positions = [
            (5, 3), (4, 5), (3, 7), (2, 9), (1, 7), (0, 9),
            (5, 5), (4, 7), (3, 9), (2, 11), (1, 9), (0, 11)
        ]

        self.apply_pattern_positions(diagonal_positions, scale_notes, root_note, "Diagonal Pattern")

    def show_horizontal_pattern(self, scale_notes, root_note):
        """Show horizontal scale pattern (same fret, different strings)"""
        # Horizontal pattern: same fret across strings
        horizontal_positions = [
            # Fret 5
            (5, 5), (4, 5), (3, 5), (2, 5), (1, 5), (0, 5),
            # Fret 7
            (5, 7), (4, 7), (3, 7), (2, 7), (1, 7), (0, 7),
            # Fret 9
            (5, 9), (4, 9), (3, 9), (2, 9), (1, 9), (0, 9)
        ]

        self.apply_pattern_positions(horizontal_positions, scale_notes, root_note, "Horizontal Pattern")

    def apply_pattern_positions(self, positions, scale_notes, root_note, pattern_name):
        """Apply pattern positions to fretboard"""
        for string_idx, fret in positions:
            if 0 <= fret <= 12:  # Valid fret range
                note_at_pos = self.get_note_at_fret(self.current_tuning[string_idx], fret)
                pos_key = f"{string_idx}_{fret}"

                if pos_key in self.fretboard_positions:
                    label = self.fretboard_positions[pos_key]

                    if note_at_pos == root_note:
                        label.configure(fg_color="#DC143C", text_color="white")  # Red for root
                    elif note_at_pos in scale_notes:
                        label.configure(fg_color="#4CAF50", text_color="white")  # Green for scale notes
                    else:
                        label.configure(fg_color="#FFD700", text_color="black")  # Gold for pattern positions

        print(f"Showing {pattern_name} pattern for {self.current_scale.name}")

    def play_current_chord(self):
        """Play the current chord"""
        if self.current_chord and self.current_chord.notes:
            print(f"Playing chord: {self.current_chord.name}")
            audio_player.play_chord(self.current_chord.notes)
        else:
            messagebox.showinfo("Info", "No chord selected!")

    def transpose_chord(self, semitones):
        """Transpose the current chord"""
        if self.current_chord:
            try:
                # Get current chord name from the dropdown
                current_chord_name = self.chord_var.get()
                if not current_chord_name:
                    messagebox.showinfo("Info", "No chord selected!")
                    return

                # Parse chord name (e.g., "C7" -> root="C", quality="7")
                parts = current_chord_name.split()
                if len(parts) < 1:
                    messagebox.showinfo("Info", "Invalid chord format!")
                    return

                root_note = parts[0]
                quality = " ".join(parts[1:]) if len(parts) > 1 else ""

                # Calculate new root
                note_letters = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
                current_index = note_letters.index(root_note)
                new_index = (current_index + semitones) % 12
                new_root = note_letters[new_index]

                # Construct new chord name
                if quality:
                    new_chord_name = f"{new_root}{quality}"
                else:
                    new_chord_name = new_root

                # Find the chord in our data (try different variations)
                found_chord = None
                for chord_key in chords_data.keys():
                    # Normalize chord names for comparison
                    normalized_key = chord_key.replace(" ", "").replace("Major", "").replace("Minor", "m")
                    normalized_new = new_chord_name.replace(" ", "").replace("Major", "").replace("Minor", "m")

                    if normalized_key.lower() == normalized_new.lower():
                        found_chord = chord_key
                        break

                if found_chord:
                    self.chord_var.set(found_chord)
                    self.on_chord_change(found_chord)
                    print(f"Transposed to: {found_chord}")
                else:
                    # Try with original naming convention
                    alt_chord_name = f"{new_root} {quality}" if quality else new_root
                    if alt_chord_name in chords_data:
                        self.chord_var.set(alt_chord_name)
                        self.on_chord_change(alt_chord_name)
                        print(f"Transposed to: {alt_chord_name}")
                    else:
                        messagebox.showinfo("Info", f"No {new_chord_name} chord available")
            except Exception as e:
                messagebox.showerror("Error", f"Transpose failed: {e}")
        else:
            messagebox.showinfo("Info", "No chord to transpose!")

    def on_progression_change(self, progression_name):
        """Handle progression selection"""
        if progression_name in progressions_data:
            chords = progressions_data[progression_name]
            self.current_progression = {
                'name': progression_name,
                'chords': chords
            }

            # Update display
            chords_str = " → ".join(chords)
            self.progression_info.configure(text=f"Progression: {progression_name}\nChords: {chords_str}")

            # Clear compatible scales
            self.compatible_scales.configure(text="Click 'Analyze' to find compatible scales")

    def play_current_progression(self):
        """Play the current chord progression"""
        if self.current_progression and self.current_progression['chords']:
            print(f"Playing progression: {self.current_progression['name']}")
            for chord_name in self.current_progression['chords']:
                if chord_name in chords_data:
                    notes = chords_data[chord_name]
                    print(f"Playing chord: {chord_name}")
                    audio_player.play_chord(notes, duration=1.5)
                    time.sleep(0.2)  # Pause between chords
                else:
                    print(f"Chord {chord_name} not found")
        else:
            messagebox.showinfo("Info", "No progression selected!")

    def analyze_progression(self):
        """Analyze the current progression and find compatible scales"""
        if self.current_progression and self.current_progression['chords']:
            # Simple analysis: find scales that contain all the chord notes
            compatible_scales = []

            for scale_name, scale_notes in scales_data.items():
                scale_note_set = set(scale_notes)

                # Check if scale contains all notes from progression chords
                progression_notes = set()
                for chord_name in self.current_progression['chords']:
                    if chord_name in chords_data:
                        progression_notes.update(chords_data[chord_name])

                # Check if scale contains most progression notes
                matching_notes = len(progression_notes.intersection(scale_note_set))
                total_notes = len(progression_notes)

                if matching_notes >= total_notes * 0.6:  # At least 60% match
                    compatible_scales.append(scale_name)

            if compatible_scales:
                scales_text = "\n".join(compatible_scales[:10])  # Show first 10
                self.compatible_scales.configure(text=scales_text)
            else:
                self.compatible_scales.configure(text="No compatible scales found")
        else:
            messagebox.showinfo("Info", "No progression to analyze!")

    def save_preset(self):
        """Save current configuration as preset"""
        import tkinter.simpledialog as simpledialog
        import tkinter.messagebox as messagebox

        # Ask for preset name
        name = simpledialog.askstring("Save Preset", "Enter preset name:")
        if not name:
            return

        # Save current state
        preset_data = {
            'scale': self.scale_var.get() if hasattr(self, 'scale_var') else None,
            'chord': self.chord_var.get() if hasattr(self, 'chord_var') else None,
            'progression': self.progression_var.get() if hasattr(self, 'progression_var') else None,
            'timestamp': str(time.time())
        }

        # Determine preset type based on active tab
        try:
            current_tab = self.tabview.get()
            if current_tab == "Scale Explorer" and preset_data['scale']:
                self.presets['scales'][name] = preset_data
                messagebox.showinfo("Preset Saved", f"Scale preset '{name}' saved!")
            elif current_tab == "Chord Builder" and preset_data['chord']:
                self.presets['chords'][name] = preset_data
                messagebox.showinfo("Preset Saved", f"Chord preset '{name}' saved!")
            elif current_tab == "Progression Analyzer" and preset_data['progression']:
                self.presets['progressions'][name] = preset_data
                messagebox.showinfo("Preset Saved", f"Progression preset '{name}' saved!")
            else:
                messagebox.showwarning("Save Preset", "No valid configuration to save!")
        except Exception as e:
            messagebox.showerror("Save Preset", f"Error saving preset: {e}")

    def load_preset(self):
        """Load a saved preset"""
        import tkinter.messagebox as messagebox

        # Show available presets
        all_presets = []
        for ptype in ['scales', 'chords', 'progressions']:
            for name in self.presets[ptype].keys():
                all_presets.append(f"{ptype[:-1].title()}: {name}")

        if all_presets:
            presets_list = "\n".join(all_presets[:10])  # Show first 10
            messagebox.showinfo("Available Presets",
                              f"Saved presets:\n\n{presets_list}\n\nFeature will be expanded!")
        else:
            messagebox.showinfo("Load Preset", "No presets saved yet!")

    def on_bpm_change(self, value):
        """Handle BPM slider change"""
        self.metronome_bpm = int(value)
        self.bpm_display.configure(text=f"{self.metronome_bpm} BPM")

    def toggle_metronome(self):
        """Start or stop the metronome"""
        if self.metronome_running:
            self.stop_metronome()
        else:
            self.start_metronome()

    def start_metronome(self):
        """Start the metronome"""
        if not self.metronome_running:
            self.metronome_running = True
            self.metronome_btn.configure(text="⏹️ Stop Metronome", fg_color="#DC143C")
            self.metronome_thread = threading.Thread(target=self.metronome_loop, daemon=True)
            self.metronome_thread.start()
            print(f"Metronome started at {self.metronome_bpm} BPM")

    def stop_metronome(self):
        """Stop the metronome"""
        self.metronome_running = False
        self.metronome_btn.configure(text="▶️ Start Metronome", fg_color="#4CAF50")
        self.beat_indicator.configure(text_color="#666666")
        print("Metronome stopped")

    def metronome_loop(self):
        """Main metronome loop"""
        beat_count = 0
        while self.metronome_running:
            beat_count += 1

            # Play click sound
            if beat_count == 1:
                # Accent first beat
                audio_player.play_note("C5", 0.1)
                self.beat_indicator.configure(text_color="#FF4444")  # Red for downbeat
            else:
                # Normal beats
                audio_player.play_note("C4", 0.05)
                self.beat_indicator.configure(text_color="#4CAF50")  # Green for other beats

            # Schedule visual reset
            self.after(150, lambda: self.beat_indicator.configure(text_color="#666666"))

            # Calculate delay for next beat
            delay = 60.0 / self.metronome_bpm  # seconds per beat
            time.sleep(delay)

    def tap_tempo(self):
        """Handle tap tempo for setting BPM"""
        current_time = time.time()
        self.tap_times.append(current_time)

        # Keep only last 4 taps
        if len(self.tap_times) > 4:
            self.tap_times.pop(0)

        if len(self.tap_times) >= 2:
            # Calculate average interval
            intervals = []
            for i in range(1, len(self.tap_times)):
                intervals.append(self.tap_times[i] - self.tap_times[i-1])

            avg_interval = sum(intervals) / len(intervals)
            bpm = 60.0 / avg_interval

            # Set reasonable bounds
            bpm = max(60, min(200, int(bpm)))

            self.metronome_bpm = bpm
            self.bpm_slider.set(bpm)
            self.bpm_display.configure(text=f"{bpm} BPM")

            print(f"Tap tempo set to {bpm} BPM")

    def create_fretboard(self):
        """Create the fretboard visualization"""
        # Clear existing content
        for widget in self.fretboard_frame.winfo_children():
            widget.destroy()

        # Create fretboard grid
        self.fretboard_positions = {}  # Store position labels

        # String names (left side) - Low E to High E
        string_names = ["E", "A", "D", "G", "B", "E"]  # Low E to High E

        # Create header with fret numbers
        header_frame = ctk.CTkFrame(self.fretboard_frame)
        header_frame.pack(fill="x", pady=(0, 5))

        # Empty corner
        corner_label = ctk.CTkLabel(header_frame, text="", width=30)
        corner_label.pack(side="left", padx=2)

        # Fret numbers
        for fret in range(13):  # 0-12 frets
            fret_label = ctk.CTkLabel(
                header_frame,
                text=str(fret),
                width=35,
                font=ctk.CTkFont(size=10, weight="bold")
            )
            fret_label.pack(side="left", padx=1)

        # Create strings (from high to low for proper guitar orientation)
        for string_idx in range(5, -1, -1):
            string_frame = ctk.CTkFrame(self.fretboard_frame)
            string_frame.pack(fill="x", pady=1)

            # String name
            string_name = string_names[string_idx]
            string_label = ctk.CTkLabel(
                string_frame,
                text=string_name,
                width=30,
                font=ctk.CTkFont(size=12, weight="bold")
            )
            string_label.pack(side="left", padx=2)

            # Create frets for this string
            for fret in range(13):
                # Calculate note at this position
                open_note = self.current_tuning[string_idx]
                note_at_fret = self.get_note_at_fret(open_note, fret)

                # Create position label
                pos_label = ctk.CTkLabel(
                    string_frame,
                    text=note_at_fret,
                    width=35,
                    height=30,
                    fg_color="#2B2B2B",
                    corner_radius=3,
                    font=ctk.CTkFont(size=11)
                )
                pos_label.pack(side="left", padx=1)

                # Store reference
                pos_key = f"{string_idx}_{fret}"
                self.fretboard_positions[pos_key] = pos_label

                # Add click binding for position info and MIDI playback
                pos_label.bind("<Button-1>", lambda e, s=string_idx, f=fret, n=note_at_fret:
                              self.on_fret_click(s, f, n))

                # Add right-click binding for MIDI playback only
                pos_label.bind("<Button-3>", lambda e, s=string_idx, f=fret, n=note_at_fret:
                              self.play_midi_note(s, f, n))

    def get_note_at_fret(self, open_note, fret):
        """Get the note at a specific fret position"""
        notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

        open_note_idx = notes.index(open_note)
        note_at_fret_idx = (open_note_idx + fret) % 12

        return notes[note_at_fret_idx]

    def note_to_midi_number(self, note_name, octave=4):
        """Convert a note name to MIDI number"""
        # MIDI note numbers: C4 = 60, C3 = 48, C5 = 72, etc.
        note_values = {
            'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3,
            'E': 4, 'F': 5, 'F#': 6, 'Gb': 6, 'G': 7, 'G#': 8,
            'Ab': 8, 'A': 9, 'A#': 10, 'Bb': 10, 'B': 11
        }

        # Extract note and octave
        if note_name[-1].isdigit():
            note = note_name[:-1]
            octave_num = int(note_name[-1])
        else:
            note = note_name
            octave_num = octave

        # Calculate MIDI number: C4 = 60 is the reference
        midi_number = (octave_num + 1) * 12 + note_values.get(note.upper(), 0)
        return midi_number

    def get_midi_at_fret(self, string_idx, fret):
        """Get MIDI number for a fret position"""
        open_note = self.current_tuning[string_idx]
        note_at_fret = self.get_note_at_fret(open_note, fret)

        # Calculate octave based on string and fret
        # Guitar strings: E2, A2, D3, G3, B3, E4
        string_octaves = [2, 2, 3, 3, 3, 4]  # Low E to High E

        # For frets > 0, might need to adjust octave
        octave = string_octaves[string_idx]
        if fret >= 12:  # After 12th fret, notes go up an octave
            octave += 1

        return self.note_to_midi_number(note_at_fret, octave)

    def on_fret_click(self, string_idx, fret, note_name):
        """Handle fret click - show info and play MIDI if enabled"""
        self.show_position_info(string_idx, fret, note_name)

        # If MIDI is enabled, also play the note
        if self.midi_enabled and hasattr(self, 'midi_enabled_var') and self.midi_enabled_var.get():
            self.play_midi_note(string_idx, fret, note_name)

    def play_midi_note(self, string_idx, fret, note_name):
        """Play MIDI note for fret position"""
        if not self.midi_enabled:
            return

        midi_number = self.get_midi_at_fret(string_idx, fret)
        self.midi_manager.play_note(midi_number, duration=1.0)
        print(f"MIDI: Playing note {note_name} (MIDI {midi_number}) on string {string_idx}, fret {fret}")

    def show_position_info(self, string_idx, fret, note_name):
        """Show information about a fret position"""
        string_names = ["Low E", "A", "D", "G", "B", "High E"]
        midi_number = self.get_midi_at_fret(string_idx, fret)

        info_text = f"String: {string_names[string_idx]}\n" \
                   f"Fret: {fret}\n" \
                   f"Note: {note_name}\n" \
                   f"MIDI: {midi_number}"

        messagebox.showinfo("Fret Position Info", info_text)

    def toggle_midi(self):
        """Toggle MIDI functionality"""
        enabled = self.midi_enabled_var.get()
        if enabled and not self.midi_manager.midi_available:
            messagebox.showwarning("MIDI Warning", "MIDI is not available. Please install 'mido' and ensure you have MIDI devices connected.")
            self.midi_enabled_var.set(False)
            return

        print(f"MIDI {'enabled' if enabled else 'disabled'}")

    def change_midi_port(self, port_name):
        """Change MIDI output port"""
        if self.midi_manager.set_port(port_name):
            print(f"MIDI port changed to: {port_name}")
        else:
            messagebox.showerror("MIDI Error", f"Could not open MIDI port: {port_name}")

    def change_midi_velocity(self, value):
        """Change MIDI velocity"""
        self.midi_manager.velocity = int(float(value))
        print(f"MIDI velocity set to: {self.midi_manager.velocity}")

    def update_fretboard_from_tabs(self):
        """Update fretboard and piano highlighting based on current tab selections"""
        self.clear_fretboard()

        # Get current tab
        current_tab = self.tabview.get()

        if current_tab == "Scale Explorer" and self.current_scale:
            self.highlight_scale_on_fretboard()
            self.highlight_notes_on_piano(self.current_scale.notes)
        elif current_tab == "Chord Builder" and self.current_chord:
            self.highlight_chord_on_fretboard()
            self.highlight_notes_on_piano(self.current_chord.notes)
        elif current_tab == "Progression Analyzer" and self.current_progression:
            self.highlight_progression_on_fretboard()
            # Highlight all notes from the progression on piano
            all_notes = set()
            for chord_name in self.current_progression['chords']:
                if chord_name in chords_data:
                    all_notes.update(chords_data[chord_name])
            self.highlight_notes_on_piano(list(all_notes))

    def highlight_scale_on_fretboard(self):
        """Highlight scale notes on fretboard"""
        if not self.current_scale or not self.current_scale.notes:
            return

        # Normalize scale notes to base octave for fretboard display
        scale_notes = set()
        for note in self.current_scale.notes:
            # Extract note name without octave
            if note[-1].isdigit():
                note_name = note[:-1]
            else:
                note_name = note
            scale_notes.add(note_name)

        # Get root note
        root_note_full = self.current_scale.notes[0]
        if root_note_full[-1].isdigit():
            root_note = root_note_full[:-1]
        else:
            root_note = root_note_full

        for string_idx in range(5, -1, -1):
            for fret in range(13):
                note_at_pos = self.get_note_at_fret(self.current_tuning[string_idx], fret)

                pos_key = f"{string_idx}_{fret}"
                if pos_key in self.fretboard_positions:
                    label = self.fretboard_positions[pos_key]

                    if note_at_pos == root_note:
                        # Root note - red
                        label.configure(fg_color="#DC143C", text_color="white")
                    elif note_at_pos in scale_notes:
                        # Scale note - green
                        label.configure(fg_color="#4CAF50", text_color="white")
                    else:
                        # Not in scale - dark
                        label.configure(fg_color="#2B2B2B", text_color="gray")

    def highlight_chord_on_fretboard(self):
        """Highlight chord notes on fretboard"""
        if not self.current_chord or not self.current_chord.notes:
            return

        # Normalize chord notes to base octave for fretboard display
        chord_notes = set()
        for note in self.current_chord.notes:
            # Extract note name without octave
            if note[-1].isdigit():
                note_name = note[:-1]
            else:
                note_name = note
            chord_notes.add(note_name)

        # Get root note
        root_note_full = self.current_chord.notes[0]
        if root_note_full[-1].isdigit():
            root_note = root_note_full[:-1]
        else:
            root_note = root_note_full

        for string_idx in range(5, -1, -1):
            for fret in range(13):
                note_at_pos = self.get_note_at_fret(self.current_tuning[string_idx], fret)

                pos_key = f"{string_idx}_{fret}"
                if pos_key in self.fretboard_positions:
                    label = self.fretboard_positions[pos_key]

                    if note_at_pos == root_note:
                        # Root note - red
                        label.configure(fg_color="#DC143C", text_color="white")
                    elif note_at_pos in chord_notes:
                        # Chord note - blue
                        label.configure(fg_color="#2196F3", text_color="white")
                    else:
                        # Not in chord - dark
                        label.configure(fg_color="#2B2B2B", text_color="gray")

    def highlight_progression_on_fretboard(self):
        """Highlight progression notes on fretboard"""
        if not self.current_progression or not self.current_progression['chords']:
            return

        # Collect all notes from progression
        progression_notes = set()
        root_notes = set()

        for chord_name in self.current_progression['chords']:
            if chord_name in chords_data:
                chord_notes = chords_data[chord_name]
                progression_notes.update(chord_notes)
                root_notes.add(chord_notes[0][:1])  # Root note letter

        for string_idx in range(5, -1, -1):
            for fret in range(13):
                note_at_pos = self.get_note_at_fret(self.current_tuning[string_idx], fret)

                pos_key = f"{string_idx}_{fret}"
                if pos_key in self.fretboard_positions:
                    label = self.fretboard_positions[pos_key]

                    if note_at_pos in root_notes:
                        # Root notes - red
                        label.configure(fg_color="#DC143C", text_color="white")
                    elif note_at_pos in progression_notes:
                        # Progression notes - purple
                        label.configure(fg_color="#9C27B0", text_color="white")
                    else:
                        # Not in progression - dark
                        label.configure(fg_color="#2B2B2B", text_color="gray")

    def clear_fretboard(self):
        """Clear all fretboard highlighting"""
        for pos_key, label in self.fretboard_positions.items():
            label.configure(fg_color="#2B2B2B", text_color="white")

    def change_tuning(self, tuning_name):
        """Change guitar tuning"""
        if tuning_name in self.tunings:
            self.current_tuning = self.tunings[tuning_name]
            self.create_fretboard()
            self.update_fretboard_from_tabs()
            print(f"Tuning changed to: {tuning_name}")

    def show_position_info(self, string_idx, fret, note):
        """Show information about a fretboard position"""
        string_names = ["High E", "B", "G", "D", "A", "Low E"]
        string_name = string_names[string_idx]

        info = f"Position: {string_name} string, fret {fret}\nNote: {note}"
        messagebox.showinfo("Fretboard Position", info)

    def create_piano_keyboard(self):
        """Create the piano keyboard visualization"""
        # Clear existing content
        for widget in self.piano_frame.winfo_children():
            widget.destroy()

        self.piano_keys = {}

        # Piano keyboard layout (2 octaves: C4 to C6)
        # White keys: C, D, E, F, G, A, B
        # Black keys: C#, D#, F#, G#, A#

        white_keys = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
        black_keys = ['C#', 'D#', None, 'F#', 'G#', 'A#', None]  # None for gaps

        # Create keyboard container
        keyboard_frame = ctk.CTkFrame(self.piano_frame)
        keyboard_frame.pack(fill="x", padx=10, pady=10)

        # Two octaves
        for octave in [4, 5]:
            octave_frame = ctk.CTkFrame(keyboard_frame)
            octave_frame.pack(fill="x", pady=(0, 5))

            # White keys row
            white_frame = ctk.CTkFrame(octave_frame)
            white_frame.pack(fill="x")

            for i, note in enumerate(white_keys):
                full_note = f"{note}{octave}"
                key_btn = ctk.CTkButton(
                    white_frame,
                    text=full_note,
                    width=35,
                    height=80,
                    fg_color="white",
                    text_color="black",
                    border_width=1,
                    border_color="gray",
                    command=lambda n=full_note: self.show_piano_key_info(n)
                )
                key_btn.pack(side="left", padx=1)
                self.piano_keys[full_note] = key_btn

            # Black keys row (overlapping white keys)
            black_frame = ctk.CTkFrame(octave_frame)
            black_frame.pack(fill="x")

            # Add spacing to align black keys
            spacer1 = ctk.CTkFrame(black_frame, width=18, height=50)
            spacer1.pack(side="left")

            for i, note in enumerate(black_keys):
                if note is not None:
                    full_note = f"{note}{octave}"
                    key_btn = ctk.CTkButton(
                        black_frame,
                        text=full_note,
                        width=25,
                        height=50,
                        fg_color="black",
                        text_color="white",
                        command=lambda n=full_note: self.show_piano_key_info(n)
                    )
                    key_btn.pack(side="left", padx=1)
                    self.piano_keys[full_note] = key_btn
                else:
                    # Spacer for gaps between black key groups
                    spacer = ctk.CTkFrame(black_frame, width=35, height=50)
                    spacer.pack(side="left")

            # Final spacer
            spacer2 = ctk.CTkFrame(black_frame, width=18, height=50)
            spacer2.pack(side="right")

    def setup_exercises(self):
        """Setup the theory exercises tab"""
        tab = self.tabview.tab("🎯 Theory Exercises")

        # Modern title section
        title_frame = ctk.CTkFrame(tab, fg_color="transparent", height=80)
        title_frame.pack(fill="x", pady=(25, 20))
        title_frame.pack_propagate(False)

        title_left = ctk.CTkFrame(title_frame, fg_color="transparent")
        title_left.pack(side="left", padx=(25, 0))

        # Amber icon for exercises/learning
        icon_bg = ctk.CTkFrame(
            title_left,
            fg_color=COLORS['accent'],
            width=50,
            height=50,
            corner_radius=25
        )
        icon_bg.pack(side="left", padx=(0, 15))
        icon_bg.pack_propagate(False)

        title_icon = ctk.CTkLabel(
            icon_bg,
            text="🎯",
            font=ctk.CTkFont(size=24),
            text_color="white"
        )
        title_icon.place(relx=0.5, rely=0.5, anchor="center")

        title_text_frame = ctk.CTkFrame(title_left, fg_color="transparent")
        title_text_frame.pack(side="left")

        title = ctk.CTkLabel(
            title_text_frame,
            text="Theory Exercises",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=COLORS['text_primary']
        )
        title.pack(anchor="w")

        subtitle = ctk.CTkLabel(
            title_text_frame,
            text="Interactive learning with instant feedback",
            font=ctk.CTkFont(size=11),
            text_color=COLORS['text_secondary']
        )
        subtitle.pack(pady=(0, 20))

        # Exercise selector
        exercise_frame = ctk.CTkFrame(tab)
        exercise_frame.pack(fill="x", padx=20, pady=(0, 20))

        exercise_label = ctk.CTkLabel(exercise_frame, text="Choose Exercise:",
                                    font=ctk.CTkFont(size=14, weight="bold"))
        exercise_label.pack(anchor="w", padx=10, pady=(10, 5))

        self.exercise_var = ctk.StringVar(value="Scale Recognition")
        exercises = ["Scale Recognition", "Chord Identification", "Interval Training", "Progression Quiz"]
        exercise_menu = ctk.CTkOptionMenu(
            exercise_frame,
            values=exercises,
            variable=self.exercise_var,
            command=self.start_exercise,
            width=200
        )
        exercise_menu.pack(anchor="w", padx=10, pady=(0, 10))

        # Start exercise button with modern styling
        start_btn = ctk.CTkButton(
            exercise_frame,
            text="🚀 Start Exercise",
            command=self.start_exercise,
            fg_color=COLORS['primary'],
            hover_color=COLORS['primary_hover'],
            border_width=STYLES['border_width'],
            corner_radius=STYLES['corner_radius'],
            font=ctk.CTkFont(size=13, weight="bold"),
            height=45,
            width=160
        )
        start_btn.pack(anchor="w", padx=10, pady=(10, 10))

        # Exercise display area
        self.exercise_display = ctk.CTkFrame(tab, height=200)
        self.exercise_display.pack(fill="x", padx=20, pady=(0, 20))

        # Answer options
        self.answer_frame = ctk.CTkFrame(tab)
        self.answer_frame.pack(fill="x", padx=20, pady=(0, 20))

        # Results display
        self.results_display = ctk.CTkFrame(tab)
        self.results_display.pack(fill="x", padx=20, pady=(0, 20))

        # Initialize exercise state
        self.current_exercise = None
        self.exercise_score = 0
        self.exercise_total = 0
        self.setup_exercise_display()

    def setup_exercise_display(self):
        """Setup the exercise display area"""
        # Clear existing content
        for widget in self.exercise_display.winfo_children():
            widget.destroy()
        for widget in self.answer_frame.winfo_children():
            widget.destroy()
        for widget in self.results_display.winfo_children():
            widget.destroy()

        # Initial message
        welcome = ctk.CTkLabel(
            self.exercise_display,
            text="🎯 Benvenuto negli esercizi interattivi!\n\nScegli un tipo di esercizio dal menu sopra e clicca 'Start Exercise' per iniziare.\n\nGli esercizi ti aiuteranno a:\n• Riconoscere scale e accordi\n• Imparare gli intervalli\n• Migliorare la teoria musicale\n• Testare le tue conoscenze",
            font=ctk.CTkFont(size=12),
            justify="left"
        )
        welcome.pack(pady=20, padx=20)

    def start_exercise(self, exercise_type=None):
        """Start a theory exercise"""
        if exercise_type is None:
            exercise_type = self.exercise_var.get()

        self.current_exercise = exercise_type
        self.exercise_score = 0
        self.exercise_total = 0

        if exercise_type == "Scale Recognition":
            self.start_scale_recognition()
        elif exercise_type == "Chord Identification":
            self.start_chord_identification()
        elif exercise_type == "Interval Training":
            self.start_interval_training()
        elif exercise_type == "Progression Quiz":
            self.start_progression_quiz()

    def start_scale_recognition(self):
        """Start scale recognition exercise"""
        self.generate_scale_question()

    def generate_scale_question(self):
        """Generate a scale recognition question"""
        # Clear display
        for widget in self.exercise_display.winfo_children():
            widget.destroy()

        # Pick a random scale
        scale_names = list(scales_data.keys())
        correct_scale = scale_names[len(scale_names) // 3]  # Start with common scales
        correct_notes = scales_data[correct_scale]

        # Question
        question = ctk.CTkLabel(
            self.exercise_display,
            text=f"🎼 Quale scala contiene queste note?\n\n{' → '.join(correct_notes)}",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        question.pack(pady=(20, 10))

        # Generate answer options
        options = [correct_scale]
        while len(options) < 4:
            wrong_scale = scale_names[len(scale_names) // 2 + len(options) - 1]
            if wrong_scale not in options:
                options.append(wrong_scale)

        # Shuffle options
        import random
        random.shuffle(options)

        # Answer buttons
        for option in options:
            btn = ctk.CTkButton(
                self.exercise_display,
                text=option,
                command=lambda ans=option, corr=correct_scale: self.check_scale_answer(ans, corr),
                width=150,
                height=35
            )
            btn.pack(pady=5)

        # Results
        self.update_exercise_score()

    def check_scale_answer(self, answer, correct):
        """Check scale recognition answer"""
        self.exercise_total += 1
        if answer == correct:
            self.exercise_score += 1
            messagebox.showinfo("✅ Correct!", f"Yes! The scale is {correct}")
        else:
            messagebox.showerror("❌ Incorrect", f"Sorry, the correct answer is {correct}")

        # Next question
        self.generate_scale_question()

    def update_exercise_score(self):
        """Update exercise score display"""
        for widget in self.results_display.winfo_children():
            widget.destroy()

        score_text = f"Score: {self.exercise_score}/{self.exercise_total}"
        if self.exercise_total > 0:
            percentage = int((self.exercise_score / self.exercise_total) * 100)
            score_text += f" ({percentage}%)"

        score_label = ctk.CTkLabel(
            self.results_display,
            text=score_text,
            font=ctk.CTkFont(size=12, weight="bold")
        )
        score_label.pack(pady=10)

    def start_chord_identification(self):
        """Start chord identification exercise"""
        self.generate_chord_question()

    def generate_chord_question(self):
        """Generate a chord identification question"""
        # Similar to scale recognition but for chords
        chord_names = list(chords_data.keys())
        correct_chord = chord_names[len(chord_names) // 4]  # Start with common chords
        correct_notes = chords_data[correct_chord]

        # Clear display
        for widget in self.exercise_display.winfo_children():
            widget.destroy()

        # Question
        question = ctk.CTkLabel(
            self.exercise_display,
            text=f"🎸 Quale accordo contiene queste note?\n\n{' + '.join(correct_notes)}",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        question.pack(pady=(20, 10))

        # Generate options
        import random
        options = [correct_chord]
        while len(options) < 4:
            wrong_chord = chord_names[len(chord_names) // 3 + len(options)]
            if wrong_chord not in options:
                options.append(wrong_chord)

        random.shuffle(options)

        # Answer buttons
        for option in options:
            btn = ctk.CTkButton(
                self.exercise_display,
                text=option,
                command=lambda ans=option, corr=correct_chord: self.check_chord_answer(ans, corr),
                width=150,
                height=35
            )
            btn.pack(pady=5)

        self.update_exercise_score()

    def check_chord_answer(self, answer, correct):
        """Check chord identification answer"""
        self.exercise_total += 1
        if answer == correct:
            self.exercise_score += 1
            messagebox.showinfo("✅ Correct!", f"Yes! The chord is {correct}")
        else:
            messagebox.showerror("❌ Incorrect", f"Sorry, the correct answer is {correct}")

        self.generate_chord_question()

    def start_interval_training(self):
        """Start interval training exercise"""
        # Placeholder for future implementation
        messagebox.showinfo("Coming Soon", "Interval training will be available in the next update!")

    def start_progression_quiz(self):
        """Start progression quiz"""
        # Placeholder for future implementation
        messagebox.showinfo("Coming Soon", "Progression quiz will be available in the next update!")

    def show_piano_key_info(self, note):
        """Show information about a piano key"""
        info = f"Piano Key: {note}\n\n"
        info += "This key corresponds to the musical note "
        info += f"{note[0]} in octave {note[1]}."
        messagebox.showinfo("Piano Key Info", info)

    def highlight_notes_on_piano(self, notes):
        """Highlight notes on the piano keyboard"""
        # Reset all keys
        for note, key_btn in self.piano_keys.items():
            if '#' in note:
                key_btn.configure(fg_color="black", text_color="white")
            else:
                key_btn.configure(fg_color="white", text_color="black")

        # Highlight specified notes
        for note in notes:
            if note in self.piano_keys:
                key_btn = self.piano_keys[note]
                if '#' in note:
                    key_btn.configure(fg_color="#FF6B6B", text_color="white")  # Red for black keys
                else:
                    key_btn.configure(fg_color="#4CAF50", text_color="white")  # Green for white keys

    def update_piano_from_tabs(self):
        """Update piano highlighting based on current tab selections"""
        # Get current tab
        current_tab = self.tabview.get()

        if current_tab == "Scale Explorer" and self.current_scale:
            self.highlight_notes_on_piano(self.current_scale.notes)
        elif current_tab == "Chord Builder" and self.current_chord:
            self.highlight_notes_on_piano(self.current_chord.notes)
        elif current_tab == "Progression Analyzer" and self.current_progression:
            # Highlight all notes from the progression
            all_notes = set()
            for chord_name in self.current_progression['chords']:
                if chord_name in chords_data:
                    all_notes.update(chords_data[chord_name])
            self.highlight_notes_on_piano(list(all_notes))

    def test_audio(self):
        """Test audio functionality"""
        print("Testing audio...")
        success = audio_player.play_note("C4", 0.5)
        if success:
            messagebox.showinfo("Audio Test", "✅ Audio is working!\n\nYou should have heard a C note.")
        else:
            messagebox.showwarning("Audio Test", "❌ Audio test failed.\n\nCheck system audio settings.")

    def show_welcome(self):
        """Show modern welcome message with improved styling"""
        welcome = ctk.CTkToplevel(self)
        welcome.title("🎸 Music Theory Engine - Professional Edition")
        welcome.geometry("550x380")
        welcome.grab_set()
        welcome.configure(fg_color=COLORS['background'])

        # Modern header with gradient effect
        header_frame = ctk.CTkFrame(
            welcome,
            fg_color=COLORS['primary'],
            height=80,
            corner_radius=15
        )
        header_frame.pack(fill="x", padx=20, pady=(20, 0))
        header_frame.pack_propagate(False)

        title = ctk.CTkLabel(
            header_frame,
            text="🎸 Music Theory Engine",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="white"
        )
        title.pack(pady=(15, 0))

        subtitle = ctk.CTkLabel(
            header_frame,
            text="Professional Edition",
            font=ctk.CTkFont(size=12),
            text_color=COLORS['primary_light']
        )
        subtitle.pack(pady=(0, 15))

        # Content area
        content_frame = ctk.CTkFrame(welcome, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=(15, 20))

        features_title = ctk.CTkLabel(
            content_frame,
            text="✨ Your Professional Music Theory Companion",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=COLORS['text_primary']
        )
        features_title.pack(pady=(0, 10))

        features = ctk.CTkLabel(
            content_frame,
            text="• 🎼 60+ Scales (Major, Minor, Modal, Exotic)\n"
                 "• 🎸 100+ Chords with instant playback\n"
                 "• 🪕 Interactive fretboard + piano keyboard\n"
                 "• 📍 Scale positions and patterns\n"
                 "• 🎯 Theory exercises with progress tracking\n"
                 "• 🎶 Custom progressions with drag & drop\n"
                 "• 💾 Advanced preset system\n"
                 "• 🎨 Modern professional interface",
            font=ctk.CTkFont(size=11),
            text_color=COLORS['text_secondary'],
            justify="left",
            anchor="w"
        )
        features.pack(pady=(0, 15), padx=10, anchor="w")

        # Quick start guide
        guide_frame = ctk.CTkFrame(
            content_frame,
            fg_color=COLORS['surface_hover'],
            corner_radius=8
        )
        guide_frame.pack(fill="x", pady=(0, 15))

        guide_title = ctk.CTkLabel(
            guide_frame,
            text="🚀 Quick Start:",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=COLORS['primary']
        )
        guide_title.pack(anchor="w", padx=10, pady=(10, 5))

        guide_text = ctk.CTkLabel(
            guide_frame,
            text="1. Scale Explorer → Select scale → Choose playback → Play\n"
                 "2. Chord Builder → Pick chord → Transpose → Play\n"
                 "3. Fretboard → See notes visually + piano keyboard\n"
                 "4. Exercises → Test your music theory knowledge",
            font=ctk.CTkFont(size=10),
            text_color=COLORS['text_secondary'],
            justify="left",
            anchor="w"
        )
        guide_text.pack(anchor="w", padx=10, pady=(0, 10))

        # Tip section
        tip_frame = ctk.CTkFrame(
            content_frame,
            fg_color=COLORS['primary_light'],
            corner_radius=8
        )
        tip_frame.pack(fill="x", pady=(0, 15))

        tip_title = ctk.CTkLabel(
            tip_frame,
            text="💡 Pro Tip:",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=COLORS['primary']
        )
        tip_title.pack(anchor="w", padx=10, pady=(10, 5))

        tip_text = ctk.CTkLabel(
            tip_frame,
            text="Hover over buttons to see helpful tooltips explaining each feature!",
            font=ctk.CTkFont(size=10),
            text_color=COLORS['text_primary']
        )
        tip_text.pack(anchor="w", padx=10, pady=(0, 10))

        # Get started button
        close_btn = ctk.CTkButton(
            welcome,
            text="🚀 Get Started!",
            command=welcome.destroy,
            fg_color=COLORS['primary'],
            hover_color=COLORS['primary_hover'],
            height=45,
            font=ctk.CTkFont(size=12, weight="bold")
        )
        close_btn.pack(pady=(0, 20))
        self.create_tooltip(close_btn, "Start exploring music theory!")

def main():
    """Main application entry point"""
    try:
        app = MusicTheoryApp()
        app.mainloop()
    except Exception as e:
        print(f"Error starting application: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()