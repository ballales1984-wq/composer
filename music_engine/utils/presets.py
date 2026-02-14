"""
Preset management for the Music Theory Engine.

This module provides functionality for saving and loading user presets
for scales, chords, and progressions.
"""

import json
import os
from typing import Dict, List, Any, Optional
from pathlib import Path


class PresetManager:
    """
    Manages user presets for scales, chords, and progressions.
    """

    def __init__(self, preset_dir: str = None):
        """
        Initialize the preset manager.

        Args:
            preset_dir: Directory to store presets (default: user data directory)
        """
        if preset_dir is None:
            # Use user data directory
            home_dir = Path.home()
            if os.name == 'nt':  # Windows
                preset_dir = home_dir / "AppData" / "Local" / "MusicTheoryEngine"
            else:  # Unix/Linux/Mac
                preset_dir = home_dir / ".config" / "music_theory_engine"

        self.preset_dir = Path(preset_dir)
        self.preset_dir.mkdir(parents=True, exist_ok=True)

        # Preset files
        self.scale_presets_file = self.preset_dir / "scale_presets.json"
        self.chord_presets_file = self.preset_dir / "chord_presets.json"
        self.progression_presets_file = self.preset_dir / "progression_presets.json"

        # Load existing presets
        self.scale_presets = self._load_presets(self.scale_presets_file)
        self.chord_presets = self._load_presets(self.chord_presets_file)
        self.progression_presets = self._load_presets(self.progression_presets_file)

    def _load_presets(self, file_path: Path) -> Dict[str, Any]:
        """Load presets from a JSON file."""
        if file_path.exists():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading presets from {file_path}: {e}")
                return {}
        return {}

    def _save_presets(self, presets: Dict[str, Any], file_path: Path):
        """Save presets to a JSON file."""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(presets, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving presets to {file_path}: {e}")

    # Scale presets
    def save_scale_preset(self, name: str, root: str, scale_type: str):
        """
        Save a scale preset.

        Args:
            name: Preset name
            root: Root note
            scale_type: Scale type
        """
        self.scale_presets[name] = {
            'root': root,
            'scale_type': scale_type,
            'created': str(Path.cwd())
        }
        self._save_presets(self.scale_presets, self.scale_presets_file)

    def load_scale_preset(self, name: str) -> Optional[Dict[str, str]]:
        """Load a scale preset."""
        return self.scale_presets.get(name)

    def get_scale_preset_names(self) -> List[str]:
        """Get list of scale preset names."""
        return list(self.scale_presets.keys())

    def delete_scale_preset(self, name: str):
        """Delete a scale preset."""
        if name in self.scale_presets:
            del self.scale_presets[name]
            self._save_presets(self.scale_presets, self.scale_presets_file)

    # Chord presets
    def save_chord_preset(self, name: str, root: str, quality: str, inversion: int = 0):
        """
        Save a chord preset.

        Args:
            name: Preset name
            root: Root note
            quality: Chord quality
            inversion: Chord inversion
        """
        self.chord_presets[name] = {
            'root': root,
            'quality': quality,
            'inversion': inversion,
            'created': str(Path.cwd())
        }
        self._save_presets(self.chord_presets, self.chord_presets_file)

    def load_chord_preset(self, name: str) -> Optional[Dict[str, Any]]:
        """Load a chord preset."""
        return self.chord_presets.get(name)

    def get_chord_preset_names(self) -> List[str]:
        """Get list of chord preset names."""
        return list(self.chord_presets.keys())

    def delete_chord_preset(self, name: str):
        """Delete a chord preset."""
        if name in self.chord_presets:
            del self.chord_presets[name]
            self._save_presets(self.chord_presets, self.chord_presets_file)

    # Progression presets
    def save_progression_preset(self, name: str, chords: List[str]):
        """
        Save a progression preset.

        Args:
            name: Preset name
            chords: List of chord symbols
        """
        self.progression_presets[name] = {
            'chords': chords,
            'created': str(Path.cwd())
        }
        self._save_presets(self.progression_presets, self.progression_presets_file)

    def load_progression_preset(self, name: str) -> Optional[Dict[str, Any]]:
        """Load a progression preset."""
        return self.progression_presets.get(name)

    def get_progression_preset_names(self) -> List[str]:
        """Get list of progression preset names."""
        return list(self.progression_presets.keys())

    def delete_progression_preset(self, name: str):
        """Delete a progression preset."""
        if name in self.progression_presets:
            del self.progression_presets[name]
            self._save_presets(self.progression_presets, self.progression_presets_file)

    # Session management
    def save_session(self, session_data: Dict[str, Any], filename: str = "session.json"):
        """
        Save a complete session.

        Args:
            session_data: Session data dictionary
            filename: Session filename
        """
        session_file = self.preset_dir / filename
        try:
            with open(session_file, 'w', encoding='utf-8') as f:
                json.dump(session_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving session: {e}")

    def load_session(self, filename: str = "session.json") -> Optional[Dict[str, Any]]:
        """Load a session."""
        session_file = self.preset_dir / filename
        if session_file.exists():
            try:
                with open(session_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading session: {e}")
        return None


# Global preset manager instance
_preset_manager = None

def get_preset_manager() -> PresetManager:
    """Get the global preset manager instance."""
    global _preset_manager
    if _preset_manager is None:
        _preset_manager = PresetManager()
    return _preset_manager