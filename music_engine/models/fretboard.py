"""
Fretboard model for guitar visualization.

This module provides classes and functions for representing
and calculating note positions on a guitar fretboard.
"""

from typing import List, Dict, Optional, Tuple, Set
from .note import Note


class FretboardPosition:
    """
    Represents a position on the guitar fretboard.

    A position is defined by:
    - String number (1-6, where 1 is high E, 6 is low E)
    - Fret number (0 = open string, 1-24 = fretted notes)
    """

    def __init__(self, string: int, fret: int, tuning: Optional[List[Tuple[str, int]]] = None):
        """
        Initialize a fretboard position.

        Args:
            string: String number (1-6, 1=high E, 6=low E)
            fret: Fret number (0=open, 1-24)
            tuning: List of (note, octave) tuples for string tuning

        Raises:
            ValueError: If string or fret is out of range
        """
        if not (1 <= string <= 6):
            raise ValueError(f"String must be between 1 and 6, got {string}")
        if fret < 0 or fret > 24:
            raise ValueError(f"Fret must be between 0 and 24, got {fret}")

        self.string = string
        self.fret = fret
        self.tuning = tuning or GuitarFretboard.STANDARD_TUNING

    @property
    def note(self) -> Note:
        """Get the note at this position with correct octave."""
        # Get the tuning for this string (string numbers are 1-6, array is 0-5)
        # Standard tuning: [('E', 2), ('A', 2), ('D', 3), ('G', 3), ('B', 3), ('E', 4)]
        # String 1 (high E) -> index 5 -> ('E', 4)
        # String 6 (low E) -> index 0 -> ('E', 2)
        note_name, base_octave = self.tuning[6 - self.string]

        # Create the open string note with correct octave
        open_note = Note(note_name, octave=base_octave)

        # Add the fret offset (each fret = 1 semitone)
        # Calculate new octave: every 12 frets, octave increases
        additional_octave = self.fret // 12
        new_octave = base_octave + additional_octave

        # Calculate new semitone within the octave (chromatic index 0-11)
        additional_semitones = self.fret % 12
        new_semitone = (open_note.chroma + additional_semitones) % 12

        # Create note with correct octave using chroma (not semitone/midi)
        return Note.from_semitone(new_semitone, new_octave)

    @property
    def midi(self) -> int:
        """Get the MIDI note number for this position."""
        return self.note.midi

    def __str__(self) -> str:
        return f"String {self.string}, Fret {self.fret}"

    def __repr__(self) -> str:
        return f"FretboardPosition(string={self.string}, fret={self.fret})"

    def __eq__(self, other) -> bool:
        if isinstance(other, FretboardPosition):
            return self.string == other.string and self.fret == other.fret
        return False

    def __hash__(self) -> int:
        return hash((self.string, self.fret))


