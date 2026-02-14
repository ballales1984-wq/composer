"""
Arpeggio Viewer GUI component.

This module provides an interactive interface for creating
and visualizing musical arpeggios.
"""

import customtkinter as ctk
from typing import List, Optional
import sys
import os

# Import modules
from ..models.arpeggio import Arpeggio
from ..core.arpeggios import ArpeggioBuilder
from ..utils.preset_manager import get_preset_manager


class ArpeggioViewer(ctk.CTkFrame):
    """
    Interactive arpeggio creation and visualization interface.

    Features:
    - Arpeggio creation from chords or scales
    - Direction selection (up, down, up_down, etc.)
    - Octave range control
    - Visual display of note sequence
    - Guitar position suggestions
    """

    def __init__(self, parent):
        super().__init__(parent)

        # Pack this frame to fill the parent tab
        self.pack(fill="both", expand=True)

        # Arpeggio data
        self.current_arpeggio: Optional[Arpeggio] = None
        self.fretboard_callback = None  # Callback for fretboard visualization

        # Available options
        self.directions = ['up', 'down', 'up_down', 'down_up']
        self.direction_names = {
            'up': 'Up',
            'down': 'Down',
            'up_down': 'Up-Down',
            'down_up': 'Down-Up'
        }

        self.source_types = ['chord', 'scale']
        self.chord_qualities = ['maj', 'min', 'dom7', 'min7', 'maj7', 'dim7']
        self.scale_types = ['major', 'minor_natural', 'dorian', 'mixolydian', 'blues_minor']

        self.setup_ui()
        self.load_default_arpeggio()

    def setup_ui(self):
        """Setup the user interface."""
        # Control panel
        self.control_frame = ctk.CTkFrame(self)
        self.control_frame.pack(fill="x", padx=20, pady=(20, 10))

        # Title
        self.title_label = ctk.CTkLabel(
            self.control_frame,
            text="Arpeggio Viewer",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.title_label.pack(pady=(10, 15))

        # Source selection
        self.source_frame = ctk.CTkFrame(self.control_frame)
        self.source_frame.pack(fill="x", padx=20, pady=(0, 15))

        self.source_type_label = ctk.CTkLabel(
            self.source_frame,
            text="Source Type:",
            font=ctk.CTkFont(weight="bold")
        )
        self.source_type_label.pack(anchor="w", padx=10, pady=(10, 5))

        self.source_type_var = ctk.StringVar(value="chord")
        self.source_type_menu = ctk.CTkOptionMenu(
            self.source_frame,
            values=["Chord", "Scale"],
            variable=self.source_type_var,
            command=self.on_source_type_change
        )
        self.source_type_menu.pack(anchor="w", padx=10, pady=(0, 10))

        # Chord/Scale selection
        self.selection_frame = ctk.CTkFrame(self.control_frame)
        self.selection_frame.pack(fill="x", padx=20, pady=(0, 15))

        # Root note
        self.root_label = ctk.CTkLabel(self.selection_frame, text="Root Note:")
        self.root_label.pack(side="left", padx=(10, 5))

        self.root_notes = ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B']
        self.root_var = ctk.StringVar(value="C")
        self.root_menu = ctk.CTkOptionMenu(
            self.selection_frame,
            values=self.root_notes,
            variable=self.root_var,
            command=self.on_selection_change
        )
        self.root_menu.pack(side="left", padx=(0, 15))

        # Quality/Type
        self.quality_label = ctk.CTkLabel(self.selection_frame, text="Quality/Type:")
        self.quality_label.pack(side="left", padx=(0, 5))

        self.quality_var = ctk.StringVar(value="maj")
        self.quality_menu = ctk.CTkOptionMenu(
            self.selection_frame,
            values=["Major", "Minor", "Dominant 7th", "Minor 7th", "Major 7th", "Diminished 7th"],
            variable=self.quality_var,
            command=self.on_selection_change
        )
        self.quality_menu.pack(side="left", padx=(0, 15))

        # Direction
        self.direction_label = ctk.CTkLabel(self.selection_frame, text="Direction:")
        self.direction_label.pack(side="left", padx=(0, 5))

        self.direction_var = ctk.StringVar(value="up")
        self.direction_menu = ctk.CTkOptionMenu(
            self.selection_frame,
            values=list(self.direction_names.values()),
            variable=self.direction_var,
            command=self.on_selection_change
        )
        self.direction_menu.pack(side="left", padx=(0, 15))

        # Octaves
        self.octaves_label = ctk.CTkLabel(self.selection_frame, text="Octaves:")
        self.octaves_label.pack(side="left", padx=(0, 5))

        self.octaves_var = ctk.IntVar(value=1)
        self.octaves_menu = ctk.CTkOptionMenu(
            self.selection_frame,
            values=["1", "2", "3"],
            variable=self.octaves_var,
            command=self.on_selection_change
        )
        self.octaves_menu.pack(side="left", padx=(0, 10))

        # Update button
        self.update_button = ctk.CTkButton(
            self.selection_frame,
            text="Generate",
            command=self.generate_arpeggio
        )
        self.update_button.pack(side="right", padx=(0, 10))

        # Show on fretboard button
        self.fretboard_button = ctk.CTkButton(
            self.selection_frame,
            text="Show on Fretboard",
            command=self.show_on_fretboard
        )
        self.fretboard_button.pack(side="right")

        # Results display
        self.results_frame = ctk.CTkFrame(self)
        self.results_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # Arpeggio info
        self.arpeggio_info_label = ctk.CTkLabel(
            self.results_frame,
            text="Arpeggio Information",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.arpeggio_info_label.pack(pady=(20, 10))

        # Basic info
        self.basic_frame = ctk.CTkFrame(self.results_frame)
        self.basic_frame.pack(fill="x", padx=20, pady=(0, 15))

        self.name_label = ctk.CTkLabel(
            self.basic_frame,
            text="Arpeggio:",
            font=ctk.CTkFont(weight="bold")
        )
        self.name_label.pack(anchor="w", padx=10, pady=(10, 5))

        self.name_display = ctk.CTkLabel(
            self.basic_frame,
            text="No arpeggio generated",
            font=ctk.CTkFont(size=14)
        )
        self.name_display.pack(anchor="w", padx=10, pady=(0, 10))

        self.notes_label = ctk.CTkLabel(
            self.basic_frame,
            text="Note Sequence:",
            font=ctk.CTkFont(weight="bold")
        )
        self.notes_label.pack(anchor="w", padx=10, pady=(0, 5))

        self.notes_display = ctk.CTkTextbox(
            self.basic_frame,
            height=60,
            wrap="word"
        )
        self.notes_display.pack(fill="x", padx=10, pady=(0, 10))

        # Guitar positions
        self.positions_frame = ctk.CTkFrame(self.results_frame)
        self.positions_frame.pack(fill="x", padx=20, pady=(0, 15))

        self.positions_label = ctk.CTkLabel(
            self.positions_frame,
            text="Guitar Playing Tips:",
            font=ctk.CTkFont(weight="bold")
        )
        self.positions_label.pack(anchor="w", padx=10, pady=(10, 5))

        self.positions_display = ctk.CTkTextbox(
            self.positions_frame,
            height=80,
            wrap="word"
        )
        self.positions_display.pack(fill="x", padx=10, pady=(0, 10))

        # Technique suggestions
        self.technique_frame = ctk.CTkFrame(self.results_frame)
        self.technique_frame.pack(fill="x", padx=20, pady=(0, 20))

        self.technique_label = ctk.CTkLabel(
            self.technique_frame,
            text="Suggested Techniques:",
            font=ctk.CTkFont(weight="bold")
        )
        self.technique_label.pack(anchor="w", padx=10, pady=(10, 5))

        self.technique_display = ctk.CTkTextbox(
            self.technique_frame,
            height=60,
            wrap="word"
        )
        self.technique_display.pack(fill="x", padx=10, pady=(0, 10))

    def load_default_arpeggio(self):
        """Load a default C major arpeggio."""
        try:
            self.current_arpeggio = ArpeggioBuilder.major_triad('C', 'up')
            self.update_display()
        except Exception as e:
            print(f"Error loading default arpeggio: {e}")

    def on_source_type_change(self, *args):
        """Handle source type change."""
        source_type = self.source_type_var.get().lower()

        if source_type == "chord":
            self.quality_menu.configure(values=["Major", "Minor", "Dominant 7th", "Minor 7th", "Major 7th", "Diminished 7th"])
            self.quality_var.set("Major")
        else:  # scale
            self.quality_menu.configure(values=["Major", "Natural Minor", "Dorian", "Mixolydian", "Minor Blues"])
            self.quality_var.set("Major")

        self.on_selection_change()

    def on_selection_change(self, *args):
        """Handle selection changes."""
        # This will be called when selections change, but we'll generate on button press
        pass

    def generate_arpeggio(self):
        """Generate the arpeggio based on current selections."""
        try:
            root = self.root_var.get()
            source_type = self.source_type_var.get().lower()
            direction_display = self.direction_var.get()
            octaves = self.octaves_var.get()

            # Find internal direction
            direction = None
            for key, value in self.direction_names.items():
                if value == direction_display:
                    direction = key
                    break

            # Find internal quality/type
            quality_display = self.quality_var.get()
            quality_map = {
                "Major": "maj", "Minor": "min", "Dominant 7th": "dom7",
                "Minor 7th": "min7", "Major 7th": "maj7", "Diminished 7th": "dim7",
                "Natural Minor": "minor_natural", "Dorian": "dorian",
                "Mixolydian": "mixolydian", "Minor Blues": "blues_minor"
            }
            quality = quality_map.get(quality_display, "maj")

            # Generate arpeggio
            if source_type == "chord":
                self.current_arpeggio = ArpeggioBuilder.from_chord(f"{root}{quality}", direction, octaves)
            else:  # scale
                scale_type = quality if quality in ['major', 'minor_natural', 'dorian', 'mixolydian', 'blues_minor'] else 'major'
                self.current_arpeggio = ArpeggioBuilder.from_scale(f"{root} {scale_type}", direction, octaves)

            self.update_display()

        except Exception as e:
            print(f"Error generating arpeggio: {e}")

    def update_display(self):
        """Update the display with current arpeggio information."""
        if not self.current_arpeggio:
            return

        # Update basic info
        self.name_display.configure(text=str(self.current_arpeggio))

        # Update note sequence
        notes_text = ""
        for i, note in enumerate(self.current_arpeggio.notes, 1):
            notes_text += f"{i}. {note.name}\n"

        self.notes_display.delete("1.0", "end")
        self.notes_display.insert("1.0", notes_text.strip())

        # Update guitar positions
        positions_text = self.get_guitar_positions()
        self.positions_display.delete("1.0", "end")
        self.positions_display.insert("1.0", positions_text)

        # Update techniques
        techniques_text = self.get_techniques()
        self.technique_display.delete("1.0", "end")
        self.technique_display.insert("1.0", techniques_text)

    def get_guitar_positions(self) -> str:
        """Get guitar position suggestions."""
        if not self.current_arpeggio:
            return "No arpeggio generated"

        source = self.current_arpeggio.source
        direction = self.current_arpeggio.direction

        tips = []

        if hasattr(source, 'quality'):  # It's a chord
            if len(source) <= 4:
                tips.append("Start with basic chord shape and lift fingers in sequence")
                tips.append("Use metronome for consistent timing")
            else:
                tips.append("Extended chords may require position shifts")
                tips.append("Consider using capo for easier playing")
        else:  # It's a scale
            tips.append("Practice scale positions first, then arpeggiate")
            tips.append("Focus on smooth transitions between notes")

        if direction in ['up_down', 'down_up']:
            tips.append("Pay attention to smooth direction changes")
            tips.append("Use alternate picking for even timing")

        tips.append(f"Total notes: {len(self.current_arpeggio)}")
        tips.append(f"Direction: {direction.replace('_', '-')}")

        return "\n".join(tips)

    def get_techniques(self) -> str:
        """Get suggested playing techniques."""
        if not self.current_arpeggio:
            return "No arpeggio generated"

        source = self.current_arpeggio.source
        length = len(self.current_arpeggio)

        techniques = []

        # Basic techniques
        techniques.append("Alternate picking (down-up-down-up)")
        techniques.append("Use metronome for timing")

        # Advanced techniques based on arpeggio
        if length > 8:
            techniques.append("Sweep picking for fast passages")
            techniques.append("Finger independence exercises")

        if hasattr(source, 'quality') and '7' in source.quality:
            techniques.append("Focus on smooth 7th intervals")

        # Direction-specific techniques
        if self.current_arpeggio.direction in ['up_down', 'down_up']:
            techniques.append("Economy picking for direction changes")
            techniques.append("Practice each direction separately first")

        return "\n".join(techniques)

    def save_preset(self, name: str, description: str = "") -> bool:
        """
        Save current arpeggio configuration as a preset.

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
                category='arpeggios',
                name=name,
                data=state,
                description=description
            )
        except Exception as e:
            print(f"Error saving arpeggio preset: {e}")
            return False

    def load_preset(self, name: str) -> bool:
        """
        Load an arpeggio preset.

        Args:
            name: Preset name

        Returns:
            True if successful, False otherwise
        """
        try:
            preset_manager = get_preset_manager()

            preset = preset_manager.load_preset('arpeggios', name)
            if not preset:
                return False

            # Apply preset state
            return self.apply_state(preset['data'])

        except Exception as e:
            print(f"Error loading arpeggio preset: {e}")
            return False

    def get_current_state(self) -> dict:
        """
        Get current arpeggio viewer state for saving.

        Returns:
            Dictionary containing current state
        """
        state = {
            'root_note': getattr(self.root_var, 'get', lambda: 'C')(),
            'arpeggio_type': getattr(self.arpeggio_var, 'get', lambda: 'major_triad')(),
            'direction': getattr(self.direction_var, 'get', lambda: 'up')(),
            'current_arpeggio': str(self.current_arpeggio) if self.current_arpeggio else None,
            'octave': getattr(self.octave_var, 'get', lambda: 4)()
        }
        return state

    def apply_state(self, state: dict) -> bool:
        """
        Apply a saved state to the arpeggio viewer.

        Args:
            state: State dictionary

        Returns:
            True if successful, False otherwise
        """
        try:
            # Set root note
            if 'root_note' in state and hasattr(self, 'root_var'):
                self.root_var.set(state['root_note'])

            # Set arpeggio type
            if 'arpeggio_type' in state and hasattr(self, 'arpeggio_var'):
                self.arpeggio_var.set(state['arpeggio_type'])

            # Set direction
            if 'direction' in state and hasattr(self, 'direction_var'):
                self.direction_var.set(state['direction'])

            # Set octave
            if 'octave' in state and hasattr(self, 'octave_var'):
                self.octave_var.set(state['octave'])

            # Update arpeggio display
            self.update_arpeggio()

            return True

        except Exception as e:
            print(f"Error applying arpeggio state: {e}")
            return False

    def get_export_data(self) -> str:
        """Get data for export."""
        if not self.current_arpeggio:
            return "No arpeggio data to export"

        data = f"Arpeggio: {self.current_arpeggio}\n"
        data += f"Direction: {self.current_arpeggio.direction.replace('_', '-')}\n"
        data += f"Source: {self.current_arpeggio.source}\n"
        data += f"Total notes: {len(self.current_arpeggio)}\n\n"

        data += "Note Sequence:\n"
        for i, note in enumerate(self.current_arpeggio.notes, 1):
            data += f"{i}. {note.name}\n"
        data += "\n"

        data += "Guitar Tips:\n"
        data += self.get_guitar_positions()
        data += "\n\n"

        data += "Techniques:\n"
        data += self.get_techniques()
        data += "\n"

        return data

    def set_fretboard_callback(self, callback):
        """Set callback for fretboard visualization."""
        self.fretboard_callback = callback

    def show_on_fretboard(self):
        """Show current arpeggio on fretboard."""
        if self.current_arpeggio and self.fretboard_callback:
            try:
                arpeggio_notes = [note for note in self.current_arpeggio.notes]
                self.fretboard_callback(arpeggio_notes)
            except Exception as e:
                print(f"Error sending arpeggio to fretboard: {e}")

    def export_fretboard_image(self, filename: str = "fretboard.png"):
        """Export the fretboard as an image."""
        try:
            # This would require PIL/Pillow to save the canvas as image
            # For now, just show a message
            print(f"Fretboard export to {filename} would be implemented here")
        except Exception as e:
            print(f"Export failed: {e}")
