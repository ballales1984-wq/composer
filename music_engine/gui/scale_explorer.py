"""
Scale Explorer GUI component.

This module provides an interactive interface for exploring
musical scales with visual feedback.
"""

import customtkinter as ctk
from typing import List, Optional
import sys
import os

# Import modules
from ..models.scale import Scale
from ..core.scales import ScaleBuilder as ScaleBuilderCore
from ..utils.audio import play_arpeggio
from ..utils.preset_manager import get_preset_manager


class ScaleExplorer(ctk.CTkFrame):
    """
    Interactive scale exploration interface.

    Features:
    - Root note selection
    - Scale type selection
    - Visual display of notes and intervals
    - Compatible chord display
    - Scale degree information
    """

    def __init__(self, parent):
        super().__init__(parent)

        # Pack this frame to fill the parent tab
        self.pack(fill="both", expand=True)

        # Scale data
        self.current_scale: Optional[Scale] = None
        self.fretboard_callback = None  # Callback for fretboard visualization

        # Available options
        self.root_notes = ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B']
        self.scale_types = [
            'major', 'minor_natural', 'minor_harmonic', 'minor_melodic',
            'dorian', 'phrygian', 'lydian', 'mixolydian', 'locrian',
            'pentatonic_major', 'pentatonic_minor', 'pentatonic_blues',
            'blues_major', 'blues_minor'
        ]

        self.scale_names = {
            'major': 'Major (Ionian)',
            'minor_natural': 'Natural Minor (Aeolian)',
            'minor_harmonic': 'Harmonic Minor',
            'minor_melodic': 'Melodic Minor',
            'dorian': 'Dorian',
            'phrygian': 'Phrygian',
            'lydian': 'Lydian',
            'mixolydian': 'Mixolydian',
            'locrian': 'Locrian',
            'pentatonic_major': 'Major Pentatonic',
            'pentatonic_minor': 'Minor Pentatonic',
            'pentatonic_blues': 'Blues Pentatonic',
            'blues_major': 'Major Blues',
            'blues_minor': 'Minor Blues'
        }

        self.setup_ui()
        self.load_default_scale()

    def setup_ui(self):
        """Setup the user interface."""
        # Control panel
        self.control_frame = ctk.CTkFrame(self)
        self.control_frame.pack(fill="x", padx=20, pady=(20, 10))

        # Title
        self.title_label = ctk.CTkLabel(
            self.control_frame,
            text="Scale Explorer",
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
            command=self.on_scale_change
        )
        self.root_menu.pack(side="left", padx=(0, 20))

        # Scale type selection
        self.scale_label = ctk.CTkLabel(self.controls_frame, text="Scale Type:")
        self.scale_label.pack(side="left", padx=(0, 10))

        self.scale_var = ctk.StringVar(value="major")
        self.scale_menu = ctk.CTkOptionMenu(
            self.controls_frame,
            values=list(self.scale_names.values()),
            variable=self.scale_var,
            command=self.on_scale_change
        )
        self.scale_menu.pack(side="left", padx=(0, 20))

        # Update button
        self.update_button = ctk.CTkButton(
            self.controls_frame,
            text="Update",
            command=self.on_scale_change
        )
        self.update_button.pack(side="right", padx=(0, 10))

        # Transpose buttons
        self.transpose_down_button = ctk.CTkButton(
            self.controls_frame,
            text="⬇️",
            command=lambda: self.transpose_scale(-1),
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
            command=lambda: self.transpose_scale(1),
            width=40,
            fg_color="#8B4513",
            hover_color="#A0522D"
        )
        self.transpose_up_button.pack(side="right", padx=(0, 10))

        # Relative scale button
        self.relative_button = ctk.CTkButton(
            self.controls_frame,
            text="Relative",
            command=self.show_relative_scale,
            fg_color="#9370DB",
            hover_color="#8A2BE2"
        )
        self.relative_button.pack(side="right", padx=(0, 10))

        # Play scale button
        self.play_button = ctk.CTkButton(
            self.controls_frame,
            text="🔊 Play Scale",
            command=self.play_scale,
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

        # Scale info
        self.scale_info_label = ctk.CTkLabel(
            self.info_frame,
            text="Scale Information",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.scale_info_label.pack(pady=(20, 10))

        # Notes display
        self.notes_frame = ctk.CTkFrame(self.info_frame)
        self.notes_frame.pack(fill="x", padx=20, pady=(0, 15))

        self.notes_label = ctk.CTkLabel(
            self.notes_frame,
            text="Notes:",
            font=ctk.CTkFont(weight="bold")
        )
        self.notes_label.pack(anchor="w", padx=10, pady=(10, 5))

        self.notes_display = ctk.CTkLabel(
            self.notes_frame,
            text="",
            font=ctk.CTkFont(size=14)
        )
        self.notes_display.pack(anchor="w", padx=10, pady=(0, 10))

        # Intervals display
        self.intervals_label = ctk.CTkLabel(
            self.notes_frame,
            text="Intervals:",
            font=ctk.CTkFont(weight="bold")
        )
        self.intervals_label.pack(anchor="w", padx=10, pady=(0, 5))

        self.intervals_display = ctk.CTkLabel(
            self.notes_frame,
            text="",
            font=ctk.CTkFont(size=14)
        )
        self.intervals_display.pack(anchor="w", padx=10, pady=(0, 10))

        # Scale degrees
        self.degrees_frame = ctk.CTkFrame(self.info_frame)
        self.degrees_frame.pack(fill="x", padx=20, pady=(0, 15))

        self.degrees_label = ctk.CTkLabel(
            self.degrees_frame,
            text="Scale Degrees:",
            font=ctk.CTkFont(weight="bold")
        )
        self.degrees_label.pack(anchor="w", padx=10, pady=(10, 5))

        self.degrees_display = ctk.CTkTextbox(
            self.degrees_frame,
            height=60,
            wrap="word"
        )
        self.degrees_display.pack(fill="x", padx=10, pady=(0, 10))

        # Compatible chords
        self.chords_frame = ctk.CTkFrame(self.info_frame)
        self.chords_frame.pack(fill="x", padx=20, pady=(0, 20))

        self.chords_label = ctk.CTkLabel(
            self.chords_frame,
            text="Compatible Chords:",
            font=ctk.CTkFont(weight="bold")
        )
        self.chords_label.pack(anchor="w", padx=10, pady=(10, 5))

        self.chords_display = ctk.CTkTextbox(
            self.chords_frame,
            height=80,
            wrap="word"
        )
        self.chords_display.pack(fill="x", padx=10, pady=(0, 10))

    def load_default_scale(self):
        """Load the default C major scale."""
        try:
            self.current_scale = ScaleBuilderCore.major('C')
            self.update_display()
        except Exception as e:
            print(f"Error loading default scale: {e}")
            import traceback
            traceback.print_exc()

    def on_scale_change(self, *args):
        """Handle scale selection change."""
        try:
            root = self.root_var.get()
            scale_type_display = self.scale_var.get()

            # Find the internal scale type
            scale_type = None
            for key, value in self.scale_names.items():
                if value == scale_type_display:
                    scale_type = key
                    break

            if scale_type:
                # Use ScaleBuilder methods dynamically
                scale_method = getattr(ScaleBuilderCore, scale_type, None)
                if scale_method:
                    self.current_scale = scale_method(root)
                    self.update_display()
                else:
                    print(f"Scale method {scale_type} not found")
        except Exception as e:
            print(f"Error changing scale: {e}")
            import traceback
            traceback.print_exc()

    def update_display(self):
        """Update the display with current scale information."""
        if not self.current_scale:
            return

        # Update notes
        notes_str = " ".join(self.current_scale.note_names)
        self.notes_display.configure(text=notes_str)

        # Update intervals
        intervals_str = " ".join([f"W/H({i})" for i in self.current_scale.intervals])
        self.intervals_display.configure(text=intervals_str)

        # Update degrees
        degrees_text = ""
        for i, note in enumerate(self.current_scale.notes, 1):
            scale_degree = self.get_scale_degree_name(i)
            degrees_text += f"{i}. {note.name} ({scale_degree})\n"
        self.degrees_display.delete("1.0", "end")
        self.degrees_display.insert("1.0", degrees_text.strip())

        # Update compatible chords
        chords_text = self.get_compatible_chords()
        self.chords_display.delete("1.0", "end")
        self.chords_display.insert("1.0", chords_text)

    def get_scale_degree_name(self, degree: int) -> str:
        """Get the name of a scale degree."""
        degree_names = {
            1: "Tonic (I)",
            2: "Supertonic (II)",
            3: "Mediant (III)",
            4: "Subdominant (IV)",
            5: "Dominant (V)",
            6: "Submediant (VI)",
            7: "Leading Tone/Subtonic (VII)"
        }
        return degree_names.get(degree, f"Degree {degree}")

    def get_compatible_chords(self) -> str:
        """Get compatible chords for the current scale."""
        if not self.current_scale:
            return "No scale selected"

        chords = []
        for degree in range(1, len(self.current_scale) + 1):
            try:
                chord = self.current_scale.get_triad(degree)
                chords.append(f"{degree}. {chord.name}")
            except:
                continue

        return "\n".join(chords)

    def set_fretboard_callback(self, callback):
        """Set callback for fretboard visualization."""
        self.fretboard_callback = callback

    def show_on_fretboard(self):
        """Show current scale on fretboard."""
        if self.current_scale and self.fretboard_callback:
            try:
                from models.note import Note
                scale_notes = [Note(name) for name in self.current_scale.note_names]
                root_note = Note(self.root_var.get())
                self.fretboard_callback(scale_notes, root_note)
            except Exception as e:
                print(f"Error sending scale to fretboard: {e}")

    def play_scale(self):
        """Play the current scale as an arpeggio."""
        if self.current_scale:
            try:
                # Convert scale notes to string format for audio player
                note_strings = [str(note) for note in self.current_scale.notes]
                play_arpeggio(note_strings, note_duration=0.3)

                # Visual feedback
                original_text = self.play_button.cget("text")
                self.play_button.configure(text="Playing...", fg_color="#FF6B35")
                self.after(2500, lambda: self.play_button.configure(text=original_text, fg_color="#2E8B57"))

                print(f"Playing scale: {self.current_scale.name}")

            except Exception as e:
                print(f"Error playing scale: {e}")
                # Show error feedback with message
                original_text = self.play_button.cget("text")
                self.play_button.configure(text="No Audio", fg_color="#DC143C")
                self.after(3000, lambda: self.play_button.configure(text=original_text, fg_color="#2E8B57"))
        else:
            print("No scale to play")

    def transpose_scale(self, semitones: int):
        """Transpose the current scale by the given number of semitones."""
        if self.current_scale:
            try:
                # Transpose the scale
                transposed_scale = self.current_scale.transpose(semitones)

                # Update current scale
                self.current_scale = transposed_scale

                # Update the root note selector to match the new root
                new_root = str(transposed_scale.root.note_name)
                if new_root in self.root_notes:
                    self.root_var.set(new_root)

                # Update display
                self.update_display()

                print(f"Transposed scale: {transposed_scale.name}")

            except Exception as e:
                print(f"Error transposing scale: {e}")
        else:
            print("No scale to transpose")

    def show_relative_scale(self):
        """Show the relative major/minor scale."""
        if self.current_scale:
            try:
                scale_type = self.current_scale.scale_type

                # Find relative scale
                if scale_type == 'major':
                    # Relative minor is 3 steps down (minor third)
                    relative_root = self.current_scale.root.transpose(-3)  # 3 semitones down
                    relative_scale = ScaleBuilderCore.minor(str(relative_root), 'natural')
                    relative_name = "Relative Minor"
                elif scale_type == 'minor_natural':
                    # Relative major is 3 steps up (3 semitones)
                    relative_root = self.current_scale.root.transpose(3)
                    relative_scale = ScaleBuilderCore.major(str(relative_root))
                    relative_name = "Relative Major"
                else:
                    print(f"No relative scale defined for {scale_type}")
                    return

                # Update current scale to relative
                self.current_scale = relative_scale

                # Update UI to match the new scale
                new_root = str(relative_scale.root.note_name)
                if new_root in self.root_notes:
                    self.root_var.set(new_root)

                # Find and set the scale type display name
                for internal_type, display_name in self.scale_names.items():
                    if internal_type == relative_scale.scale_type:
                        self.scale_var.set(display_name)
                        break

                # Update display
                self.update_display()

                print(f"Switched to {relative_name}: {relative_scale.name}")

            except Exception as e:
                print(f"Error showing relative scale: {e}")
        else:
            print("No scale to find relative for")

    def get_export_data(self) -> str:
        """Get data for export."""
        if not self.current_scale:
            return "No scale data to export"

        data = f"Scale: {self.current_scale.name}\n"
        data += f"Notes: {' '.join(self.current_scale.note_names)}\n"
        data += f"Intervals: {' '.join(str(i) for i in self.current_scale.intervals)}\n\n"
        data += "Compatible Chords:\n"
        data += self.get_compatible_chords()
        data += "\n"

        return data

    def save_preset(self, name: str, description: str = "") -> bool:
        """
        Save current scale configuration as a preset.

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
                category='scales',
                name=name,
                data=state,
                description=description
            )
        except Exception as e:
            print(f"Error saving scale preset: {e}")
            return False

    def load_preset(self, name: str) -> bool:
        """
        Load a scale preset.

        Args:
            name: Preset name

        Returns:
            True if successful, False otherwise
        """
        try:
            preset_manager = get_preset_manager()

            preset = preset_manager.load_preset('scales', name)
            if not preset:
                return False

            # Apply preset state
            return self.apply_state(preset['data'])

        except Exception as e:
            print(f"Error loading scale preset: {e}")
            return False

    def get_current_state(self) -> dict:
        """
        Get current scale explorer state for saving.

        Returns:
            Dictionary containing current state
        """
        state = {
            'root_note': getattr(self.root_var, 'get', lambda: 'C')(),
            'scale_type': getattr(self.scale_var, 'get', lambda: 'major')(),
            'selected_scale': self.current_scale.name if self.current_scale else None,
            'octave': getattr(self.octave_var, 'get', lambda: 4)()
        }
        return state

    def apply_state(self, state: dict) -> bool:
        """
        Apply a saved state to the scale explorer.

        Args:
            state: State dictionary

        Returns:
            True if successful, False otherwise
        """
        try:
            # Set root note
            if 'root_note' in state and hasattr(self, 'root_var'):
                self.root_var.set(state['root_note'])

            # Set scale type
            if 'scale_type' in state and hasattr(self, 'scale_var'):
                self.scale_var.set(state['scale_type'])

            # Set octave
            if 'octave' in state and hasattr(self, 'octave_var'):
                self.octave_var.set(state['octave'])

            # Update scale display
            self.update_scale()

            return True

        except Exception as e:
            print(f"Error applying scale state: {e}")
            return False
