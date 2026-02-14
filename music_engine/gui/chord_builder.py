"""
Chord Builder GUI component.

This module provides an interactive interface for building
and exploring musical chords.
"""

import customtkinter as ctk
from typing import List, Optional
import sys
import os

# Import modules
from ..models.chord import Chord
from ..core.chords import ChordBuilder as ChordBuilderCore
from ..utils.audio import play_chord
from ..utils.preset_manager import get_preset_manager


class ChordBuilder(ctk.CTkFrame):
    """
    Interactive chord building interface.

    Features:
    - Root note selection
    - Chord quality selection
    - Visual display of notes and intervals
    - Inversion options
    - Guitar voicing suggestions
    """

    def __init__(self, parent):
        super().__init__(parent)

        # Pack this frame to fill the parent tab
        self.pack(fill="both", expand=True)

        # Chord data
        self.current_chord: Optional[Chord] = None
        self.fretboard_callback = None  # Callback for fretboard visualization

        # Available options
        self.root_notes = ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B']
        self.chord_qualities = [
            'maj', 'min', 'dim', 'aug', 'sus2', 'sus4', '5',
            'maj7', 'dom7', 'min7', 'dim7', 'min7b5', 'maj7b5',
            '7sus4', '9', 'min9', 'maj9', '11', 'min11', 'maj11',
            '13', 'min13', 'maj13', '6', 'min6', '6/9'
        ]

        self.chord_names = {
            'maj': 'Major', 'min': 'Minor', 'dim': 'Diminished', 'aug': 'Augmented',
            'sus2': 'Suspended 2nd', 'sus4': 'Suspended 4th', '5': 'Power Chord (5th)',
            'maj7': 'Major 7th', 'dom7': 'Dominant 7th', 'min7': 'Minor 7th',
            'dim7': 'Diminished 7th', 'min7b5': 'Minor 7th Flat 5', 'maj7b5': 'Major 7th Flat 5',
            '7sus4': '7th Suspended 4th', '9': 'Dominant 9th', 'min9': 'Minor 9th',
            'maj9': 'Major 9th', '11': 'Dominant 11th', 'min11': 'Minor 11th',
            'maj11': 'Major 11th', '13': 'Dominant 13th', 'min13': 'Minor 13th',
            'maj13': 'Major 13th', '6': 'Major 6th', 'min6': 'Minor 6th', '6/9': '6/9'
        }

        self.setup_ui()
        self.load_default_chord()

    def setup_ui(self):
        """Setup the user interface."""
        # Control panel
        self.control_frame = ctk.CTkFrame(self)
        self.control_frame.pack(fill="x", padx=20, pady=(20, 10))

        # Title
        self.title_label = ctk.CTkLabel(
            self.control_frame,
            text="Chord Builder",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.title_label.pack(pady=(10, 15))

        # Controls
        self.controls_frame = ctk.CTkFrame(self.control_frame)
        self.controls_frame.pack(fill="x", padx=20, pady=(0, 20))

        # Root note selection
        self.root_label = ctk.CTkLabel(self.controls_frame, text="Root Note:")
        self.root_label.pack(side="left", padx=(0, 10))

        self.root_var = ctk.StringVar(value="C")
        self.root_menu = ctk.CTkOptionMenu(
            self.controls_frame,
            values=self.root_notes,
            variable=self.root_var,
            command=self.on_chord_change
        )
        self.root_menu.pack(side="left", padx=(0, 20))

        # Chord quality selection
        self.quality_label = ctk.CTkLabel(self.controls_frame, text="Chord Quality:")
        self.quality_label.pack(side="left", padx=(0, 10))

        self.quality_var = ctk.StringVar(value="maj")
        self.quality_menu = ctk.CTkOptionMenu(
            self.controls_frame,
            values=list(self.chord_names.values()),
            variable=self.quality_var,
            command=self.on_chord_change
        )
        self.quality_menu.pack(side="left", padx=(0, 20))

        # Inversion selection
        self.inversion_label = ctk.CTkLabel(self.controls_frame, text="Inversion:")
        self.inversion_label.pack(side="left", padx=(0, 10))

        self.inversion_var = ctk.IntVar(value=0)
        self.inversion_menu = ctk.CTkOptionMenu(
            self.controls_frame,
            values=["Root Position", "1st Inversion", "2nd Inversion", "3rd Inversion"],
            variable=self.inversion_var,
            command=self.on_inversion_change
        )
        self.inversion_menu.pack(side="left", padx=(0, 20))

        # Update button
        self.update_button = ctk.CTkButton(
            self.controls_frame,
            text="Update",
            command=self.on_chord_change
        )
        self.update_button.pack(side="right", padx=(0, 10))

        # Transpose buttons
        self.transpose_down_button = ctk.CTkButton(
            self.controls_frame,
            text="⬇️",
            command=lambda: self.transpose_chord(-1),
            width=40,
            fg_color="#8B4513",
            hover_color="#A0522D"
        )
        self.transpose_down_button.pack(side="right", padx=(0, 5))

        self.transpose_label = ctk.CTkLabel(self.controls_frame, text="Transpose")
        self.transpose_label.pack(side="right", padx=(0, 5))

        self.transpose_up_button = ctk.CTkButton(
            self.controls_frame,
            text="⬆️",
            command=lambda: self.transpose_chord(1),
            width=40,
            fg_color="#8B4513",
            hover_color="#A0522D"
        )
        self.transpose_up_button.pack(side="right", padx=(0, 10))

        # Play chord button
        self.play_button = ctk.CTkButton(
            self.controls_frame,
            text="🔊 Play Chord",
            command=self.play_chord,
            fg_color="#2E8B57",
            hover_color="#3CB371"
        )
        self.play_button.pack(side="right", padx=(0, 10))

        # Show on fretboard button
        self.fretboard_button = ctk.CTkButton(
            self.controls_frame,
            text="Show on Fretboard",
            command=self.show_on_fretboard
        )
        self.fretboard_button.pack(side="right")

        # Information display
        self.info_frame = ctk.CTkFrame(self)
        self.info_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # Chord info
        self.chord_info_label = ctk.CTkLabel(
            self.info_frame,
            text="Chord Information",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.chord_info_label.pack(pady=(20, 10))

        # Basic info
        self.basic_frame = ctk.CTkFrame(self.info_frame)
        self.basic_frame.pack(fill="x", padx=20, pady=(0, 15))

        self.name_label = ctk.CTkLabel(
            self.basic_frame,
            text="Name:",
            font=ctk.CTkFont(weight="bold")
        )
        self.name_label.pack(anchor="w", padx=10, pady=(10, 5))

        self.name_display = ctk.CTkLabel(
            self.basic_frame,
            text="",
            font=ctk.CTkFont(size=14)
        )
        self.name_display.pack(anchor="w", padx=10, pady=(0, 10))

        self.notes_label = ctk.CTkLabel(
            self.basic_frame,
            text="Notes:",
            font=ctk.CTkFont(weight="bold")
        )
        self.notes_label.pack(anchor="w", padx=10, pady=(0, 5))

        self.notes_display = ctk.CTkLabel(
            self.basic_frame,
            text="",
            font=ctk.CTkFont(size=14)
        )
        self.notes_display.pack(anchor="w", padx=10, pady=(0, 10))

        self.intervals_label = ctk.CTkLabel(
            self.basic_frame,
            text="Intervals:",
            font=ctk.CTkFont(weight="bold")
        )
        self.intervals_label.pack(anchor="w", padx=10, pady=(0, 5))

        self.intervals_display = ctk.CTkLabel(
            self.basic_frame,
            text="",
            font=ctk.CTkFont(size=14)
        )
        self.intervals_display.pack(anchor="w", padx=10, pady=(0, 10))

        # Guitar voicings
        self.voicings_frame = ctk.CTkFrame(self.info_frame)
        self.voicings_frame.pack(fill="x", padx=20, pady=(0, 15))

        self.voicings_label = ctk.CTkLabel(
            self.voicings_frame,
            text="Guitar Voicing Suggestions:",
            font=ctk.CTkFont(weight="bold")
        )
        self.voicings_label.pack(anchor="w", padx=10, pady=(10, 5))

        self.voicings_display = ctk.CTkTextbox(
            self.voicings_frame,
            height=80,
            wrap="word"
        )
        self.voicings_display.pack(fill="x", padx=10, pady=(0, 10))

        # Extensions and alterations
        self.extensions_frame = ctk.CTkFrame(self.info_frame)
        self.extensions_frame.pack(fill="x", padx=20, pady=(0, 20))

        self.extensions_label = ctk.CTkLabel(
            self.extensions_frame,
            text="Possible Extensions:",
            font=ctk.CTkFont(weight="bold")
        )
        self.extensions_label.pack(anchor="w", padx=10, pady=(10, 5))

        self.extensions_display = ctk.CTkTextbox(
            self.extensions_frame,
            height=60,
            wrap="word"
        )
        self.extensions_display.pack(fill="x", padx=10, pady=(0, 10))

    def load_default_chord(self):
        """Load the default C major chord."""
        try:
            self.current_chord = ChordBuilderCore.major('C')
            self.update_display()
        except Exception as e:
            print(f"Error loading default chord: {e}")
            import traceback
            traceback.print_exc()

    def on_chord_change(self, *args):
        """Handle chord selection change."""
        try:
            root = self.root_var.get()
            quality_display = self.quality_var.get()

            # Find the internal quality
            quality = None
            for key, value in self.chord_names.items():
                if value == quality_display:
                    quality = key
                    break

            if quality:
                # Map quality codes to ChordBuilder methods
                quality_to_method = {
                    'maj': 'major', 'min': 'minor', 'dim': 'diminished', 'aug': 'augmented',
                    'sus2': 'suspended2', 'sus4': 'suspended4', '5': 'power_chord',
                    'maj7': 'major7', 'dom7': 'dominant7', 'min7': 'minor7',
                    'dim7': 'diminished7', 'min7b5': 'minor7b5', 'maj7b5': 'major7b5',
                    '7sus4': 'seven_sus4', '9': 'dom9', 'min9': 'minor9',
                    'maj9': 'major9', '11': 'dom11', 'min11': 'minor11',
                    'maj11': 'major11', '13': 'dom13', 'min13': 'minor13',
                    'maj13': 'major13', '6': 'sixth', 'min6': 'minor6', '6/9': 'six_nine'
                }

                method_name = quality_to_method.get(quality)
                if method_name:
                    try:
                        chord_method = getattr(ChordBuilderCore, method_name)
                        base_chord = chord_method(root)
                        # Apply inversion if selected
                        inversion = self.inversion_var.get()
                        if inversion > 0 and hasattr(base_chord, 'get_inversion'):
                            self.current_chord = base_chord.get_inversion(inversion)
                        else:
                            self.current_chord = base_chord
                        self.update_display()
                    except AttributeError:
                        print(f"Chord method {method_name} not found in ChordBuilder")
                        self.current_chord = None
                    except Exception as e:
                        print(f"Error creating chord: {e}")
                        self.current_chord = None
                else:
                    print(f"No mapping found for quality: {quality}")
                    self.current_chord = None
        except Exception as e:
            print(f"Error changing chord: {e}")
            import traceback
            traceback.print_exc()

    def on_inversion_change(self, *args):
        """Handle inversion change."""
        self.on_chord_change()

    def update_display(self):
        """Update the display with current chord information."""
        if not self.current_chord:
            return

        # Update basic info
        self.name_display.configure(text=self.current_chord.name)
        self.notes_display.configure(text=" ".join(self.current_chord.note_names))

        # Update intervals
        intervals_str = " ".join([f"{i}semitones" for i in self.current_chord.intervals])
        self.intervals_display.configure(text=intervals_str)

        # Update voicings
        voicing_text = self.get_guitar_voicings()
        self.voicings_display.delete("1.0", "end")
        self.voicings_display.insert("1.0", voicing_text)

        # Update extensions
        extensions_text = self.get_extensions()
        self.extensions_display.delete("1.0", "end")
        self.extensions_display.insert("1.0", extensions_text)

    def get_guitar_voicings(self) -> str:
        """Get guitar voicing suggestions."""
        if not self.current_chord:
            return "No chord selected"

        # Simple voicing suggestions based on chord type
        voicings = []

        if len(self.current_chord) <= 4:  # Basic chords
            if self.current_chord.quality in ['maj', 'min', 'dom7', 'min7', 'maj7']:
                voicings.append("Open chord position (if applicable)")
                voicings.append("Barre chord at appropriate fret")
            else:
                voicings.append("Barre chord formation")
        else:  # Extended chords
            voicings.append("Extended chords often require:")
            voicings.append("- Partial barre techniques")
            voicings.append("- Multi-position fingering")
            voicings.append("- Capo usage for easier playing")

        return "\n".join(voicings)

    def get_extensions(self) -> str:
        """Get possible extensions for the current chord."""
        if not self.current_chord:
            return "No chord selected"

        try:
            extensions = self.current_chord.get_extensions()
            if extensions:
                return "\n".join([f"- {ext}" for ext in extensions])
            else:
                return "No common extensions available"
        except:
            return "Extensions not available for this chord type"

    def set_fretboard_callback(self, callback):
        """Set callback for fretboard visualization."""
        self.fretboard_callback = callback

    def show_on_fretboard(self):
        """Show current chord on fretboard."""
        if self.current_chord and self.fretboard_callback:
            try:
                chord_notes = [note for note in self.current_chord.notes]
                root_note = self.current_chord.root
                self.fretboard_callback(chord_notes, root_note)
            except Exception as e:
                print(f"Error sending chord to fretboard: {e}")

    def play_chord(self):
        """Play the current chord."""
        if self.current_chord:
            try:
                # Convert chord notes to string format for audio player
                note_strings = [str(note) for note in self.current_chord.notes]
                play_chord(note_strings, duration=2.0)
                print(f"Playing chord: {self.current_chord.name}")

                # Visual feedback
                original_text = self.play_button.cget("text")
                self.play_button.configure(text="Playing...", fg_color="#FF6B35")
                self.after(3000, lambda: self.play_button.configure(text=original_text, fg_color="#2E8B57"))

            except Exception as e:
                print(f"Error playing chord: {e}")
                # Show error feedback with message
                original_text = self.play_button.cget("text")
                self.play_button.configure(text="No Audio", fg_color="#DC143C")
                self.after(3000, lambda: self.play_button.configure(text=original_text, fg_color="#2E8B57"))
        else:
            print("No chord to play")

    def transpose_chord(self, semitones: int):
        """Transpose the current chord by the given number of semitones."""
        if self.current_chord:
            try:
                # Create transposed chord
                transposed_root = self.current_chord.root.transpose(semitones)
                transposed_chord = ChordBuilderCore.from_quality(str(transposed_root), self.quality_var.get())

                # Apply inversion if needed
                inversion = self.inversion_var.get()
                if inversion > 0 and hasattr(transposed_chord, 'get_inversion'):
                    transposed_chord = transposed_chord.get_inversion(inversion)

                # Update current chord
                self.current_chord = transposed_chord

                # Update the root note selector to match the new root
                new_root = str(transposed_chord.root.note_name)
                if new_root in self.root_notes:
                    self.root_var.set(new_root)

                # Update display
                self.update_display()

                print(f"Transposed chord: {transposed_chord.name}")

            except Exception as e:
                print(f"Error transposing chord: {e}")
        else:
            print("No chord to transpose")

    def save_preset(self, name: str, description: str = "") -> bool:
        """
        Save current chord configuration as a preset.

        Args:
            name: Preset name
            description: Optional description

        Returns:
            True if successful, False otherwise
        """
        try:
            preset_manager = get_preset_manager()

            # Get current state
            state = self.get_current_state()

            return preset_manager.save_preset(
                category='chords',
                name=name,
                data=state,
                description=description
            )
        except Exception as e:
            print(f"Error saving chord preset: {e}")
            return False

    def load_preset(self, name: str) -> bool:
        """
        Load a chord preset.

        Args:
            name: Preset name

        Returns:
            True if successful, False otherwise
        """
        try:
            preset_manager = get_preset_manager()

            preset = preset_manager.load_preset('chords', name)
            if not preset:
                return False

            # Apply preset state
            return self.apply_state(preset['data'])

        except Exception as e:
            print(f"Error loading chord preset: {e}")
            return False

    def get_current_state(self) -> dict:
        """
        Get current chord builder state for saving.

        Returns:
            Dictionary containing current state
        """
        state = {
            'root_note': getattr(self.root_var, 'get', lambda: 'C')(),
            'chord_type': getattr(self.chord_var, 'get', lambda: 'maj')(),
            'selected_chord': self.current_chord.name if self.current_chord else None,
            'octave': getattr(self.octave_var, 'get', lambda: 4)()
        }
        return state

    def apply_state(self, state: dict) -> bool:
        """
        Apply a saved state to the chord builder.

        Args:
            state: State dictionary

        Returns:
            True if successful, False otherwise
        """
        try:
            # Set root note
            if 'root_note' in state and hasattr(self, 'root_var'):
                self.root_var.set(state['root_note'])

            # Set chord type
            if 'chord_type' in state and hasattr(self, 'chord_var'):
                self.chord_var.set(state['chord_type'])

            # Set octave
            if 'octave' in state and hasattr(self, 'octave_var'):
                self.octave_var.set(state['octave'])

            # Update chord display
            self.update_chord()

            return True

        except Exception as e:
            print(f"Error applying chord state: {e}")
            return False

    def get_export_data(self) -> str:
        """Get data for export."""
        if not self.current_chord:
            return "No chord data to export"

        data = f"Chord: {self.current_chord.name}\n"
        data += f"Notes: {' '.join(self.current_chord.note_names)}\n"
        data += f"Intervals: {' '.join(str(i) for i in self.current_chord.intervals)}\n"
        data += f"Inversion: {'Yes' if self.current_chord.is_inverted else 'No'}\n\n"

        data += "Guitar Voicings:\n"
        data += self.get_guitar_voicings()
        data += "\n\n"

        data += "Possible Extensions:\n"
        data += self.get_extensions()
        data += "\n"

        return data