class FretboardCanvas:
    """
    Canvas-based guitar fretboard visualization.

    Handles the graphical drawing of strings, frets, and notes.
    """

    def __init__(self, canvas, num_frets=15, string_names=None):
        """
        Initialize the fretboard canvas.

        Args:
            canvas: Tkinter Canvas widget
            num_frets: Number of frets to display
            string_names: Names for strings (optional)
        """
        self.canvas = canvas
        self.num_frets = num_frets
        self.string_names = string_names or ["E", "B", "G", "D", "A", "E"]

        # Canvas dimensions
        self.width = self.canvas.winfo_width() or 800
        self.height = self.canvas.winfo_height() or 400

        # Spacing calculations
        self.string_spacing = self.height // 9  # Space between strings
        self.fret_width = self.width // (self.num_frets + 2)  # Width per fret

        # Positions
        self.string_y_positions = [self.string_spacing * (i + 1) for i in range(6)]
        self.fret_x_positions = [self.fret_width * (i + 1) for i in range(self.num_frets + 1)]

        # Note positions and highlights
        self.note_positions = {}  # (string, fret) -> canvas_item_id
        self.highlighted_notes = set()  # Set of (string, fret) tuples
        self.note_colors = {}  # (string, fret) -> color

        # Draw the fretboard
        self.draw_fretboard()

    def draw_fretboard(self):
        """Draw the complete fretboard."""
        self.canvas.delete("all")

        # Draw strings (horizontal lines)
        for i, y in enumerate(self.string_y_positions):
            string_thickness = 3 if i in [0, 5] else 2  # Thicker for low/high E
            self.canvas.create_line(
                self.fret_x_positions[0], y,
                self.fret_x_positions[-1], y,
                fill="#8B4513",  # Brown color for strings
                width=string_thickness,
                tags="string"
            )

            # String labels (on the left)
            self.canvas.create_text(
                self.fret_x_positions[0] - 25, y,
                text=self.string_names[i],
                anchor="center",
                fill="#ffffff",
                font=("Arial", 12, "bold"),
                tags="string_label"
            )

        # Draw frets (vertical lines)
        for i, x in enumerate(self.fret_x_positions):
            line_width = 4 if i == 0 else 2  # Thicker nut
            self.canvas.create_line(
                x, self.string_y_positions[0] - 10,
                x, self.string_y_positions[-1] + 10,
                fill="#C0C0C0" if i == 0 else "#666666",
                width=line_width,
                tags="fret"
            )

            # Fret numbers (starting from fret 1, skip open)
            if i > 0 and i <= self.num_frets:
                self.canvas.create_text(
                    x + self.fret_width//2,
                    self.string_y_positions[-1] + 25,
                    text=str(i),
                    fill="#ffffff",
                    font=("Arial", 10),
                    tags="fret_number"
                )

        # Draw fret markers (dots)
        marker_frets = [3, 5, 7, 9, 12, 15]
        for fret in marker_frets:
            if fret <= self.num_frets:
                x = self.fret_x_positions[fret] + self.fret_width//2
                y = self.height // 2

                # Double dots at 12th fret
                if fret == 12:
                    self.canvas.create_oval(
                        x-6, y-6, x+6, y+6,
                        fill="#ffffff",
                        outline="#ffffff",
                        tags="marker"
                    )
                    self.canvas.create_oval(
                        x-6, y-20, x+6, y-8,
                        fill="#ffffff",
                        outline="#ffffff",
                        tags="marker"
                    )
                else:
                    self.canvas.create_oval(
                        x-4, y-4, x+4, y+4,
                        fill="#ffffff",
                        outline="#ffffff",
                        tags="marker"
                    )

        # Draw all note positions
        self.draw_note_positions()

    def draw_note_positions(self):
        """Draw all possible note positions on the fretboard."""
        for string in range(6):  # 0-5 (strings)
            for fret in range(self.num_frets + 1):  # 0 to num_frets
                x = self.fret_x_positions[fret] + self.fret_width//2
                y = self.string_y_positions[string]

                # Skip positions that are too close to frets (for open strings)
                if fret == 0:
                    x = self.fret_x_positions[0] - 20

                # Determine note color
                pos_key = (string, fret)
                if pos_key in self.highlighted_notes:
                    dot_color = self.note_colors.get(pos_key, "#ff6b6b")
                    outline_color = "#ffffff"
                    outline_width = 2
                else:
                    dot_color = "#333333"
                    outline_color = "#666666"
                    outline_width = 1

                # Draw note dot
                item_id = self.canvas.create_oval(
                    x-12, y-12, x+12, y+12,  # Much larger dots
                    fill=dot_color,
                    outline=outline_color,
                    width=outline_width,
                    tags=f"note_{string}_{fret}"
                )

                self.note_positions[pos_key] = item_id

    def highlight_notes(self, positions, color="#ff6b6b"):
        """
        Highlight specific note positions.

        Args:
            positions: List of (string, fret) tuples (0-based)
            color: Color for highlighting
        """
        for pos in positions:
            if pos in self.note_positions:
                self.highlighted_notes.add(pos)
                self.note_colors[pos] = color

        self.redraw_highlights()
        # Force canvas update
        self.canvas.update()

    def clear_highlights(self):
        """Clear all highlighted positions."""
        self.highlighted_notes.clear()
        self.note_colors.clear()
        self.redraw_highlights()

    def redraw_highlights(self):
        """Redraw only the note positions with updated highlights."""
        for (string, fret), item_id in self.note_positions.items():
            pos_key = (string, fret)

            if pos_key in self.highlighted_notes:
                color = self.note_colors.get(pos_key, "#ff6b6b")
                self.canvas.itemconfig(item_id, fill=color, outline="#ffffff", width=4)
            else:
                self.canvas.itemconfig(item_id, fill="#666666", outline="#999999", width=2)

    def get_note_at_position(self, string, fret):
        """Get the note name at a specific position."""
        # Convert to 1-based string index for GuitarFretboard compatibility
        fretboard = GuitarFretboard(self.num_frets)
        return fretboard.get_position(string + 1, fret).note.name

    def find_positions_for_notes(self, notes, max_fret=None):
        """
        Find all fretboard positions for given notes.

        Args:
            notes: List of Note objects
            max_fret: Maximum fret to search

        Returns:
            List of (string, fret) tuples (0-based)
        """
        max_fret = max_fret or self.num_frets
        positions = []

        for string in range(6):  # 0-5
            for fret in range(max_fret + 1):  # 0 to max_fret
                fretboard_pos = GuitarFretboard().get_position(string + 1, fret)

                # Check if note matches any of the input notes
                for note in notes:
                    if fretboard_pos.note == note or str(fretboard_pos.note) == str(note):
                        positions.append((string, fret))
                        break
        return positions


