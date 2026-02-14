"""
Preset Manager GUI component.

This module provides an interface for managing presets
(save/load configurations) for the Music Theory Engine.
"""

import customtkinter as ctk
from tkinter import messagebox
from typing import List, Dict, Any, Optional, Callable
import sys
import os

# Import modules
from ..utils.preset_manager import get_preset_manager, PresetManager


class PresetManagerGUI(ctk.CTkFrame):
    """
    Interactive preset management interface.

    Features:
    - Save current configurations as presets
    - Load saved presets
    - Manage preset categories
    - Delete unwanted presets
    - Preset descriptions and timestamps
    """

    def __init__(self, parent):
        super().__init__(parent)

        # Pack this frame to fill the parent tab
        self.pack(fill="both", expand=True)

        # Preset manager
        self.preset_manager = get_preset_manager()

        # Callbacks for loading presets in other components
        self.load_callbacks = {
            'scales': None,
            'chords': None,
            'progressions': None,
            'arpeggios': None,
            'sessions': None
        }

        self._create_interface()

    def _create_interface(self):
        """Create the preset management interface."""
        # Main container
        main_container = ctk.CTkFrame(self)
        main_container.pack(fill="both", expand=True, padx=20, pady=20)

        # Title
        title_label = ctk.CTkLabel(
            main_container,
            text="🎵 Preset Manager",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(pady=(0, 10))

        # Create sections
        self._create_save_section(main_container)
        self._create_load_section(main_container)
        self._create_stats_section(main_container)

    def _create_save_section(self, parent):
        """Create the save preset section."""
        save_frame = ctk.CTkFrame(parent)
        save_frame.pack(fill="x", pady=(0, 20))

        # Save section title
        save_title = ctk.CTkLabel(
            save_frame,
            text="💾 Save Current Configuration",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        save_title.pack(pady=(20, 10))

        # Preset name input
        name_frame = ctk.CTkFrame(save_frame)
        name_frame.pack(fill="x", padx=20, pady=(0, 10))

        ctk.CTkLabel(name_frame, text="Preset Name:").pack(side="left", padx=(0, 10))

        self.save_name_entry = ctk.CTkEntry(
            name_frame,
            placeholder_text="Enter preset name...",
            width=250
        )
        self.save_name_entry.pack(side="left", padx=(0, 10))

        # Category selector
        category_frame = ctk.CTkFrame(save_frame)
        category_frame.pack(fill="x", padx=20, pady=(0, 15))

        ctk.CTkLabel(category_frame, text="Category:").pack(side="left", padx=(0, 10))

        self.save_category_var = ctk.StringVar(value="scales")
        category_menu = ctk.CTkOptionMenu(
            category_frame,
            values=["scales", "chords", "progressions", "arpeggios"],
            variable=self.save_category_var,
            width=150
        )
        category_menu.pack(side="left", padx=(0, 10))

        # Description input
        desc_frame = ctk.CTkFrame(save_frame)
        desc_frame.pack(fill="x", padx=20, pady=(0, 15))

        ctk.CTkLabel(desc_frame, text="Description:").pack(anchor="w", padx=(0, 10))

        self.save_desc_entry = ctk.CTkEntry(
            desc_frame,
            placeholder_text="Optional description...",
            width=400
        )
        self.save_desc_entry.pack(fill="x", padx=(0, 10), pady=(5, 0))

        # Save button
        save_button = ctk.CTkButton(
            save_frame,
            text="💾 Save Preset",
            command=self._save_current_preset,
            fg_color="#4CAF50",
            hover_color="#45A049"
        )
        save_button.pack(pady=(0, 20))

    def _create_load_section(self, parent):
        """Create the load preset section."""
        load_frame = ctk.CTkFrame(parent)
        load_frame.pack(fill="both", expand=True, pady=(0, 20))

        # Load section title
        load_title = ctk.CTkLabel(
            load_frame,
            text="📂 Load Saved Presets",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        load_title.pack(pady=(20, 10))

        # Category selector for loading
        category_frame = ctk.CTkFrame(load_frame)
        category_frame.pack(fill="x", padx=20, pady=(0, 10))

        ctk.CTkLabel(category_frame, text="Category:").pack(side="left", padx=(0, 10))

        self.load_category_var = ctk.StringVar(value="scales")
        category_menu = ctk.CTkOptionMenu(
            category_frame,
            values=["scales", "chords", "progressions", "arpeggios"],
            variable=self.load_category_var,
            command=self._update_preset_list,
            width=150
        )
        category_menu.pack(side="left")

        # Preset list
        list_frame = ctk.CTkFrame(load_frame)
        list_frame.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        # Preset listbox (using scrollbar and text for simplicity)
        self.preset_textbox = ctk.CTkTextbox(
            list_frame,
            wrap="none",
            font=ctk.CTkFont(size=10)
        )
        self.preset_textbox.pack(fill="both", expand=True, padx=10, pady=10)

        # Action buttons
        buttons_frame = ctk.CTkFrame(load_frame)
        buttons_frame.pack(fill="x", padx=20, pady=(0, 20))

        load_button = ctk.CTkButton(
            buttons_frame,
            text="📂 Load Selected",
            command=self._load_selected_preset,
            fg_color="#2196F3",
            hover_color="#1976D2"
        )
        load_button.pack(side="left", padx=(0, 10))

        delete_button = ctk.CTkButton(
            buttons_frame,
            text="🗑️ Delete Selected",
            command=self._delete_selected_preset,
            fg_color="#F44336",
            hover_color="#D32F2F"
        )
        delete_button.pack(side="left")

        refresh_button = ctk.CTkButton(
            buttons_frame,
            text="🔄 Refresh",
            command=self._update_preset_list
        )
        refresh_button.pack(side="right")

        # Initialize preset list
        self._update_preset_list()

    def _create_stats_section(self, parent):
        """Create the statistics section."""
        stats_frame = ctk.CTkFrame(parent)
        stats_frame.pack(fill="x", pady=(0, 10))

        stats_title = ctk.CTkLabel(
            stats_frame,
            text="📊 Preset Statistics",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        stats_title.pack(pady=(10, 5))

        self.stats_label = ctk.CTkLabel(
            stats_frame,
            text="Loading...",
            font=ctk.CTkFont(size=11)
        )
        self.stats_label.pack(pady=(0, 10))

        self._update_stats()

    def _save_current_preset(self):
        """Save the current configuration as a preset."""
        name = self.save_name_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Please enter a preset name.")
            return

        category = self.save_category_var.get()
        description = self.save_desc_entry.get().strip()

        # Call the appropriate save method based on category
        save_method = getattr(self, f"_save_{category}_preset", None)
        if save_method:
            if save_method(name, description):
                messagebox.showinfo("Success", f"Preset '{name}' saved successfully!")
                self.save_name_entry.delete(0, 'end')
                self.save_desc_entry.delete(0, 'end')
                self._update_preset_list()
                self._update_stats()
            else:
                messagebox.showerror("Error", f"Failed to save preset '{name}'.")
        else:
            messagebox.showerror("Error", f"No save method available for category '{category}'.")

    def _save_scales_preset(self, name: str, description: str) -> bool:
        """Save current scale configuration."""
        # This will be called from the main window
        if hasattr(self.master.master, 'scale_explorer'):
            return self.master.master.scale_explorer.save_preset(name, description)
        return False

    def _save_chords_preset(self, name: str, description: str) -> bool:
        """Save current chord configuration."""
        if hasattr(self.master.master, 'chord_builder'):
            return self.master.master.chord_builder.save_preset(name, description)
        return False

    def _save_progressions_preset(self, name: str, description: str) -> bool:
        """Save current progression configuration."""
        if hasattr(self.master.master, 'progression_analyzer'):
            return self.master.master.progression_analyzer.save_preset(name, description)
        return False

    def _save_arpeggios_preset(self, name: str, description: str) -> bool:
        """Save current arpeggio configuration."""
        if hasattr(self.master.master, 'arpeggio_viewer'):
            return self.master.master.arpeggio_viewer.save_preset(name, description)
        return False

    def _load_selected_preset(self):
        """Load the selected preset."""
        try:
            # Get selected text from textbox
            selected_text = self.preset_textbox.get("sel.first", "sel.last")
            if not selected_text:
                messagebox.showwarning("Warning", "Please select a preset from the list.")
                return

            # Extract preset name (first line)
            preset_name = selected_text.split('\n')[0].strip()

            category = self.load_category_var.get()

            # Call the appropriate load method
            load_method = getattr(self, f"_load_{category}_preset", None)
            if load_method:
                if load_method(preset_name):
                    messagebox.showinfo("Success", f"Preset '{preset_name}' loaded successfully!")
                    # Switch to the appropriate tab
                    self._switch_to_tab(category)
                else:
                    messagebox.showerror("Error", f"Failed to load preset '{preset_name}'.")
            else:
                messagebox.showerror("Error", f"No load method available for category '{category}'.")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load preset: {str(e)}")

    def _load_scales_preset(self, name: str) -> bool:
        """Load a scale preset."""
        if hasattr(self.master.master, 'scale_explorer'):
            return self.master.master.scale_explorer.load_preset(name)
        return False

    def _load_chords_preset(self, name: str) -> bool:
        """Load a chord preset."""
        if hasattr(self.master.master, 'chord_builder'):
            return self.master.master.chord_builder.load_preset(name)
        return False

    def _load_progressions_preset(self, name: str) -> bool:
        """Load a progression preset."""
        if hasattr(self.master.master, 'progression_analyzer'):
            return self.master.master.progression_analyzer.load_preset(name)
        return False

    def _load_arpeggios_preset(self, name: str) -> bool:
        """Load an arpeggio preset."""
        if hasattr(self.master.master, 'arpeggio_viewer'):
            return self.master.master.arpeggio_viewer.load_preset(name)
        return False

    def _delete_selected_preset(self):
        """Delete the selected preset."""
        try:
            # Get selected text from textbox
            selected_text = self.preset_textbox.get("sel.first", "sel.last")
            if not selected_text:
                messagebox.showwarning("Warning", "Please select a preset from the list.")
                return

            # Extract preset name
            preset_name = selected_text.split('\n')[0].strip()

            # Confirm deletion
            if not messagebox.askyesno("Confirm Delete",
                                     f"Are you sure you want to delete preset '{preset_name}'?"):
                return

            category = self.load_category_var.get()
            if self.preset_manager.delete_preset(category, preset_name):
                messagebox.showinfo("Success", f"Preset '{preset_name}' deleted successfully!")
                self._update_preset_list()
                self._update_stats()
            else:
                messagebox.showerror("Error", f"Failed to delete preset '{preset_name}'.")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete preset: {str(e)}")

    def _update_preset_list(self, category=None):
        """Update the preset list display."""
        if category is None:
            category = self.load_category_var.get()

        presets = self.preset_manager.list_presets(category)

        # Clear textbox
        self.preset_textbox.delete("0.0", "end")

        if not presets:
            self.preset_textbox.insert("0.0", f"No presets found in category '{category}'.")
            return

        # Add presets to textbox
        for preset in presets:
            name = preset.get('name', 'Unknown')
            desc = preset.get('description', '')
            timestamp = preset.get('timestamp', '')[:19]  # Show only date/time

            preset_text = f"{name}\n"
            if desc:
                preset_text += f"  Description: {desc}\n"
            preset_text += f"  Created: {timestamp}\n"
            preset_text += "-" * 40 + "\n"

            self.preset_textbox.insert("end", preset_text)

    def _update_stats(self):
        """Update the statistics display."""
        stats = self.preset_manager.get_preset_stats()
        stats_text = " | ".join([f"{cat}: {count}" for cat, count in stats.items()])
        self.stats_label.configure(text=stats_text)

    def _switch_to_tab(self, category: str):
        """Switch to the appropriate tab after loading a preset."""
        tab_mapping = {
            'scales': "Scale Explorer",
            'chords': "Chord Builder",
            'progressions': "Progression Analyzer",
            'arpeggios': "Arpeggio Viewer"
        }

        if category in tab_mapping and hasattr(self.master.master, 'tabview'):
            try:
                self.master.master.tabview.set(tab_mapping[category])
            except:
                pass  # Ignore if tab switching fails