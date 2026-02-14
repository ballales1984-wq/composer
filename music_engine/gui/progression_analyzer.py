"""
Progression Analyzer GUI component.

This module provides an interactive interface for analyzing
chord progressions and finding compatible scales.
"""

import customtkinter as ctk
from typing import List, Optional
import sys
import os

# Import modules
from ..models.progression import Progression
from ..core.progressions import ProgressionAnalyzer as ProgressionAnalyzerCore
from ..utils.preset_manager import get_preset_manager
from ..analysis.advanced_analytics import HarmonicAnalyzer
from ..analysis.visualization import AnalyticsVisualizer


class ProgressionAnalyzer(ctk.CTkFrame):
    """
    Interactive chord progression analysis interface.

    Features:
    - Chord progression input
    - Key detection
    - Compatible scale suggestions
    - Harmonic analysis
    - Complexity assessment
    """

    def __init__(self, parent):
        super().__init__(parent)

        # Pack this frame to fill the parent tab
        self.pack(fill="both", expand=True)

        # Progression data
        self.current_progression: Optional[Progression] = None

        # Common chord progressions for examples
        self.example_progressions = [
            "C F G C",  # I-IV-V-I
            "Cm Fm Gm Cm",  # i-iv-v-i
            "C Am F G",  # I-vi-IV-V
            "Cmaj7 Dm7 G7 Cmaj7",  # II-V-I with extensions
            "Am F C G",  # vi-IV-I-V
            "C D Em F",  # I-II-III-IV
        ]

        self.setup_ui()

    def setup_ui(self):
        """Setup the user interface."""
        # Control panel
        self.control_frame = ctk.CTkFrame(self)
        self.control_frame.pack(fill="x", padx=20, pady=(20, 10))

        # Title
        self.title_label = ctk.CTkLabel(
            self.control_frame,
            text="Progression Analyzer",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.title_label.pack(pady=(10, 15))

        # Input section
        self.input_frame = ctk.CTkFrame(self.control_frame)
        self.input_frame.pack(fill="x", padx=20, pady=(0, 15))

        self.input_label = ctk.CTkLabel(
            self.input_frame,
            text="Enter chord progression (e.g., C F G C):",
            font=ctk.CTkFont(weight="bold")
        )
        self.input_label.pack(anchor="w", padx=10, pady=(10, 5))

        self.progression_entry = ctk.CTkEntry(
            self.input_frame,
            placeholder_text="C F G C",
            font=ctk.CTkFont(size=14)
        )
        self.progression_entry.pack(fill="x", padx=10, pady=(0, 10))

        # Buttons
        self.button_frame = ctk.CTkFrame(self.input_frame)
        self.button_frame.pack(fill="x", padx=10, pady=(0, 10))

        self.analyze_button = ctk.CTkButton(
            self.button_frame,
            text="Analyze",
            command=self.analyze_progression
        )
        self.analyze_button.pack(side="left", padx=(0, 10))

        self.advanced_button = ctk.CTkButton(
            self.button_frame,
            text="🎯 Advanced Analysis",
            command=self.show_advanced_analysis,
            fg_color="#FF6B6B",
            hover_color="#FF5252"
        )
        self.advanced_button.pack(side="left", padx=(0, 10))

        self.clear_button = ctk.CTkButton(
            self.button_frame,
            text="Clear",
            command=self.clear_progression
        )
        self.clear_button.pack(side="left", padx=(0, 10))

        # Example progressions
        self.example_label = ctk.CTkLabel(
            self.button_frame,
            text="Examples:",
            font=ctk.CTkFont(weight="bold")
        )
        self.example_label.pack(side="left", padx=(20, 5))

        self.example_var = ctk.StringVar()
        self.example_menu = ctk.CTkOptionMenu(
            self.button_frame,
            values=self.example_progressions,
            variable=self.example_var,
            command=self.load_example
        )
        self.example_menu.pack(side="left")

        # Results display
        self.results_frame = ctk.CTkFrame(self)
        self.results_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # Progression info
        self.progression_info_label = ctk.CTkLabel(
            self.results_frame,
            text="Progression Analysis",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.progression_info_label.pack(pady=(20, 10))

        # Basic analysis
        self.basic_frame = ctk.CTkFrame(self.results_frame)
        self.basic_frame.pack(fill="x", padx=20, pady=(0, 15))

        self.chords_label = ctk.CTkLabel(
            self.basic_frame,
            text="Chords:",
            font=ctk.CTkFont(weight="bold")
        )
        self.chords_label.pack(anchor="w", padx=10, pady=(10, 5))

        self.chords_display = ctk.CTkLabel(
            self.basic_frame,
            text="No progression analyzed",
            font=ctk.CTkFont(size=14)
        )
        self.chords_display.pack(anchor="w", padx=10, pady=(0, 10))

        self.notes_label = ctk.CTkLabel(
            self.basic_frame,
            text="All Notes:",
            font=ctk.CTkFont(weight="bold")
        )
        self.notes_label.pack(anchor="w", padx=10, pady=(0, 5))

        self.notes_display = ctk.CTkLabel(
            self.basic_frame,
            text="",
            font=ctk.CTkFont(size=14)
        )
        self.notes_display.pack(anchor="w", padx=10, pady=(0, 10))

        self.key_label = ctk.CTkLabel(
            self.basic_frame,
            text="Detected Key:",
            font=ctk.CTkFont(weight="bold")
        )
        self.key_label.pack(anchor="w", padx=10, pady=(0, 5))

        self.key_display = ctk.CTkLabel(
            self.basic_frame,
            text="",
            font=ctk.CTkFont(size=14)
        )
        self.key_display.pack(anchor="w", padx=10, pady=(0, 10))

        self.complexity_label = ctk.CTkLabel(
            self.basic_frame,
            text="Complexity:",
            font=ctk.CTkFont(weight="bold")
        )
        self.complexity_label.pack(anchor="w", padx=10, pady=(0, 5))

        self.complexity_display = ctk.CTkLabel(
            self.basic_frame,
            text="",
            font=ctk.CTkFont(size=14)
        )
        self.complexity_display.pack(anchor="w", padx=10, pady=(0, 10))

        # Scale suggestions
        self.scales_frame = ctk.CTkFrame(self.results_frame)
        self.scales_frame.pack(fill="x", padx=20, pady=(0, 15))

        self.scales_label = ctk.CTkLabel(
            self.scales_frame,
            text="Compatible Scales (for improvisation):",
            font=ctk.CTkFont(weight="bold")
        )
        self.scales_label.pack(anchor="w", padx=10, pady=(10, 5))

        self.scales_display = ctk.CTkTextbox(
            self.scales_frame,
            height=120,
            wrap="word"
        )
        self.scales_display.pack(fill="x", padx=10, pady=(0, 10))

        # Additional analysis
        self.analysis_frame = ctk.CTkFrame(self.results_frame)
        self.analysis_frame.pack(fill="x", padx=20, pady=(0, 20))

        self.analysis_label = ctk.CTkLabel(
            self.analysis_frame,
            text="Additional Analysis:",
            font=ctk.CTkFont(weight="bold")
        )
        self.analysis_label.pack(anchor="w", padx=10, pady=(10, 5))

        self.analysis_display = ctk.CTkTextbox(
            self.analysis_frame,
            height=80,
            wrap="word"
        )
        self.analysis_display.pack(fill="x", padx=10, pady=(0, 10))

    def analyze_progression(self):
        """Analyze the entered chord progression."""
        progression_text = self.progression_entry.get().strip()

        if not progression_text:
            self.clear_results()
            return

        try:
            # Parse chord progression
            chord_list = progression_text.split()

            # Create progression object
            self.current_progression = ProgressionAnalyzerCore.analyze_progression(chord_list)

            # Update display
            self.update_display()

        except Exception as e:
            self.show_error(f"Error analyzing progression: {str(e)}")

    def show_advanced_analysis(self):
        """Show advanced harmonic analysis in a new window."""
        if not self.current_progression:
            self.show_error("Please analyze a progression first.")
            return

        try:
            # Create analysis window
            analysis_window = ctk.CTkToplevel(self)
            analysis_window.title("Advanced Harmonic Analysis")
            analysis_window.geometry("900x700")

            # Center on parent
            x = self.winfo_x() + self.winfo_width() // 2 - 450
            y = self.winfo_y() + self.winfo_height() // 2 - 350
            analysis_window.geometry(f"+{x}+{y}")

            # Create dashboard
            dashboard = AnalyticsVisualizer.create_analytics_dashboard(
                analysis_window, self.current_progression, width=850, height=600
            )

            # Close button
            close_button = ctk.CTkButton(
                analysis_window,
                text="Close",
                command=analysis_window.destroy
            )
            close_button.pack(pady=10)

        except Exception as e:
            self.show_error(f"Error creating advanced analysis: {str(e)}")

    def load_example(self, example: str):
        """Load an example progression."""
        self.progression_entry.delete(0, 'end')
        self.progression_entry.insert(0, example)
        self.analyze_progression()

    def clear_progression(self):
        """Clear the current progression and results."""
        self.progression_entry.delete(0, 'end')
        self.clear_results()
        self.current_progression = None

    def clear_results(self):
        """Clear all result displays."""
        self.chords_display.configure(text="No progression analyzed")
        self.notes_display.configure(text="")
        self.key_display.configure(text="")
        self.complexity_display.configure(text="")

        self.scales_display.delete("1.0", "end")
        self.analysis_display.delete("1.0", "end")

    def update_display(self):
        """Update the display with analysis results."""
        if not self.current_progression:
            self.clear_results()
            return

        # Update basic info
        chords_text = str(self.current_progression)
        self.chords_display.configure(text=chords_text)

        notes_text = " ".join(sorted(self.current_progression.all_note_names))
        self.notes_display.configure(text=notes_text)

        key_text = self.current_progression.key_name or "Undetermined"
        self.key_display.configure(text=key_text)

        # Add advanced metrics to complexity display
        try:
            analysis = HarmonicAnalyzer.analyze_progression(self.current_progression)
            complexity_data = analysis.get('complexity_metrics', {})
            tension_data = analysis.get('tension_profile', {})

            complexity_text = complexity_data.get('complexity_description', 'Unknown')
            avg_tension = tension_data.get('average_tension', 0)

            complexity_info = f"{complexity_text} (Tension: {avg_tension:.1f}/10)"
            self.complexity_display.configure(text=complexity_info)

        except Exception:
            # Fallback to basic complexity if advanced analysis fails
            complexity = self.current_progression._analysis.get('complexity', 'simple')
            self.complexity_display.configure(text=complexity.title())

        complexity_text = self.current_progression.analysis.get('complexity', 'Unknown')
        self.complexity_display.configure(text=complexity_text.title())

        # Update scale suggestions
        scales = ProgressionAnalyzerCore.suggest_scales_for_improvisation(
            self.current_progression, max_suggestions=5
        )

        scales_text = ""
        for i, scale in enumerate(scales, 1):
            scales_text += f"{i}. {scale.name}\n"

        if not scales_text:
            scales_text = "No compatible scales found"

        self.scales_display.delete("1.0", "end")
        self.scales_display.insert("1.0", scales_text.strip())

        # Update additional analysis
        analysis_text = self.get_additional_analysis()
        self.analysis_display.delete("1.0", "end")
        self.analysis_display.insert("1.0", analysis_text)

    def get_additional_analysis(self) -> str:
        """Get additional analysis information."""
        if not self.current_progression:
            return ""

        analysis = []

        # Cadence detection
        cadences = ProgressionAnalyzerCore.get_progression_cadences(self.current_progression)
        if cadences:
            analysis.append(f"Cadences detected: {', '.join(cadences)}")
        else:
            analysis.append("No specific cadences detected")

        # Scale count
        all_scales = ProgressionAnalyzerCore.find_compatible_scales(self.current_progression)
        analysis.append(f"Total compatible scales found: {len(all_scales)}")

        # Progression length
        length = ProgressionAnalyzerCore.get_progression_length(self.current_progression)
        analysis.append(f"Progression length: {length} chords")

        return "\n".join(analysis)

    def show_error(self, message: str):
        """Show an error message."""
        error_window = ctk.CTkToplevel(self)
        error_window.title("Analysis Error")
        error_window.geometry("400x150")

        # Center on parent
        x = self.winfo_x() + self.winfo_width() // 2 - 200
        y = self.winfo_y() + self.winfo_height() // 2 - 75
        error_window.geometry(f"+{x}+{y}")

        error_label = ctk.CTkLabel(
            error_window,
            text=message,
            wraplength=350
        )
        error_label.pack(pady=20, padx=20)

        ok_button = ctk.CTkButton(
            error_window,
            text="OK",
            command=error_window.destroy
        )
        ok_button.pack(pady=(0, 20))

    def save_preset(self, name: str, description: str = "") -> bool:
        """
        Save current progression configuration as a preset.

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
                category='progressions',
                name=name,
                data=state,
                description=description
            )
        except Exception as e:
            print(f"Error saving progression preset: {e}")
            return False

    def load_preset(self, name: str) -> bool:
        """
        Load a progression preset.

        Args:
            name: Preset name

        Returns:
            True if successful, False otherwise
        """
        try:
            preset_manager = get_preset_manager()

            preset = preset_manager.load_preset('progressions', name)
            if not preset:
                return False

            # Apply preset state
            return self.apply_state(preset['data'])

        except Exception as e:
            print(f"Error loading progression preset: {e}")
            return False

    def get_current_state(self) -> dict:
        """
        Get current progression analyzer state for saving.

        Returns:
            Dictionary containing current state
        """
        state = {
            'progression_text': getattr(self.progression_entry, 'get', lambda: '')() if hasattr(self, 'progression_entry') else '',
            'selected_progression': getattr(self.progression_var, 'get', lambda: '')() if hasattr(self, 'progression_var') else '',
            'current_progression': str(self.current_progression) if self.current_progression else None
        }
        return state

    def apply_state(self, state: dict) -> bool:
        """
        Apply a saved state to the progression analyzer.

        Args:
            state: State dictionary

        Returns:
            True if successful, False otherwise
        """
        try:
            # Set progression text
            if 'progression_text' in state and hasattr(self, 'progression_entry'):
                self.progression_entry.delete(0, 'end')
                self.progression_entry.insert(0, state['progression_text'])

            # Set selected progression
            if 'selected_progression' in state and hasattr(self, 'progression_var'):
                self.progression_var.set(state['selected_progression'])

            # Analyze progression
            if 'progression_text' in state and state['progression_text']:
                self.analyze_progression()

            return True

        except Exception as e:
            print(f"Error applying progression state: {e}")
            return False

    def get_export_data(self) -> str:
        """Get data for export."""
        if not self.current_progression:
            return "No progression data to export"

        data = f"Progression: {self.current_progression}\n"
        data += f"Key: {self.current_progression.key_name or 'Undetermined'}\n"
        data += f"Complexity: {self.current_progression.analysis.get('complexity', 'Unknown')}\n"
        data += f"All Notes: {' '.join(sorted(self.current_progression.all_note_names))}\n\n"

        # Compatible scales
        scales = ProgressionAnalyzerCore.suggest_scales_for_improvisation(
            self.current_progression, max_suggestions=10
        )
        data += "Compatible Scales:\n"
        for i, scale in enumerate(scales, 1):
            data += f"{i}. {scale.name}\n"
        data += "\n"

        # Additional analysis
        data += "Additional Analysis:\n"
        data += self.get_additional_analysis()
        data += "\n"

        return data
