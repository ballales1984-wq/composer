"""
Fretboard Viewer GUI component.

This module provides a visual representation of the guitar fretboard
showing notes, scales, chords, and arpeggios.
"""

import customtkinter as ctk
from tkinter import Canvas
from typing import List, Dict, Optional, Tuple, Set
import sys
import os

# Import modules
from ..models.fretboard import GuitarFretboard, FretboardPosition, FretboardCanvas
from ..models.note import Note


class FretboardViewer(ctk.CTkFrame):
    """
    Guitar fretboard visualization using a simple grid/table approach.

    Features:
    - Grid-based fretboard representation (6 strings x 8 positions)
    - Note highlighting for scales, chords, arpeggios
    - Simple and reliable visualization
    - Legend and controls
    - Easy to understand and debug
    """

    def __init__(self, parent, width: int = 900, height: int = 500):
        super().__init__(parent)

        # Pack this frame to fill the parent tab
        self.pack(fill="both", expand=True)

        self.fretboard_width = width
        self.fretboard_height = height

        # Fretboard data
        self.fretboard = GuitarFretboard(num_frets=15)
        self.grid_labels = []  # 6x8 grid of labels
        self.highlighted_positions = set()
        self.current_mode = "notes"

        # String names (from high to low: E B G D A E)
        self.string_names = ["E", "B", "G", "D", "A", "E"]

        self.setup_ui()

    def setup_ui(self):
        """Setup the user interface."""
        # Title
        self.title_label = ctk.CTkLabel(
            self,
            text="🎸 Guitar Fretboard Viewer",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.title_label.pack(pady=(20, 10))

        # Status and controls
        controls_frame = ctk.CTkFrame(self)
        controls_frame.pack(fill="x", padx=20, pady=(0, 10))

        # Status display
        self.status_label = ctk.CTkLabel(
            controls_frame,
            text="Ready - Create scales/chords in other tabs and click 'Show on Fretboard'",
            font=ctk.CTkFont(size=12)
        )
        self.status_label.pack(side="left", padx=(10, 20))

        # Test button
        self.test_btn = ctk.CTkButton(
            controls_frame,
            text="Test C Major",
            command=self.test_c_major
        )
        self.test_btn.pack(side="right", padx=(10, 10))

        # Clear button
        self.clear_btn = ctk.CTkButton(
            controls_frame,
            text="Clear Highlights",
            command=self.clear_highlights
        )
        self.clear_btn.pack(side="right")

        # Test label removed - grid should be visible now

        # Fretboard grid (6 strings x 16 positions)
        self.grid_frame = ctk.CTkFrame(self)
        self.grid_frame.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        # Create the fretboard grid
        self.create_fretboard_grid()

        # Legend
        self.legend_frame = ctk.CTkFrame(self)
        self.legend_frame.pack(fill="x", padx=20, pady=(0, 20))

        self.legend_label = ctk.CTkLabel(
            self.legend_frame,
            text="🎨 Legend:",
            font=ctk.CTkFont(weight="bold")
        )
        self.legend_label.pack(anchor="w", padx=10, pady=(10, 5))

        # Color indicators
        legend_text = "🔴 Red: Root notes  • 🔵 Blue: Chord tones  • 🟢 Green: Scale notes  • 🟡 Yellow: Arpeggio sequence"
        self.legend_text = ctk.CTkLabel(
            self.legend_frame,
            text=legend_text,
            font=ctk.CTkFont(size=12)
        )
        self.legend_text.pack(anchor="w", padx=10, pady=(0, 10))

    def create_fretboard_grid(self):
        """Create a 6x13 grid representing the guitar fretboard (open + 12 frets)."""
        # Clear existing grid
        for widget in self.grid_frame.winfo_children():
            widget.destroy()

        self.grid_labels = []

        # Create 6 strings x 13 positions (open + 12 frets)
        for string in range(6):  # All 6 strings
            row_labels = []

            # String name label (left side)
            string_label = ctk.CTkLabel(
                self.grid_frame,
                text=self.string_names[string],
                font=ctk.CTkFont(size=14, weight="bold"),
                width=45,
                height=35,
                fg_color="#444444",
                text_color="#ffffff"
            )
            string_label.grid(row=string, column=0, padx=(10, 10), pady=2)

            # Create 13 fret positions (open + 12 frets)
            for fret in range(13):  # 0-12 frets
                # Get the note at this position
                pos = self.fretboard.get_position(string + 1, fret)
                note_name = pos.note.note_name if pos.note else "?"
                octave = pos.note.octave if pos.note else ""

                # Display format: fret number and note
                if fret == 0:
                    display_text = f"Open\n{note_name}"
                else:
                    display_text = f"{fret}\n{note_name}"

                # Create label for this position
                label = ctk.CTkLabel(
                    self.grid_frame,
                    text=display_text,
                    font=ctk.CTkFont(size=9),
                    width=55,
                    height=35,
                    fg_color="#2b2b2b",  # Default dark background
                    text_color="#ffffff"
                )

                # Position in grid (offset by 1 for string label column)
                label.grid(row=string, column=fret + 1, padx=1, pady=2)
                row_labels.append(label)

            self.grid_labels.append(row_labels)

        # Add fret number labels at the bottom
        for fret in range(13):
            if fret == 0:
                fret_text = "Open"
            else:
                fret_text = str(fret)

            fret_label = ctk.CTkLabel(
                self.grid_frame,
                text=fret_text,
                font=ctk.CTkFont(size=9, weight="bold"),
                width=55,
                height=25,
                fg_color="#666666",
                text_color="#ffffff"
            )
            fret_label.grid(row=6, column=fret + 1, padx=1, pady=(5, 5))

        print(f"Fretboard grid created: {len(self.grid_labels)} strings x {len(self.grid_labels[0]) if self.grid_labels else 0} frets")

    def test_c_major(self):
        """Test function to show C Major scale on the grid."""
        # Create C Major scale notes in 4th octave (standard)
        c_notes = [
            Note("C", octave=4), Note("D", octave=4), Note("E", octave=4),
            Note("F", octave=4), Note("G", octave=4), Note("A", octave=4), Note("B", octave=4)
        ]

        print(f"Testing C Major scale: {[str(n) for n in c_notes]}")
        self.highlight_scale(c_notes, Note("C", octave=4))

        if hasattr(self, 'status_label'):
            self.status_label.configure(text="Testing C Major Scale", text_color="green")

    # Fretboard drawing is now handled by FretboardCanvas

    def highlight_positions(self, positions: List[Tuple[int, int]],
                          color: str = "#ff6b6b",
                          mode: str = "scale"):
        """
        Highlight specific positions on the fretboard.

        Args:
            positions: List of (string, fret) tuples (0-based)
            color: Color for highlighting
            mode: Type of highlighting (scale, chord, arpeggio, root)
        """
        print(f"DEBUG: highlight_positions called with {len(positions)} positions, color: {color}")
        # This method is kept for compatibility but we use the specific methods below
        self.current_mode = mode
        if hasattr(self, 'status_label'):
            self.status_label.configure(text=f"Showing {mode.title()}", text_color="green")

    def clear_highlights(self):
        """Clear all highlighted positions on the grid."""
        # Reset all grid labels to default colors
        for string in range(len(self.grid_labels)):
            for fret in range(len(self.grid_labels[string])):
                self.grid_labels[string][fret].configure(
                    fg_color="#2b2b2b",  # Default dark background
                    text_color="#ffffff"
                )

        self.current_mode = "notes"
        if hasattr(self, 'status_label'):
            self.status_label.configure(text="Highlights cleared", text_color="gray")

    def highlight_scale(self, scale_notes: List[Note], root_note: Optional[Note] = None):
        """Highlight all positions of a scale on the fretboard grid."""
        # Clear previous highlights
        self.clear_highlights()

        print(f"Highlighting scale with {len(scale_notes)} notes")

        # Find and highlight positions for scale notes in green
        for string in range(6):  # All 6 strings
            for fret in range(13):  # 0-12 frets
                pos = self.fretboard.get_position(string + 1, fret)
                note_at_pos = pos.note

                if note_at_pos:
                    # Check if this position's note matches any scale note (compare by note name, not octave)
                    for scale_note in scale_notes:
                        if note_at_pos.note_name == scale_note.note_name:
                            if 0 <= string < len(self.grid_labels) and 0 <= fret < len(self.grid_labels[string]):
                                self.grid_labels[string][fret].configure(
                                    fg_color="#00aa00",  # Green for scale notes
                                    text_color="#ffffff"
                                )
                                break

        # Highlight root note positions in red (overrides green)
        if root_note:
            print(f"Looking for root note {root_note}")
            for string in range(6):  # All 6 strings
                for fret in range(13):  # 0-12 frets
                    pos = self.fretboard.get_position(string + 1, fret)
                    if pos.note and pos.note.note_name == root_note.note_name:
                        if 0 <= string < len(self.grid_labels) and 0 <= fret < len(self.grid_labels[string]):
                            self.grid_labels[string][fret].configure(
                                fg_color="#aa0000",  # Red for root notes
                                text_color="#ffffff"
                            )

        # Update status
        if hasattr(self, 'status_label'):
            self.status_label.configure(text=f"Showing {len(scale_notes)}-note scale", text_color="green")

        print("Scale highlighting completed")

    def highlight_chord(self, chord_notes: List[Note], root_note: Optional[Note] = None):
        """Highlight all positions of a chord on the fretboard grid."""
        # Clear previous highlights
        self.clear_highlights()

        # Find and highlight positions for chord notes in blue
        for note in chord_notes:
            for string in range(6):
                for fret in range(13):
                    pos = self.fretboard.get_position(string + 1, fret)
                    if pos.note and pos.note.note_name == note.note_name:
                        if 0 <= string < len(self.grid_labels) and 0 <= fret < len(self.grid_labels[string]):
                            self.grid_labels[string][fret].configure(
                                fg_color="#0077aa",  # Blue for chord notes
                                text_color="#ffffff"
                            )

        # Highlight root note in red (overrides blue)
        if root_note:
            for string in range(6):
                for fret in range(13):
                    pos = self.fretboard.get_position(string + 1, fret)
                    if pos.note and pos.note.note_name == root_note.note_name:
                        if 0 <= string < len(self.grid_labels) and 0 <= fret < len(self.grid_labels[string]):
                            self.grid_labels[string][fret].configure(
                                fg_color="#aa0000",  # Red for root notes
                                text_color="#ffffff"
                            )

        # Update status
        if hasattr(self, 'status_label'):
            self.status_label.configure(text=f"Showing {len(chord_notes)}-note chord", text_color="blue")

    def highlight_arpeggio(self, arpeggio_notes: List[Note]):
        """Highlight an arpeggio sequence on the fretboard grid."""
        # Clear previous highlights
        self.clear_highlights()

        # Find and highlight positions for arpeggio notes in yellow
        for note in arpeggio_notes:
            for string in range(6):
                for fret in range(13):
                    pos = self.fretboard.get_position(string + 1, fret)
                    if pos.note and pos.note.note_name == note.note_name:
                        if 0 <= string < len(self.grid_labels) and 0 <= fret < len(self.grid_labels[string]):
                            self.grid_labels[string][fret].configure(
                                fg_color="#aaaa00",  # Yellow for arpeggio notes
                                text_color="#ffffff"
                            )

        # Update status
        if hasattr(self, 'status_label'):
            self.status_label.configure(text=f"Showing {len(arpeggio_notes)}-note arpeggio", text_color="yellow")

    # Old methods removed - now using FretboardCanvas

    def get_highlighted_notes(self) -> List[Note]:
        """Get list of currently highlighted notes."""
        notes = []
        # Get notes from highlighted grid positions
        for string in range(len(self.grid_labels)):
            for fret in range(len(self.grid_labels[string])):
                if self.grid_labels[string][fret].cget("fg_color") != "#2b2b2b":  # If highlighted
                    pos = self.fretboard.get_position(string + 1, fret)
                    if pos.note not in notes:
                        notes.append(pos.note)
        return notes

    def export_fretboard_image(self, filename: str = "fretboard.png"):
        """Export the fretboard as an image."""
        try:
            # This would require PIL/Pillow to save the canvas as image
            # For now, just show a message
            print(f"Fretboard export to {filename} would be implemented here")
        except Exception as e:
            print(f"Export failed: {e}")

    def on_canvas_click(self, event):
        """Handle canvas click events."""
        # Convert click coordinates to string/fret position
        # This could be used for interactive note selection
        pass
