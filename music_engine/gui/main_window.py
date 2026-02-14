"""
Main GUI window for the Music Theory Engine.

This module provides the main graphical interface for exploring
music theory concepts interactively.
"""

import customtkinter as ctk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import os

# Import GUI components with proper path setup
import sys
import os

# Ensure the parent directory is in the path
parent_dir = os.path.dirname(os.path.dirname(__file__))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

try:
    from gui.scale_explorer import ScaleExplorer
    from gui.chord_builder import ChordBuilder
    from gui.progression_analyzer import ProgressionAnalyzer
    from gui.arpeggio_viewer import ArpeggioViewer
    from gui.fretboard_viewer import FretboardViewer
    from gui.virtual_keyboard import VirtualKeyboard
    from gui.preset_manager import PresetManagerGUI
except ImportError:
    # Fallback for when running as script
    from .scale_explorer import ScaleExplorer
    from .chord_builder import ChordBuilder
    from .progression_analyzer import ProgressionAnalyzer
    from .arpeggio_viewer import ArpeggioViewer
    from .fretboard_viewer import FretboardViewer
    from .virtual_keyboard import VirtualKeyboard
    from .preset_manager import PresetManagerGUI


class MusicTheoryGUI(ctk.CTk):
    """
    Main GUI window for the Music Theory Engine.

    Features:
    - Tab-based interface for different music theory tools
    - Scale Explorer
    - Chord Builder
    - Progression Analyzer
    - Arpeggio Viewer
    - Export functionality
    """

    def __init__(self):
        super().__init__()

        # Configure window
        self.title("Music Theory Engine - Guitarist's Companion")
        self.geometry("1200x800")
        self.minsize(1000, 700)

        # Set appearance - try light mode for better visibility
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        # Initialize components
        self.setup_ui()
        self.setup_menu()
        self.setup_tabs()

        # Center window and make sure it's visible
        self.center_window()
        self.lift()  # Bring to front
        self.focus_force()  # Give focus
        self.attributes('-topmost', True)  # Always on top initially
        self.after(1000, lambda: self.attributes('-topmost', False))  # Remove always on top after 1 second

        # Show welcome message after initialization
        self.after(1500, self.show_welcome_message)

    def show_welcome_message(self):
        """Show welcome message with audio instructions."""
        # Import here to avoid relative import issues during initialization
        try:
            from ..utils.audio import get_audio_status
        except ImportError:
            # Fallback
            def get_audio_status():
                return "Audio status unknown"
        audio_status = get_audio_status()

        message = "Welcome to Music Theory Engine!\n\n"
        message += "Features:\n"
        message += "• Explore scales and chords\n"
        message += "• Transpose music in real-time\n"
        message += "• Find relative scales\n"
        message += "• Visualize on fretboard\n\n"

        if "not available" in audio_status.lower():
            message += "Audio: Not available\n"
            message += "Install numpy for audio support\n"
        else:
            message += f"Audio: {audio_status}\n"
            message += "Use Play buttons to hear notes!\n"

        message += "\nTry selecting a scale and clicking 'Play Scale'"

        import tkinter.messagebox as messagebox
        messagebox.showinfo("Welcome!", message)

    def setup_ui(self):
        """Setup the main UI components."""
        # Create main frame
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Title
        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="🎸 Music Theory Engine",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.pack(pady=(20, 10))

        # Subtitle
        self.subtitle_label = ctk.CTkLabel(
            self.main_frame,
            text="Professional Music Theory Tools for Guitarists",
            font=ctk.CTkFont(size=14)
        )
        self.subtitle_label.pack(pady=(0, 10))

        # Audio status and test button
        audio_frame = ctk.CTkFrame(self.main_frame)
        audio_frame.pack(fill="x", padx=20, pady=(0, 10))

        # Import here to avoid relative import issues during initialization
        try:
            from ..utils.audio import get_audio_status
        except ImportError:
            # Fallback
            def get_audio_status():
                return "Audio status unknown"
        audio_status = get_audio_status()

        # Show audio status with more details
        if "not available" in audio_status.lower():
            status_text = "Audio: Not Available"
            status_color = "#DC143C"  # Red
        elif "basic" in audio_status.lower():
            status_text = "Audio: Basic (Windows Beeps)"
            status_color = "#FF8C00"  # Orange
        else:
            status_text = "Audio: Full Support"
            status_color = "#4CAF50"  # Green

        self.audio_label = ctk.CTkLabel(
            audio_frame,
            text=status_text,
            font=ctk.CTkFont(size=12),
            text_color=status_color
        )
        self.audio_label.pack(side="left", padx=(10, 10))

        self.test_audio_button = ctk.CTkButton(
            audio_frame,
            text="Test Audio",
            command=self.test_audio,
            width=100,
            fg_color="#4CAF50",
            hover_color="#45a049"
        )
        self.test_audio_button.pack(side="right", padx=(0, 10))

    def setup_menu(self):
        """Setup the menu bar."""
        # Create menu frame
        self.menu_frame = ctk.CTkFrame(self.main_frame, height=40)
        self.menu_frame.pack(fill="x", padx=20, pady=(0, 10))
        self.menu_frame.pack_propagate(False)

        # Menu buttons
        self.file_button = ctk.CTkButton(
            self.menu_frame,
            text="File",
            width=80,
            command=self.show_file_menu
        )
        self.file_button.pack(side="left", padx=(0, 10))

        self.help_button = ctk.CTkButton(
            self.menu_frame,
            text="Help",
            width=80,
            command=self.show_help
        )
        self.help_button.pack(side="right")

    def setup_tabs(self):
        """Setup the tabbed interface."""
        # Create tabview
        self.tabview = ctk.CTkTabview(self.main_frame, width=1100, height=600)
        self.tabview.pack(pady=(0, 20))

        # Create tabs
        self.tabview.add("Scale Explorer")
        self.tabview.add("Chord Builder")
        self.tabview.add("Progression Analyzer")
        self.tabview.add("Arpeggio Viewer")
        self.tabview.add("Fretboard Viewer")
        self.tabview.add("Virtual Keyboard")
        self.tabview.add("Presets")

        # Initialize tab contents
        self.scale_explorer = ScaleExplorer(self.tabview.tab("Scale Explorer"))
        self.chord_builder = ChordBuilder(self.tabview.tab("Chord Builder"))
        self.progression_analyzer = ProgressionAnalyzer(self.tabview.tab("Progression Analyzer"))
        self.arpeggio_viewer = ArpeggioViewer(self.tabview.tab("Arpeggio Viewer"))
        self.fretboard_viewer = FretboardViewer(self.tabview.tab("Fretboard Viewer"))
        self.virtual_keyboard = VirtualKeyboard(self.tabview.tab("Virtual Keyboard"))
        self.preset_manager = PresetManagerGUI(self.tabview.tab("Presets"))

        # Add tooltips to tabs
        self._add_tab_tooltips()

        # Connect components for fretboard visualization
        self._connect_components()

    def test_audio(self):
        """Test audio functionality."""
        try:
            from ..utils.audio import test_audio, get_audio_status
        except ImportError:
            def test_audio(): return "Audio not available"
            def get_audio_status(): return "Audio status unknown"
        try:
            audio_status = get_audio_status()
            result = test_audio()

            import tkinter.messagebox as messagebox

            if "not available" in audio_status.lower():
                messagebox.showwarning("Audio Test",
                    "Audio is not available on this system.\n\n"
                    "To enable audio:\n"
                    "1. Make sure speakers/headphones are connected\n"
                    "2. Check system volume\n"
                    "3. Close other audio applications\n"
                    "4. Install numpy: pip install numpy")
            elif "working" in result.lower():
                messagebox.showinfo("Audio Test",
                    "✅ Audio test completed!\n\n"
                    "If you didn't hear anything:\n"
                    "• Check system volume\n"
                    "• Make sure speakers are working\n"
                    "• Try the Play buttons in Scale/Chord tabs\n"
                    "• Close other audio applications")
            else:
                messagebox.showinfo("Audio Test",
                    f"Audio test result: {result}\n\n"
                    "Try the Play buttons in the Scale and Chord tabs.\n"
                    "If you don't hear anything, check:\n"
                    "• System volume\n"
                    "• Speaker connections\n"
                    "• Other audio applications")

        except Exception as e:
            import tkinter.messagebox as messagebox
            messagebox.showerror("Audio Test", f"Audio test failed: {e}\n\nCheck console for details.")

    def _add_tab_tooltips(self):
        """Add tooltips to tab buttons."""
        tab_tooltips = {
            "Scale Explorer": "Explore musical scales, play them, and see positions on guitar",
            "Chord Builder": "Build chords, explore inversions, and hear them",
            "Progression Analyzer": "Analyze chord progressions and find compatible scales",
            "Arpeggio Viewer": "Create and play arpeggios from scales and chords",
            "Fretboard Viewer": "Visual guitar fretboard showing note positions",
            "Virtual Keyboard": "Interactive piano keyboard for visual note selection",
            "Presets": "Save and load your favorite scale, chord, and progression configurations"
        }

        # Try to add tooltips to tab buttons (if supported by CTkTabview)
        try:
            for tab_name, tooltip in tab_tooltips.items():
                # This might not work with current CTkTabview, but we try
                tab_button = getattr(self.tabview, f"_tab_{tab_name.replace(' ', '_').lower()}", None)
                if tab_button:
                    # Add tooltip if possible
                    pass  # CTkTabview might not support direct tooltips
        except:
            pass  # Tooltips might not be supported

    def _connect_components(self):
        """Connect components to enable fretboard visualization."""
        # Connect scale explorer to fretboard
        if hasattr(self.scale_explorer, 'set_fretboard_callback'):
            self.scale_explorer.set_fretboard_callback(self._on_scale_selected)

        # Connect chord builder to fretboard
        if hasattr(self.chord_builder, 'set_fretboard_callback'):
            self.chord_builder.set_fretboard_callback(self._on_chord_selected)

        # Connect arpeggio viewer to fretboard
        if hasattr(self.arpeggio_viewer, 'set_fretboard_callback'):
            self.arpeggio_viewer.set_fretboard_callback(self._on_arpeggio_selected)

        # Connect virtual keyboard to other components
        if hasattr(self.virtual_keyboard, 'set_note_callback'):
            self.virtual_keyboard.set_note_callback(self._on_note_selected)

    def _on_scale_selected(self, scale_notes: list, root_note=None):
        """Handle scale selection for fretboard display."""
        try:
            self.fretboard_viewer.highlight_scale(scale_notes, root_note)
            # Switch to fretboard tab
            self.tabview.set("Fretboard Viewer")
        except Exception as e:
            print(f"Error displaying scale on fretboard: {e}")

    def _on_chord_selected(self, chord_notes: list, root_note=None):
        """Handle chord selection for fretboard display."""
        try:
            self.fretboard_viewer.highlight_chord(chord_notes, root_note)
            # Switch to fretboard tab
            self.tabview.set("Fretboard Viewer")
        except Exception as e:
            print(f"Error displaying chord on fretboard: {e}")

    def _on_arpeggio_selected(self, arpeggio_notes: list):
        """Handle arpeggio selection for fretboard display."""
        try:
            self.fretboard_viewer.highlight_arpeggio(arpeggio_notes)
            # Switch to fretboard tab
            self.tabview.set("Fretboard Viewer")
        except Exception as e:
            print(f"Error displaying arpeggio on fretboard: {e}")

    def center_window(self):
        """Center the window on screen."""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def show_file_menu(self):
        """Show file menu options."""
        # Create a popup menu
        menu = ctk.CTkToplevel(self)
        menu.title("File Menu")
        menu.geometry("200x150")
        menu.resizable(False, False)

        # Center on parent
        x = self.winfo_x() + self.winfo_width() // 2 - 100
        y = self.winfo_y() + 100
        menu.geometry(f"+{x}+{y}")

        # Menu options
        export_button = ctk.CTkButton(
            menu,
            text="Export Results",
            command=self.export_results
        )
        export_button.pack(pady=10, padx=20, fill="x")

        save_button = ctk.CTkButton(
            menu,
            text="Save Session",
            command=self.save_session
        )
        save_button.pack(pady=(0, 10), padx=20, fill="x")

        close_button = ctk.CTkButton(
            menu,
            text="Close Menu",
            command=menu.destroy
        )
        close_button.pack(pady=(0, 10), padx=20, fill="x")

    def export_results(self):
        """Export current results to file."""
        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                title="Export Music Theory Results"
            )

            if file_path:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write("Music Theory Engine - Export Results\n")
                    f.write("=" * 40 + "\n\n")

                    # Export current tab data
                    current_tab = self.tabview.get()
                    if current_tab == "Scale Explorer":
                        f.write(self.scale_explorer.get_export_data())
                    elif current_tab == "Chord Builder":
                        f.write(self.chord_builder.get_export_data())
                    elif current_tab == "Progression Analyzer":
                        f.write(self.progression_analyzer.get_export_data())
                    elif current_tab == "Arpeggio Viewer":
                        f.write(self.arpeggio_viewer.get_export_data())

                messagebox.showinfo("Export Complete", f"Results exported to {file_path}")

        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export: {str(e)}")

    def save_session(self):
        """Save current session."""
        messagebox.showinfo("Save Session", "Session saving functionality coming soon!")

    def show_help(self):
        """Show help information."""
        help_text = """
        Music Theory Engine Help

        Scale Explorer:
        - Select root note and scale type
        - View notes, intervals, and degrees
        - See compatible chords

        Chord Builder:
        - Choose root note and chord quality
        - View chord notes and intervals
        - Explore inversions

        Progression Analyzer:
        - Enter chord progression
        - Get key detection and analysis
        - Find compatible scales

        Arpeggio Viewer:
        - Create arpeggios from chords or scales
        - Choose direction and octaves
        - View guitar positions

        Use File menu to export results.
        """

        help_window = ctk.CTkToplevel(self)
        help_window.title("Help - Music Theory Engine")
        help_window.geometry("500x400")

        # Center on parent
        x = self.winfo_x() + self.winfo_width() // 2 - 250
        y = self.winfo_y() + self.winfo_height() // 2 - 200
        help_window.geometry(f"+{x}+{y}")

        text_box = ctk.CTkTextbox(help_window, wrap="word")
        text_box.pack(fill="both", expand=True, padx=20, pady=20)
        text_box.insert("1.0", help_text)
        text_box.configure(state="disabled")

        close_button = ctk.CTkButton(
            help_window,
            text="Close",
            command=help_window.destroy
        )
        close_button.pack(pady=(0, 20))

    def _on_note_selected(self, note):
        """Handle note selection from virtual keyboard."""
        # Update fretboard to show the selected note
        if hasattr(self.fretboard_viewer, 'highlight_note'):
            self.fretboard_viewer.highlight_note(note)

        # Could also update other components that might be interested in note selection
        # For now, just update the fretboard


def main():
    """Main entry point for the GUI application."""
    app = MusicTheoryGUI()
    app.mainloop()


if __name__ == "__main__":
    main()
