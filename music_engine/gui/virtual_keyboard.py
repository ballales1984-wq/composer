"""
Virtual Keyboard GUI component.

This module provides an interactive piano keyboard interface
for selecting musical notes visually.
"""

import customtkinter as ctk
from typing import List, Optional, Callable
import sys
import os

# Import modules
from ..models.note import Note
from ..utils.audio import play_note


class VirtualKeyboard(ctk.CTkFrame):
    """
    Interactive virtual piano keyboard interface.

    Features:
    - Visual piano keyboard (88 keys: A0-C8)
    - Click to select notes
    - Octave range selection
    - Audio feedback
    - Note information display
    - Integration with other components
    """

    # Standard piano key layout
    WHITE_KEYS = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
    BLACK_KEYS = ['C#', 'D#', None, 'F#', 'G#', 'A#', None]

    def __init__(self, parent):
        super().__init__(parent)

        # Pack this frame to fill the parent tab
        self.pack(fill="both", expand=True)

        # Keyboard data
        self.current_note: Optional[Note] = None
        self.selected_octave = 4
        self.note_callback: Optional[Callable] = None  # Callback for note selection

        # Available octaves
        self.octaves = list(range(0, 9))  # A0 to C8

        self._create_interface()
        self._setup_key_bindings()

    def _create_interface(self):
        """Create the keyboard interface."""
        # Main container
        main_container = ctk.CTkFrame(self)
        main_container.pack(fill="both", expand=True, padx=20, pady=20)

        # Title
        title_label = ctk.CTkLabel(
            main_container,
            text="🎹 Virtual Piano Keyboard",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(pady=(0, 10))

        # Octave selector
        self._create_octave_selector(main_container)

        # Keyboard area
        self._create_keyboard_area(main_container)

        # Note info display
        self._create_note_info(main_container)

        # Instructions
        self._create_instructions(main_container)

    def _create_octave_selector(self, parent):
        """Create octave selection controls."""
        octave_frame = ctk.CTkFrame(parent)
        octave_frame.pack(fill="x", pady=(0, 15))

        octave_label = ctk.CTkLabel(
            octave_frame,
            text="Octave:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        octave_label.pack(side="left", padx=(20, 10))

        # Octave buttons
        self.octave_buttons = {}
        for octave in self.octaves:
            btn = ctk.CTkButton(
                octave_frame,
                text=str(octave),
                width=40,
                height=30,
                command=lambda o=octave: self._select_octave(o)
            )
            btn.pack(side="left", padx=2)
            self.octave_buttons[octave] = btn

        # Highlight current octave
        self._highlight_octave_button(self.selected_octave)

    def _create_keyboard_area(self, parent):
        """Create the visual keyboard."""
        keyboard_frame = ctk.CTkFrame(parent, height=200)
        keyboard_frame.pack(fill="x", pady=(0, 15))
        keyboard_frame.pack_propagate(False)

        # Create canvas for keyboard
        self.keyboard_canvas = ctk.CTkCanvas(
            keyboard_frame,
            height=180,
            bg="#2B2B2B",
            highlightthickness=0
        )
        self.keyboard_canvas.pack(fill="both", expand=True, padx=10, pady=10)

        # Draw keyboard
        self._draw_keyboard()

    def _create_note_info(self, parent):
        """Create note information display."""
        info_frame = ctk.CTkFrame(parent)
        info_frame.pack(fill="x", pady=(0, 15))

        # Current note display
        note_frame = ctk.CTkFrame(info_frame)
        note_frame.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(
            note_frame,
            text="Selected Note:",
            font=ctk.CTkFont(size=12, weight="bold")
        ).pack(side="left", padx=(0, 10))

        self.note_display = ctk.CTkLabel(
            note_frame,
            text="None",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#4CAF50"
        )
        self.note_display.pack(side="left")

        # Note details
        details_frame = ctk.CTkFrame(info_frame)
        details_frame.pack(fill="x", padx=20, pady=(0, 10))

        self.frequency_label = ctk.CTkLabel(
            details_frame,
            text="Frequency: - Hz",
            font=ctk.CTkFont(size=11)
        )
        self.frequency_label.pack(side="left", padx=(0, 20))

        self.semitone_label = ctk.CTkLabel(
            details_frame,
            text="Semitone: -",
            font=ctk.CTkFont(size=11)
        )
        self.semitone_label.pack(side="left")

    def _create_instructions(self, parent):
        """Create usage instructions."""
        instructions_frame = ctk.CTkFrame(parent)
        instructions_frame.pack(fill="x", pady=(0, 10))

        instructions_text = """
        🎵 How to use:
        • Click on white/black keys to select notes
        • Use octave buttons to change range
        • Selected notes play automatically
        • Note information updates in real-time
        """

        instructions_label = ctk.CTkLabel(
            instructions_frame,
            text=instructions_text,
            font=ctk.CTkFont(size=10),
            justify="left"
        )
        instructions_label.pack(padx=20, pady=10)

    def _draw_keyboard(self):
        """Draw the piano keyboard on canvas."""
        canvas_width = self.keyboard_canvas.winfo_width()
        if canvas_width <= 1:  # Canvas not yet sized
            canvas_width = 800

        # Clear canvas
        self.keyboard_canvas.delete("all")

        # Calculate key dimensions
        white_key_width = canvas_width // 14  # 7 white keys * 2 octaves
        white_key_height = 140
        black_key_width = white_key_width // 2
        black_key_height = 90

        # Draw white keys
        white_key_positions = {}
        for i, note in enumerate(['C', 'D', 'E', 'F', 'G', 'A', 'B'] * 2):
            x1 = i * white_key_width
            y1 = 10
            x2 = (i + 1) * white_key_width
            y2 = y1 + white_key_height

            # Alternate colors for octave visualization
            fill_color = "#FFFFFF" if i < 7 else "#F8F8F8"

            key_id = self.keyboard_canvas.create_rectangle(
                x1, y1, x2, y2,
                fill=fill_color,
                outline="#000000",
                width=2,
                tags=f"white_key_{note}_{i//7}"
            )

            # Store position for click detection
            white_key_positions[f"{note}_{i//7}"] = (x1, y1, x2, y2)

            # Label
            octave = self.selected_octave + (i // 7)
            self.keyboard_canvas.create_text(
                (x1 + x2) // 2, y2 - 20,
                text=f"{note}{octave}",
                font=("Arial", 8, "bold"),
                fill="#000000"
            )

        # Draw black keys
        black_positions = [1, 2, 4, 5, 6]  # Positions relative to white keys
        for i, pos in enumerate(black_positions):
            if pos + 7 < 14:  # Don't draw on second octave edge
                x1 = (pos + 7) * white_key_width - black_key_width // 2
                y1 = 10
                x2 = x1 + black_key_width
                y2 = y1 + black_key_height

                black_note = self.BLACK_KEYS[i]
                if black_note:
                    key_id = self.keyboard_canvas.create_rectangle(
                        x1, y1, x2, y2,
                        fill="#000000",
                        outline="#000000",
                        width=1,
                        tags=f"black_key_{black_note}_1"
                    )

                    # Label
                    octave = self.selected_octave + 1
                    self.keyboard_canvas.create_text(
                        (x1 + x2) // 2, y2 - 15,
                        text=f"{black_note}{octave}",
                        font=("Arial", 6),
                        fill="#FFFFFF"
                    )

        # Store positions for click handling
        self.white_key_positions = white_key_positions

    def _setup_key_bindings(self):
        """Setup keyboard event bindings."""
        self.keyboard_canvas.bind("<Button-1>", self._on_key_click)
        self.keyboard_canvas.bind("<Configure>", lambda e: self._draw_keyboard())

    def _on_key_click(self, event):
        """Handle mouse click on keyboard."""
        x, y = event.x, event.y

        # Check black keys first (they're on top)
        items = self.keyboard_canvas.find_overlapping(x, y, x, y)
        clicked_key = None

        for item in items:
            tags = self.keyboard_canvas.gettags(item)
            for tag in tags:
                if tag.startswith("black_key_"):
                    parts = tag.split("_")
                    note_name = parts[2]
                    octave = int(parts[3])
                    clicked_key = f"{note_name}{octave}"
                    break
                elif tag.startswith("white_key_"):
                    parts = tag.split("_")
                    note_name = parts[2]
                    octave = self.selected_octave + int(parts[3])
                    clicked_key = f"{note_name}{octave}"
                    break

        if clicked_key:
            self._select_note(clicked_key)

    def _select_octave(self, octave):
        """Select active octave."""
        self.selected_octave = octave
        self._highlight_octave_button(octave)
        self._draw_keyboard()

    def _highlight_octave_button(self, octave):
        """Highlight the selected octave button."""
        for oct_num, button in self.octave_buttons.items():
            if oct_num == octave:
                button.configure(fg_color="#4CAF50", text_color="white")
            else:
                button.configure(fg_color=["#3B8ED0", "#1F6AA5"], text_color="white")

    def _select_note(self, note_name):
        """Select a note and update displays."""
        try:
            self.current_note = Note(note_name)

            # Update displays
            self.note_display.configure(text=note_name)
            self.frequency_label.configure(text=".1f")
            self.semitone_label.configure(text=f"Semitone: {self.current_note.semitone}")

            # Play note
            try:
                play_note(note_name, 0.3)
            except Exception:
                pass  # Audio might not be available

            # Call callback if set
            if self.note_callback:
                self.note_callback(self.current_note)

        except Exception as e:
            print(f"Error selecting note {note_name}: {e}")

    def set_note_callback(self, callback: Callable):
        """Set callback for note selection events."""
        self.note_callback = callback

    def get_current_note(self) -> Optional[Note]:
        """Get currently selected note."""
        return self.current_note