class GuitarFretboard:
    """
    Represents a guitar fretboard with note positions including octaves.

    Provides methods for finding positions of notes, scales, chords, etc.
    """

    # Standard guitar tuning with octaves: E2 A2 D3 G3 B3 E4 (low to high)
    STANDARD_TUNING = [('E', 2), ('A', 2), ('D', 3), ('G', 3), ('B', 3), ('E', 4)]

    def __init__(self, num_frets: int = 24, tuning: Optional[List[Tuple[str, int]]] = None):
        """
        Initialize a guitar fretboard.

        Args:
            num_frets: Number of frets (default: 24)
            tuning: List of (note, octave) tuples for open strings (default: standard tuning)
        """
        self.num_frets = num_frets
        self.tuning = tuning or self.STANDARD_TUNING.copy()

        if len(self.tuning) != 6:
            raise ValueError("Guitar must have 6 strings")

        # Create all positions
        self._positions: Dict[Tuple[int, int], FretboardPosition] = {}
        for string in range(1, 7):  # 1-6
            for fret in range(self.num_frets + 1):  # 0 to num_frets
                pos = FretboardPosition(string, fret, self.tuning)
                self._positions[(string, fret)] = pos

    def get_position(self, string: int, fret: int) -> FretboardPosition:
        """Get the position at the specified string and fret."""
        return self._positions[(string, fret)]

    def find_note_positions(self, note: Note, max_fret: Optional[int] = None) -> List[FretboardPosition]:
        """
        Find all positions of a note on the fretboard.

        Args:
            note: The note to find
            max_fret: Maximum fret to search (default: all frets)

        Returns:
            List of positions where the note can be found
        """
        max_fret = max_fret or self.num_frets
        positions = []

        # Use chroma (chromatic index 0-11) for comparison instead of semitone/midi
        target_chroma = note.chroma

        for string in range(1, 7):
            for fret in range(max_fret + 1):
                pos = self.get_position(string, fret)
                # Compare chroma (chromatic index), not semitone/MIDI
                if pos.note.chroma == target_chroma:
                    positions.append(pos)

        return positions

    def get_scale_positions(self, scale_notes: List[Note], max_fret: int = 12) -> Dict[Note, List[FretboardPosition]]:
        """
        Get positions for all notes in a scale.

        Args:
            scale_notes: List of notes in the scale
            max_fret: Maximum fret to include

        Returns:
            Dictionary mapping each scale note to its positions
        """
        scale_positions = {}

        for note in scale_notes:
            positions = self.find_note_positions(note, max_fret)
            scale_positions[note] = positions

        return scale_positions

    def get_chord_positions(self, chord_notes: List[Note], max_fret: int = 12) -> Dict[Note, List[FretboardPosition]]:
        """
        Get positions for all notes in a chord.

        Args:
            chord_notes: List of notes in the chord
            max_fret: Maximum fret to include

        Returns:
            Dictionary mapping each chord note to its positions
        """
        return self.get_scale_positions(chord_notes, max_fret)

    def get_arpeggio_positions(self, arpeggio_notes: List[Note], max_fret: int = 12) -> List[FretboardPosition]:
        """
        Get positions for an arpeggio sequence.

        Args:
            arpeggio_notes: Notes in arpeggio order
            max_fret: Maximum fret to include

        Returns:
            List of positions in arpeggio order (first available position per note)
        """
        positions = []

        for note in arpeggio_notes:
            note_positions = self.find_note_positions(note, max_fret)
            if note_positions:
                # Take the first (lowest) position
                positions.append(note_positions[0])

        return positions

    def get_open_positions(self) -> List[FretboardPosition]:
        """Get all open string positions."""
        return [self.get_position(string, 0) for string in range(1, 7)]

    def get_root_positions(self, root_note: Note, max_fret: int = 12) -> List[FretboardPosition]:
        """
        Get positions for the root note (useful for chord shapes).

        Args:
            root_note: The root note
            max_fret: Maximum fret to include

        Returns:
            List of positions for the root note
        """
        return self.find_note_positions(root_note, max_fret)

    def suggest_chord_positions(self, chord_notes: List[Note], max_span: int = 4) -> List[Dict[Note, FretboardPosition]]:
        """
        Suggest playable chord positions.

        Args:
            chord_notes: Notes in the chord
            max_span: Maximum fret span for the chord

        Returns:
            List of chord voicings (dict mapping notes to positions)
        """
        # This is a simplified implementation
        # A full implementation would consider voice leading, playability, etc.

        voicings = []
        root_positions = self.get_root_positions(chord_notes[0], max_fret=12)

        for root_pos in root_positions[:5]:  # Limit to first 5 root positions
            voicing = {chord_notes[0]: root_pos}

            # Try to find other notes within the span
            min_fret = max(0, root_pos.fret - max_span)
            max_fret = root_pos.fret + max_span

            for note in chord_notes[1:]:
                note_positions = self.find_note_positions(note, max_fret)
                # Find positions within the span and not on the same string
                valid_positions = [
                    pos for pos in note_positions
                    if min_fret <= pos.fret <= max_fret and pos.string != root_pos.string
                ]

                if valid_positions:
                    # Take the first valid position
                    voicing[note] = valid_positions[0]

            if len(voicing) > 1:  # At least root + one other note
                voicings.append(voicing)

        return voicings[:3]  # Return up to 3 voicings


# Utility functions
def get_string_name(string_num: int) -> str:
    """Get the name of a string (e.g., 'Low E', 'A', etc.)."""
    names = {
        6: "Low E",
        5: "A",
        4: "D",
        3: "G",
        2: "B",
        1: "High E"
    }
    return names.get(string_num, f"String {string_num}")


def get_note_name_at_position(string: int, fret: int) -> str:
    """Get the note name at a specific position."""
    pos = FretboardPosition(string, fret)
    return pos.note.name
