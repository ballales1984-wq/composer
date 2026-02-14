#!/usr/bin/env python3
"""
Standalone Music Theory Engine Demo.

This is a self-contained demo that includes all necessary code
to avoid import issues. Perfect for testing the GUI.
"""

import sys
import os
import customtkinter as ctk
from tkinter import Canvas
from typing import List, Optional, Union, Dict

# Import FretboardCanvas
from models.fretboard import FretboardCanvas

# Full FretboardViewer for standalone demo
class FretboardViewer(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        # Title
        title = ctk.CTkLabel(self, text="Guitar Fretboard Viewer", font=ctk.CTkFont(size=16, weight="bold"))
        title.pack(pady=10)

        # Info text
        self.info_text = ctk.CTkTextbox(self, height=400, wrap="word")
        self.info_text.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        self.info_text.insert("1.0", "Fretboard Visualization:\n\n")
        self.info_text.insert("end", "• Click 'Show on Fretboard' in other tabs to see positions\n")
        self.info_text.insert("end", "• Scale notes appear in GREEN\n")
        self.info_text.insert("end", "• Chord notes appear in BLUE\n")
        self.info_text.insert("end", "• Arpeggio sequences appear in YELLOW\n")
        self.info_text.insert("end", "• Root notes appear in RED\n\n")
        self.info_text.insert("end", "Try it now! Go to Scale Explorer and click 'Show on Fretboard'")

        # Make text read-only
        self.info_text.configure(state="disabled")

        # Current highlights tracking
        self.current_highlights = []

        # Add test buttons
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(fill="x", padx=20, pady=(10, 20))

        self.test_btn = ctk.CTkButton(button_frame, text="Test C Major Scale", command=self.test_highlight)
        self.test_btn.pack(side="left", padx=(0, 10))

        # Force redraw button for debugging
        redraw_btn = ctk.CTkButton(button_frame, text="Redraw", command=self._force_redraw)
        redraw_btn.pack(side="left")

        clear_btn = ctk.CTkButton(button_frame, text="Clear", command=self.clear_highlights)
        clear_btn.pack(side="left")

        # Status label
        self.status_label = ctk.CTkLabel(button_frame, text="Ready", text_color="green")
        self.status_label.pack(side="right")

        # Canvas for fretboard visualization
        self.canvas_frame = ctk.CTkFrame(self)
        self.canvas_frame.pack(fill="both", expand=True, padx=20, pady=(10, 10))

        self.canvas = Canvas(
            self.canvas_frame,
            width=900,
            height=500,
            bg="#1a1a1a",
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True, padx=10, pady=10)

        # Initialize the fretboard canvas after canvas is created
        self.fretboard_canvas = FretboardCanvas(self.canvas, num_frets=15)

        # Ensure canvas is properly sized
        self.canvas_frame.bind("<Configure>", lambda e: self._resize_canvas())

    def highlight_scale(self, notes, root=None):
        """Show scale information and highlight on fretboard."""
        # Update text information
        self.info_text.configure(state="normal")
        self.info_text.delete("1.0", "end")

        self.info_text.insert("1.0", f"🎼 SCALE VIEW\n\n")
        self.info_text.insert("end", f"Notes in scale: {len(notes)}\n")

        if root:
            self.info_text.insert("end", f"Root note: {root.name} (RED)\n")

        self.info_text.insert("end", f"\nPositions highlighted on fretboard:\n")
        self.info_text.insert("end", f"🟢 Green: All scale notes\n🔴 Red: Root note\n\n")

        # Find actual guitar positions and highlight on canvas
        if self.fretboard_canvas:
            # Clear previous highlights
            self.fretboard_canvas.clear_highlights()

            # Find positions for scale notes
            scale_positions = self.fretboard_canvas.find_positions_for_notes(notes, max_fret=15)

            # Highlight scale notes in bright green
            if scale_positions:
                self.fretboard_canvas.highlight_notes(scale_positions, "#00ff00")  # Bright Green

            # Highlight root note in bright red if specified
            if root:
                root_positions = self.fretboard_canvas.find_positions_for_notes([root], max_fret=15)
                if root_positions:
                    self.fretboard_canvas.highlight_notes(root_positions, "#ff0000")  # Bright Red

        # Show guitar positions in text
        self.info_text.insert("end", "🎸 Sample Positions:\n")
        if self.fretboard_canvas:
            for i, note in enumerate(notes[:6]):  # Show first 6 positions
                positions = self.fretboard_canvas.find_positions_for_notes([note], max_fret=12)
                if positions:
                    string, fret = positions[0]  # Take first position
                    self.info_text.insert("end", f"• {note.name}: String {string+1}, Fret {fret}\n")
                else:
                    self.info_text.insert("end", f"• {note.name}: No positions found\n")

        self.info_text.configure(state="disabled")
        self.current_highlights.append(f"Scale: {len(notes)} notes")

        # Force canvas redraw
        if self.fretboard_canvas:
            self.fretboard_canvas.canvas.after(50, lambda: self.fretboard_canvas.redraw_highlights())
            self.fretboard_canvas.canvas.after(100, lambda: self.fretboard_canvas.canvas.update())

        # Update status
        if hasattr(self, 'status_label'):
            self.status_label.configure(text=f"Showing {len(notes)}-note scale", text_color="green")

    def _force_redraw(self):
        """Force complete redraw of fretboard."""
        if hasattr(self, 'fretboard_canvas') and self.fretboard_canvas:
            print("DEBUG: Manual force redraw triggered")
            self.fretboard_canvas.draw_fretboard()
            self.fretboard_canvas.redraw_highlights()
            self.fretboard_canvas.canvas.update()
            print("DEBUG: Manual redraw completed")

    def _resize_canvas(self):
        """Handle canvas resizing."""
        if hasattr(self, 'fretboard_canvas') and self.fretboard_canvas:
            # Force redraw when canvas is resized
            self.fretboard_canvas.canvas.after(10, lambda: self.fretboard_canvas.draw_fretboard())

    def highlight_chord(self, notes, root=None):
        """Show chord information."""
        self.info_text.configure(state="normal")
        self.info_text.delete("1.0", "end")

        self.info_text.insert("1.0", f"🎹 CHORD VIEW\n\n")
        self.info_text.insert("end", f"Notes in chord: {len(notes)}\n")

        if root:
            self.info_text.insert("end", f"Root note: {root} (RED)\n")

        self.info_text.insert("end", f"\nAll positions highlighted in BLUE\n")
        self.info_text.insert("end", f"Note list: {' '.join([n.name for n in notes])}\n\n")

        # Simulate chord voicings
        self.info_text.insert("end", "🎸 Chord Voicings:\n")
        for i, note in enumerate(notes):
            self.info_text.insert("end", f"• {note.name}: Position {i+1}\n")

        self.info_text.configure(state="disabled")
        self.current_highlights.append(f"Chord: {len(notes)} notes")

    def highlight_arpeggio(self, notes):
        """Show arpeggio information."""
        self.info_text.configure(state="normal")
        self.info_text.delete("1.0", "end")

        self.info_text.insert("end", f"🎶 ARPEGGIO VIEW\n\n")
        self.info_text.insert("end", f"Notes in sequence: {len(notes)}\n")
        self.info_text.insert("end", f"\nSequence highlighted in YELLOW\n")
        self.info_text.insert("end", f"Playing order: {' → '.join([n.name for n in notes])}\n\n")

        # Simulate arpeggio positions
        self.info_text.insert("end", "🎸 Arpeggio Positions:\n")
        for i, note in enumerate(notes):
            self.info_text.insert("end", f"{i+1}. {note.name}: String {(i % 6) + 1}, Fret {i % 12}\n")

        self.info_text.configure(state="disabled")
        self.current_highlights.append(f"Arpeggio: {len(notes)} notes")

    def test_highlight(self):
        """Test highlight functionality."""
        print("DEBUG: Test highlight button clicked")
        # Create a simple C major scale for testing
        c_note = Note('C')
        d_note = Note('D')
        e_note = Note('E')
        f_note = Note('F')
        g_note = Note('G')
        a_note = Note('A')
        b_note = Note('B')

        test_notes = [c_note, d_note, e_note, f_note, g_note, a_note, b_note]
        self.highlight_scale(test_notes, c_note)
        print("DEBUG: Test highlight completed")

    def clear_highlights(self):
        """Clear current highlights."""
        self.current_highlights.clear()
        self.info_text.configure(state="normal")
        self.info_text.delete("1.0", "end")
        self.info_text.insert("1.0", "🎸 GUITAR FRETBOARD VIEWER\n\n")
        self.info_text.insert("end", "This tab shows guitar positions for scales, chords, and arpeggios.\n\n")
        self.info_text.insert("end", "HOW TO USE:\n")
        self.info_text.insert("end", "1. Go to other tabs (Scale Explorer, Chord Builder, etc.)\n")
        self.info_text.insert("end", "2. Create a scale, chord, or arpeggio\n")
        self.info_text.insert("end", "3. Click 'Show on Fretboard' button\n")
        self.info_text.insert("end", "4. Come back to this tab to see the positions!\n\n")
        self.info_text.insert("end", "COLOR CODING:\n")
        self.info_text.insert("end", "• 🔴 RED: Root notes\n")
        self.info_text.insert("end", "• 🔵 BLUE: Chord tones\n")
        self.info_text.insert("end", "• 🟢 GREEN: Scale notes\n")
        self.info_text.insert("end", "• 🟡 YELLOW: Arpeggio sequence\n\n")
        self.info_text.insert("end", "Ready to explore! 🎵")
        self.info_text.configure(state="disabled")

# =============================================================================
# MUSIC THEORY CLASSES - COPIED HERE FOR STANDALONE USE
# =============================================================================

# Constants (simplified)
NATURAL_NOTES = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
NOTE_TO_SEMITONE = {
    'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3,
    'E': 4, 'F': 5, 'F#': 6, 'Gb': 6, 'G': 7, 'G#': 8,
    'Ab': 8, 'A': 9, 'A#': 10, 'Bb': 10, 'B': 11
}
SEMITONE_TO_NOTES = {
    0: ['C'], 1: ['C#', 'Db'], 2: ['D'], 3: ['D#', 'Eb'],
    4: ['E'], 5: ['F'], 6: ['F#', 'Gb'], 7: ['G'], 8: ['G#', 'Ab'],
    9: ['A'], 10: ['A#', 'Bb'], 11: ['B']
}
SCALE_INTERVALS = {
    'major': [0, 2, 4, 5, 7, 9, 11],
    'minor_natural': [0, 2, 3, 5, 7, 8, 10],
    'dorian': [0, 2, 3, 5, 7, 9, 10],
    'mixolydian': [0, 2, 4, 5, 7, 9, 10],
    'pentatonic_minor': [0, 3, 5, 7, 10]
}
CHORD_INTERVALS = {
    'maj': [0, 4, 7], 'min': [0, 3, 7], 'dom7': [0, 4, 7, 10],
    'dim7': [0, 3, 6, 9], 'min7': [0, 3, 7, 10]
}

class Note:
    """Simple Note class for standalone demo."""
    def __init__(self, note: Union[str, int]):
        if isinstance(note, str):
            self._name = note.upper()
            self._semitone = NOTE_TO_SEMITONE.get(self._name, 0)
        else:
            self._semitone = note % 12
            self._name = SEMITONE_TO_NOTES[self._semitone][0]

    @property
    def name(self):
        return self._name

    @property
    def semitone(self):
        return self._semitone

    def transpose(self, semitones: int):
        new_semitone = (self._semitone + semitones) % 12
        return Note(new_semitone)

    def __str__(self):
        return self._name

    def __eq__(self, other):
        if isinstance(other, Note):
            return self._semitone == other._semitone
        return False

class Scale:
    """Simple Scale class for standalone demo."""
    def __init__(self, root: Union[str, Note], scale_type: str):
        self._root = root if isinstance(root, Note) else Note(root)
        self._type = scale_type
        self._intervals = SCALE_INTERVALS.get(scale_type, [0, 2, 4, 5, 7, 9, 11])
        self._notes = self._generate_notes()

    def _generate_notes(self):
        notes = []
        for interval in self._intervals:
            semitone = (self._root.semitone + interval) % 12
            note = Note(semitone)
            notes.append(note)
        return notes

    @property
    def notes(self):
        return self._notes.copy()

    @property
    def name(self):
        return f"{self._root} {self._type.title()}"

class Chord:
    """Simple Chord class for standalone demo."""
    def __init__(self, root: Union[str, Note], quality: str):
        self._root = root if isinstance(root, Note) else Note(root)
        self._quality = quality
        self._intervals = CHORD_INTERVALS.get(quality, [0, 4, 7])
        self._notes = self._generate_notes()

    def _generate_notes(self):
        notes = []
        for interval in self._intervals:
            semitone = (self._root.semitone + interval) % 12
            note = Note(semitone)
            notes.append(note)
        return notes

    @property
    def notes(self):
        return self._notes.copy()

    @property
    def name(self):
        return f"{self._root}{self._quality}"

class Arpeggio:
    """Simple Arpeggio class for standalone demo."""
    def __init__(self, source: Union[Chord, Scale], direction: str = 'up'):
        self._source = source
        self._direction = direction
        self._notes = self._generate_arpeggio()

    def _generate_arpeggio(self):
        base_notes = self._source.notes.copy()
        if self._direction == 'down':
            return list(reversed(base_notes))
        return base_notes

    @property
    def notes(self):
        return self._notes.copy()

class Progression:
    """Simple Progression class for standalone demo."""
    def __init__(self, chords: List[Union[str, Chord]]):
        self._chords = []
        for chord in chords:
            if isinstance(chord, str):
                # Parse simple chord (e.g., "C", "Dm", "G7")
                if chord.endswith('m'):
                    root = chord[:-1]
                    quality = 'min'
                elif chord.endswith('7'):
                    root = chord[:-1]
                    quality = 'dom7'
                elif chord.endswith('dim7') or chord.endswith('°7'):
                    root = chord[:-4] if chord.endswith('dim7') else chord[:-2]
                    quality = 'dim7'
                else:
                    root = chord
                    quality = 'maj'
                self._chords.append(Chord(root, quality))
            else:
                self._chords.append(chord)

    @property
    def chords(self):
        return self._chords.copy()

    def __str__(self):
        return " → ".join([chord.name for chord in self._chords])

# =============================================================================
# GUI APPLICATION
# =============================================================================

class StandaloneMusicDemo(ctk.CTk):
    """Standalone music theory demo GUI."""

    def __init__(self):
        super().__init__()

        self.title("Music Theory Engine - Standalone Demo")
        self.geometry("1000x700")

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.setup_ui()

    def setup_ui(self):
        """Setup the user interface."""
        # Main title
        title = ctk.CTkLabel(
            self,
            text="🎵 Music Theory Engine - Standalone Demo",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title.pack(pady=20)

        # Tab view
        self.tabview = ctk.CTkTabview(self, width=900, height=550)
        self.tabview.pack(pady=(0, 20))

        # Create tabs
        self.tabview.add("Scale Explorer")
        self.tabview.add("Chord Builder")
        self.tabview.add("Arpeggio Viewer")
        self.tabview.add("Progression Analyzer")
        self.tabview.add("Fretboard Viewer")

        # Setup tab contents
        self.setup_scale_tab()
        self.setup_chord_tab()
        self.setup_arpeggio_tab()
        self.setup_progression_tab()
        self.setup_fretboard_tab()

        # Initialize tab components for callbacks
        self.scale_explorer = self
        self.chord_builder = self
        self.arpeggio_viewer = self
        self.progression_analyzer = self

        # Connect components for fretboard visualization
        self._connect_components()

        # Bottom buttons
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(fill="x", padx=20, pady=(0, 20))

        # Temporarily disabled - causing conflicts
        # run_demo_btn = ctk.CTkButton(
        #     button_frame,
        #     text="Run Full Demo",
        #     command=self.run_demo
        # )
        # run_demo_btn.pack(side="left", padx=(0, 10))

        clear_btn = ctk.CTkButton(
            button_frame,
            text="Clear",
            command=self.clear_results
        )
        clear_btn.pack(side="left", padx=(0, 10))

        quit_btn = ctk.CTkButton(
            button_frame,
            text="Quit",
            command=self.quit
        )
        quit_btn.pack(side="right")

        # FretboardCanvas will be initialized in FretboardViewer.setup_ui

    def setup_scale_tab(self):
        """Setup the scale explorer tab."""
        tab = self.tabview.tab("Scale Explorer")

        # Controls
        control_frame = ctk.CTkFrame(tab)
        control_frame.pack(fill="x", padx=20, pady=(20, 10))

        ctk.CTkLabel(control_frame, text="Root Note:").pack(side="left", padx=(0, 5))
        self.scale_root_var = ctk.StringVar(value="C")
        root_menu = ctk.CTkOptionMenu(
            control_frame,
            values=['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B'],
            variable=self.scale_root_var
        )
        root_menu.pack(side="left", padx=(0, 20))

        ctk.CTkLabel(control_frame, text="Scale Type:").pack(side="left", padx=(0, 5))
        self.scale_type_var = ctk.StringVar(value="major")
        type_menu = ctk.CTkOptionMenu(
            control_frame,
            values=["Major", "Natural Minor", "Dorian", "Mixolydian", "Minor Pentatonic"],
            variable=self.scale_type_var
        )
        type_menu.pack(side="left", padx=(0, 20))

        create_btn = ctk.CTkButton(
            control_frame,
            text="Create Scale",
            command=self.create_scale
        )
        create_btn.pack(side="left", padx=(0, 10))

        fretboard_btn = ctk.CTkButton(
            control_frame,
            text="Show on Fretboard",
            command=self.show_scale_on_fretboard
        )
        fretboard_btn.pack(side="left")

        # Debug button
        debug_btn = ctk.CTkButton(
            control_frame,
            text="TEST",
            command=lambda: print("BUTTON WORKS")
        )
        debug_btn.pack(side="left", padx=(10, 0))

        # Results
        self.scale_result = ctk.CTkTextbox(tab, height=300, wrap="word")
        self.scale_result.pack(fill="both", padx=20, pady=(10, 20))

    def setup_chord_tab(self):
        """Setup the chord builder tab."""
        tab = self.tabview.tab("Chord Builder")

        # Controls
        control_frame = ctk.CTkFrame(tab)
        control_frame.pack(fill="x", padx=20, pady=(20, 10))

        ctk.CTkLabel(control_frame, text="Root Note:").pack(side="left", padx=(0, 5))
        self.chord_root_var = ctk.StringVar(value="C")
        root_menu = ctk.CTkOptionMenu(
            control_frame,
            values=['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B'],
            variable=self.chord_root_var
        )
        root_menu.pack(side="left", padx=(0, 20))

        ctk.CTkLabel(control_frame, text="Chord Type:").pack(side="left", padx=(0, 5))
        self.chord_type_var = ctk.StringVar(value="maj")
        type_menu = ctk.CTkOptionMenu(
            control_frame,
            values=["Major", "Minor", "Dominant 7th", "Minor 7th", "Diminished 7th"],
            variable=self.chord_type_var
        )
        type_menu.pack(side="left", padx=(0, 20))

        create_btn = ctk.CTkButton(
            control_frame,
            text="Create Chord",
            command=self.create_chord
        )
        create_btn.pack(side="left", padx=(0, 10))

        fretboard_btn = ctk.CTkButton(
            control_frame,
            text="Show on Fretboard",
            command=self.show_chord_on_fretboard
        )
        fretboard_btn.pack(side="left")

        # Results
        self.chord_result = ctk.CTkTextbox(tab, height=300, wrap="word")
        self.chord_result.pack(fill="both", padx=20, pady=(10, 20))

    def setup_arpeggio_tab(self):
        """Setup the arpeggio viewer tab."""
        tab = self.tabview.tab("Arpeggio Viewer")

        # Controls
        control_frame = ctk.CTkFrame(tab)
        control_frame.pack(fill="x", padx=20, pady=(20, 10))

        ctk.CTkLabel(control_frame, text="Source:").pack(side="left", padx=(0, 5))
        self.arp_source_var = ctk.StringVar(value="chord")
        source_menu = ctk.CTkOptionMenu(
            control_frame,
            values=["Chord", "Scale"],
            variable=self.arp_source_var,
            command=self.on_source_change
        )
        source_menu.pack(side="left", padx=(0, 20))

        ctk.CTkLabel(control_frame, text="Root:").pack(side="left", padx=(0, 5))
        self.arp_root_var = ctk.StringVar(value="C")
        self.arp_root_menu = ctk.CTkOptionMenu(
            control_frame,
            values=['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B'],
            variable=self.arp_root_var
        )
        self.arp_root_menu.pack(side="left", padx=(0, 20))

        ctk.CTkLabel(control_frame, text="Type:").pack(side="left", padx=(0, 5))
        self.arp_type_var = ctk.StringVar(value="maj")
        self.arp_type_menu = ctk.CTkOptionMenu(
            control_frame,
            values=["Major", "Minor", "Dominant 7th"],
            variable=self.arp_type_var
        )
        self.arp_type_menu.pack(side="left", padx=(0, 20))

        ctk.CTkLabel(control_frame, text="Direction:").pack(side="left", padx=(0, 5))
        self.arp_direction_var = ctk.StringVar(value="up")
        direction_menu = ctk.CTkOptionMenu(
            control_frame,
            values=["Up", "Down"],
            variable=self.arp_direction_var
        )
        direction_menu.pack(side="left", padx=(0, 20))

        create_btn = ctk.CTkButton(
            control_frame,
            text="Create Arpeggio",
            command=self.create_arpeggio
        )
        create_btn.pack(side="left", padx=(0, 10))

        fretboard_btn = ctk.CTkButton(
            control_frame,
            text="Show on Fretboard",
            command=self.show_arpeggio_on_fretboard
        )
        fretboard_btn.pack(side="left")

        # Results
        self.arpeggio_result = ctk.CTkTextbox(tab, height=300, wrap="word")
        self.arpeggio_result.pack(fill="both", padx=20, pady=(10, 20))

    def setup_progression_tab(self):
        """Setup the progression analyzer tab."""
        tab = self.tabview.tab("Progression Analyzer")

        # Input
        input_frame = ctk.CTkFrame(tab)
        input_frame.pack(fill="x", padx=20, pady=(20, 10))

        ctk.CTkLabel(input_frame, text="Enter progression (e.g., C F G C):").pack(anchor="w", padx=10, pady=(10, 5))

        self.progression_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="C F G C",
            font=ctk.CTkFont(size=14)
        )
        self.progression_entry.pack(fill="x", padx=10, pady=(0, 10))

        analyze_btn = ctk.CTkButton(
            input_frame,
            text="Analyze Progression",
            command=self.analyze_progression
        )
        analyze_btn.pack(pady=(0, 10))

        # Results
        self.progression_result = ctk.CTkTextbox(tab, height=350, wrap="word")
        self.progression_result.pack(fill="both", padx=20, pady=(10, 20))

    def setup_fretboard_tab(self):
        """Setup the fretboard viewer tab."""
        tab = self.tabview.tab("Fretboard Viewer")
        print("DEBUG: Setting up fretboard tab")
        
        # Initialize the fretboard viewer in this tab
        self.fretboard_viewer = FretboardViewer(tab)
        print("DEBUG: FretboardViewer created")
        
        # CRITICAL: Pack the fretboard viewer to make it visible!
        self.fretboard_viewer.pack(fill="both", expand=True)
        print("DEBUG: FretboardViewer packed and should be visible")

    def _on_tab_change(self):
        """Handle tab changes."""
        current_tab = self.tabview.get()
        if current_tab == "Fretboard Viewer":
            print("DEBUG: Entered Fretboard Viewer tab")
            # Force complete redraw of fretboard when entering the tab
            if hasattr(self, 'fretboard_viewer') and hasattr(self.fretboard_viewer, 'fretboard_canvas'):
                print("DEBUG: Fretboard canvas exists, forcing redraw")
                canvas = self.fretboard_viewer.fretboard_canvas.canvas
                print(f"DEBUG: Canvas size: {canvas.winfo_width()}x{canvas.winfo_height()}")
                print(f"DEBUG: Canvas visible: {canvas.winfo_viewable()}")

                # Force canvas to be visible and redraw everything
                self.fretboard_viewer.fretboard_canvas.draw_fretboard()
                self.fretboard_viewer.fretboard_canvas.redraw_highlights()
                canvas.update()

                # Additional forced redraws with delays
                canvas.after(10, lambda: canvas.update())
                canvas.after(50, lambda: self.fretboard_viewer.fretboard_canvas.redraw_highlights())
                canvas.after(100, lambda: canvas.update())

                print("DEBUG: Redraw operations scheduled")

    def _connect_components(self):
        """Connect components for fretboard visualization."""
        # Connect scale explorer to fretboard
        if hasattr(self, 'scale_explorer') and hasattr(self.scale_explorer, 'set_fretboard_callback'):
            self.scale_explorer.set_fretboard_callback(self._on_scale_selected)

        # Connect chord builder to fretboard
        if hasattr(self, 'chord_builder') and hasattr(self.chord_builder, 'set_fretboard_callback'):
            self.chord_builder.set_fretboard_callback(self._on_chord_selected)

        # Connect arpeggio viewer to fretboard
        if hasattr(self, 'arpeggio_viewer') and hasattr(self.arpeggio_viewer, 'set_fretboard_callback'):
            self.arpeggio_viewer.set_fretboard_callback(self._on_arpeggio_selected)

    def _on_scale_selected(self, scale_notes, root_note=None):
        """Handle scale selection for fretboard display."""
        try:
            print(f"DEBUG: Scale selected - notes: {len(scale_notes)}, root: {root_note}")
            self.fretboard_viewer.highlight_scale(scale_notes, root_note)
            self.tabview.set("Fretboard Viewer")
            print("DEBUG: Switched to fretboard tab")
        except Exception as e:
            print(f"Error displaying scale on fretboard: {e}")
            import traceback
            traceback.print_exc()

    def _on_chord_selected(self, chord_notes, root_note=None):
        """Handle chord selection for fretboard display."""
        try:
            self.fretboard_viewer.highlight_chord(chord_notes, root_note)
            self.tabview.set("Fretboard Viewer")
            if hasattr(self.fretboard_viewer, 'status_label'):
                chord_type_display = self.chord_type_var.get()
                self.fretboard_viewer.status_label.configure(text=f"Showing {root} {chord_type_display}", text_color="blue")
        except Exception as e:
            print(f"Error displaying chord on fretboard: {e}")

    def _on_arpeggio_selected(self, arpeggio_notes):
        """Handle arpeggio selection for fretboard display."""
        try:
            self.fretboard_viewer.highlight_arpeggio(arpeggio_notes)
            self.tabview.set("Fretboard Viewer")
            if hasattr(self.fretboard_viewer, 'status_label'):
                arp_type = self.arp_type_var.get()
                self.fretboard_viewer.status_label.configure(text=f"Showing {self.arp_root_var.get()} {arp_type} arpeggio", text_color="yellow")
        except Exception as e:
            print(f"Error displaying arpeggio on fretboard: {e}")

    def create_scale(self):
        """Create and display a scale."""
        root = self.scale_root_var.get()
        scale_type_display = self.scale_type_var.get()

        # Convert display names to internal types
        type_map = {
            "Major": "major",
            "Natural Minor": "minor_natural",
            "Dorian": "dorian",
            "Mixolydian": "mixolydian",
            "Minor Pentatonic": "pentatonic_minor"
        }
        scale_type = type_map.get(scale_type_display, "major")

        try:
            scale = Scale(root, scale_type)
            notes_str = " ".join([note.name for note in scale.notes])

            result = f"Scale: {scale.name}\n"
            result += f"Notes: {notes_str}\n"
            result += f"Number of notes: {len(scale.notes)}\n\n"
            result += "This scale contains all the notes you'll need to play\n"
            result += "music in the key of the selected root note!"

            self.scale_result.delete("1.0", "end")
            self.scale_result.insert("1.0", result)

        except Exception as e:
            self.scale_result.delete("1.0", "end")
            self.scale_result.insert("1.0", f"Error creating scale: {e}")

    def create_chord(self):
        """Create and display a chord."""
        root = self.chord_root_var.get()
        chord_type_display = self.chord_type_var.get()

        # Convert display names to internal types
        type_map = {
            "Major": "maj",
            "Minor": "min",
            "Dominant 7th": "dom7",
            "Minor 7th": "min7",
            "Diminished 7th": "dim7"
        }
        chord_type = type_map.get(chord_type_display, "maj")

        try:
            chord = Chord(root, chord_type)
            notes_str = " ".join([note.name for note in chord.notes])

            result = f"Chord: {chord.name}\n"
            result += f"Notes: {notes_str}\n"
            result += f"Number of notes: {len(chord.notes)}\n\n"

            if chord_type == "maj":
                result += "This is a basic major triad - the foundation of harmony!"
            elif chord_type == "min":
                result += "This is a minor triad - often used for sad or emotional sounds."
            elif "7" in chord_type:
                result += "This is a seventh chord - adds tension and color to progressions!"

            self.chord_result.delete("1.0", "end")
            self.chord_result.insert("1.0", result)

        except Exception as e:
            self.chord_result.delete("1.0", "end")
            self.chord_result.insert("1.0", f"Error creating chord: {e}")

    def on_source_change(self, *args):
        """Handle arpeggio source change."""
        source = self.arp_source_var.get().lower()
        if source == "chord":
            self.arp_type_menu.configure(values=["Major", "Minor", "Dominant 7th"])
            self.arp_type_var.set("Major")
        else:
            self.arp_type_menu.configure(values=["Major", "Natural Minor", "Dorian"])
            self.arp_type_var.set("Major")

    def create_arpeggio(self):
        """Create and display an arpeggio."""
        root = self.arp_root_var.get()
        source_type = self.arp_source_var.get().lower()
        type_display = self.arp_type_var.get()
        direction_display = self.arp_direction_var.get().lower()

        # Convert display names
        type_map = {
            "Major": "maj", "Minor": "min", "Dominant 7th": "dom7",
            "Natural Minor": "minor_natural", "Dorian": "dorian"
        }
        source_quality = type_map.get(type_display, "maj")

        try:
            if source_type == "chord":
                source = Chord(root, source_quality)
            else:
                source = Scale(root, source_quality)

            arpeggio = Arpeggio(source, direction_display)
            notes_str = " ".join([note.name for note in arpeggio.notes])

            result = f"Arpeggio from {source.name}\n"
            result += f"Direction: {direction_display.title()}\n"
            result += f"Notes: {notes_str}\n"
            result += f"Total notes: {len(arpeggio.notes)}\n\n"

            result += "Arpeggios are essential for:\n"
            result += "- Melodic improvisation\n"
            result += "- Chord soloing techniques\n"
            result += "- Connecting chord changes smoothly\n"
            result += "- Developing finger independence"

            self.arpeggio_result.delete("1.0", "end")
            self.arpeggio_result.insert("1.0", result)

        except Exception as e:
            self.arpeggio_result.delete("1.0", "end")
            self.arpeggio_result.insert("1.0", f"Error creating arpeggio: {e}")

    def analyze_progression(self):
        """Analyze a chord progression."""
        progression_text = self.progression_entry.get().strip()

        if not progression_text:
            self.progression_result.delete("1.0", "end")
            self.progression_result.insert("1.0", "Please enter a chord progression first!")
            return

        try:
            # Split by spaces and create progression
            chord_names = progression_text.split()
            progression = Progression(chord_names)

            result = f"Progression Analysis\n"
            result += "=" * 30 + "\n\n"
            result += f"Progression: {progression}\n"
            result += f"Number of chords: {len(progression.chords)}\n\n"

            result += "Chord Details:\n"
            for i, chord in enumerate(progression.chords, 1):
                notes_str = " ".join([note.name for note in chord.notes])
                result += f"{i}. {chord.name}: {notes_str}\n"

            result += "\nThis progression uses chords that work well together!\n"
            result += "Try playing these chords in sequence on your instrument."

            self.progression_result.delete("1.0", "end")
            self.progression_result.insert("1.0", result)

        except Exception as e:
            self.progression_result.delete("1.0", "end")
            self.progression_result.insert("1.0", f"Error analyzing progression: {e}")

    def show_scale_on_fretboard(self):
        """Show current scale on fretboard."""
        try:
            root = self.scale_root_var.get()
            scale_type_display = self.scale_type_var.get()

            # Convert display names to internal types
            type_map = {
                "Major": "major",
                "Natural Minor": "minor_natural",
                "Dorian": "dorian",
                "Mixolydian": "mixolydian",
                "Minor Pentatonic": "pentatonic_minor"
            }
            scale_type = type_map.get(scale_type_display, "major")

            scale = Scale(root, scale_type)
            # Notes from scale already have octave 4, use them directly
            scale_notes = list(scale.notes)  # Already have correct octaves (C4, D4, etc.)
            root_note = Note(root, octave=4)

            self.fretboard_viewer.highlight_scale(scale_notes, root_note)
            self.tabview.set("Fretboard Viewer")

            # Force canvas redraw after tab change
            self.fretboard_viewer.fretboard_canvas.canvas.after(100, lambda: self.fretboard_viewer.fretboard_canvas.canvas.update())

            if hasattr(self.fretboard_viewer, 'status_label'):
                self.fretboard_viewer.status_label.configure(text=f"Showing {root} {scale_type_display}", text_color="green")
        except Exception as e:
            print(f"Error showing scale on fretboard: {e}")

    def show_chord_on_fretboard(self):
        """Show current chord on fretboard."""
        try:
            root = self.chord_root_var.get()
            chord_type_display = self.chord_type_var.get()

            # Convert display names to internal types
            type_map = {
                "Major": "maj",
                "Minor": "min",
                "Dominant 7th": "dom7",
                "Minor 7th": "min7",
                "Diminished 7th": "dim7"
            }
            chord_type = type_map.get(chord_type_display, "maj")

            chord = Chord(root, chord_type)
            # Chord notes already have correct octaves, use them directly
            chord_notes = list(chord.notes)
            root_note = Note(root, octave=4)

            self.fretboard_viewer.highlight_chord(chord_notes, root_note)
            self.tabview.set("Fretboard Viewer")
            if hasattr(self.fretboard_viewer, 'status_label'):
                chord_type_display = self.chord_type_var.get()
                self.fretboard_viewer.status_label.configure(text=f"Showing {root} {chord_type_display}", text_color="blue")
        except Exception as e:
            print(f"Error showing chord on fretboard: {e}")

    def show_arpeggio_on_fretboard(self):
        """Show current arpeggio on fretboard."""
        try:
            root = self.arp_root_var.get()
            source_type = self.arp_source_var.get().lower()
            type_display = self.arp_type_var.get()
            direction_display = self.arp_direction_var.get().lower()

            # Convert display names
            type_map = {
                "Major": "maj", "Minor": "min", "Dominant 7th": "dom7",
                "Natural Minor": "minor_natural", "Dorian": "dorian"
            }
            source_quality = type_map.get(type_display, "maj")

            if source_type == "chord":
                source = Chord(root, source_quality)
            else:
                source = Scale(root, source_quality)

            arpeggio = Arpeggio(source, direction_display)
            arpeggio_notes = [note for note in arpeggio.notes]

            self.fretboard_viewer.highlight_arpeggio(arpeggio_notes)
            self.tabview.set("Fretboard Viewer")
            if hasattr(self.fretboard_viewer, 'status_label'):
                arp_type = self.arp_type_var.get()
                self.fretboard_viewer.status_label.configure(text=f"Showing {self.arp_root_var.get()} {arp_type} arpeggio", text_color="yellow")
        except Exception as e:
            print(f"Error showing arpeggio on fretboard: {e}")

    def clear_results(self):
        """Clear all results and reset the interface."""
        # Clear scale tab
        self.scale_result.delete("1.0", "end")

        # Clear chord tab
        self.chord_result.delete("1.0", "end")

        # Clear arpeggio tab
        self.arpeggio_result.delete("1.0", "end")

        # Clear progression tab
        self.progression_result.delete("1.0", "end")

        # Clear fretboard highlights
        self.fretboard_viewer.clear_highlights()

    def run_demo(self):
        """Run a full demo of all features."""
        # Set default values and create examples
        self.scale_root_var.set("C")
        self.scale_type_var.set("Major")
        self.create_scale()
        # Also show on fretboard
        self.show_scale_on_fretboard()

        self.chord_root_var.set("C")
        self.chord_type_var.set("Major")
        self.create_chord()
        # Also show on fretboard
        self.show_chord_on_fretboard()

        self.arp_source_var.set("Chord")
        self.arp_root_var.set("C")
        self.arp_type_var.set("Major")
        self.arp_direction_var.set("Up")
        self.on_source_change()
        self.create_arpeggio()
        # Also show on fretboard
        self.show_arpeggio_on_fretboard()

        self.progression_entry.delete(0, "end")
        self.progression_entry.insert(0, "C G Am F")
        self.analyze_progression()

        # Switch to fretboard tab to show the visualizations
        self.tabview.set("Fretboard Viewer")

def main():
    """Launch the standalone demo."""
    print("Launching Music Theory Engine Standalone Demo...")

    try:
        app = StandaloneMusicDemo()
        print("App created successfully, starting mainloop...")
        app.mainloop()
    except Exception as e:
        print(f"Error launching GUI: {e}")
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
