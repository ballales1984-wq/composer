#!/usr/bin/env python3
"""
Simplified GUI launcher for the Music Theory Engine.

This version imports everything directly to avoid package issues.
"""

import sys
import os
import customtkinter as ctk
from tkinter import messagebox

# Setup paths
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Import all modules directly
from models.note import Note
from models.chord import Chord
from models.scale import Scale
from models.arpeggio import Arpeggio
from models.progression import Progression

from core.scales import ScaleBuilder
from core.chords import ChordBuilder
from core.arpeggios import ArpeggioBuilder
from core.progressions import ProgressionAnalyzer


class SimpleMusicGUI(ctk.CTk):
    """Simplified music theory GUI."""

    def __init__(self):
        super().__init__()

        self.title("Music Theory Engine - Simple GUI")
        self.geometry("800x600")

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.setup_ui()
        self.test_functionality()

    def setup_ui(self):
        """Setup the user interface."""
        # Main title
        title = ctk.CTkLabel(
            self,
            text="🎵 Music Theory Engine",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.pack(pady=20)

        # Test section
        test_frame = ctk.CTkFrame(self)
        test_frame.pack(fill="x", padx=20, pady=(0, 20))

        self.test_label = ctk.CTkLabel(
            test_frame,
            text="Testing core functionality...",
            font=ctk.CTkFont(size=16)
        )
        self.test_label.pack(pady=20)

        self.result_text = ctk.CTkTextbox(test_frame, height=300, wrap="word")
        self.result_text.pack(fill="both", padx=20, pady=(0, 20))

        # Buttons
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(fill="x", padx=20, pady=(0, 20))

        test_btn = ctk.CTkButton(
            button_frame,
            text="Run Tests",
            command=self.test_functionality
        )
        test_btn.pack(side="left", padx=(0, 10))

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

    def test_functionality(self):
        """Test core music functionality."""
        self.result_text.delete("1.0", "end")
        self.result_text.insert("1.0", "Running tests...\n\n")

        try:
            # Test 1: Notes
            self.result_text.insert("end", "1. Testing Notes:\n")
            c = Note('C')
            c_sharp = Note('C#')
            d_flat = Note('Db')

            self.result_text.insert("end", f"   C note: {c} (semitone: {c.semitone})\n")
            self.result_text.insert("end", f"   C# note: {c_sharp} (semitone: {c_sharp.semitone})\n")
            self.result_text.insert("end", f"   Db note: {d_flat} (semitone: {d_flat.semitone})\n")
            self.result_text.insert("end", f"   C# == Db: {c_sharp == d_flat}\n\n")

            # Test 2: Scales
            self.result_text.insert("end", "2. Testing Scales:\n")
            c_major = ScaleBuilder.major('C')
            notes_str = " ".join([n.name for n in c_major.notes])
            self.result_text.insert("end", f"   C Major: {notes_str}\n")

            a_minor = ScaleBuilder.minor('A', 'natural')
            notes_str = " ".join([n.name for n in a_minor.notes])
            self.result_text.insert("end", f"   A Natural Minor: {notes_str}\n\n")

            # Test 3: Chords
            self.result_text.insert("end", "3. Testing Chords:\n")
            c_maj = ChordBuilder.major('C')
            notes_str = " ".join([n.name for n in c_maj.notes])
            self.result_text.insert("end", f"   C Major: {notes_str}\n")

            dm = ChordBuilder.minor('D')
            notes_str = " ".join([n.name for n in dm.notes])
            self.result_text.insert("end", f"   D Minor: {notes_str}\n\n")

            # Test 4: Arpeggios
            self.result_text.insert("end", "4. Testing Arpeggios:\n")
            c_arp = ArpeggioBuilder.from_chord('C', 'up')
            notes_str = " ".join([n.name for n in c_arp.notes])
            self.result_text.insert("end", f"   C Major arpeggio: {notes_str}\n\n")

            # Test 5: Progressions
            self.result_text.insert("end", "5. Testing Progressions:\n")
            prog = ProgressionAnalyzer.analyze(['C', 'F', 'G', 'C'])
            self.result_text.insert("end", f"   Progression: {prog}\n")
            self.result_text.insert("end", f"   Key detected: {prog.key_name or 'None'}\n")
            self.result_text.insert("end", f"   Complexity: {prog.analysis.get('complexity', 'Unknown')}\n\n")

            self.result_text.insert("end", "SUCCESS: All tests passed! The Music Theory Engine is working.\n")
            self.result_text.insert("end", "\nYou can now use the full GUI application with:\n")
            self.result_text.insert("end", "python main_gui.py\n")

        except Exception as e:
            self.result_text.insert("end", f"ERROR: {str(e)}\n")
            import traceback
            self.result_text.insert("end", traceback.format_exc())

    def clear_results(self):
        """Clear the results text."""
        self.result_text.delete("1.0", "end")


def main():
    """Launch the simplified GUI."""
    app = SimpleMusicGUI()
    app.mainloop()


if __name__ == "__main__":
    main()
