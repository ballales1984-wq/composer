"""
Preset Manager for Music Theory Engine.

This module provides functionality for saving and loading presets
(configurations) for scales, chords, progressions, and other settings.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging

# Setup logging
logger = logging.getLogger(__name__)


class PresetManager:
    """
    Manages presets for the Music Theory Engine.

    Features:
    - Save/load presets in JSON format
    - Preset categories (scales, chords, progressions, sessions)
    - Automatic timestamping
    - Preset validation
    - User-friendly preset names
    """

    def __init__(self, preset_dir: str = "presets"):
        """
        Initialize the preset manager.

        Args:
            preset_dir: Directory to store preset files
        """
        self.preset_dir = Path(preset_dir)
        self.preset_dir.mkdir(exist_ok=True)

        # Preset categories
        self.categories = {
            'scales': self.preset_dir / 'scales',
            'chords': self.preset_dir / 'chords',
            'progressions': self.preset_dir / 'progressions',
            'arpeggios': self.preset_dir / 'arpeggios',
            'sessions': self.preset_dir / 'sessions'
        }

        # Create category directories
        for category_dir in self.categories.values():
            category_dir.mkdir(exist_ok=True)

        logger.info(f"PresetManager initialized with directory: {self.preset_dir}")

    def save_preset(self, category: str, name: str, data: Dict[str, Any],
                   description: str = "") -> bool:
        """
        Save a preset to file.

        Args:
            category: Preset category ('scales', 'chords', etc.)
            name: Preset name
            data: Preset data dictionary
            description: Optional description

        Returns:
            True if successful, False otherwise
        """
        try:
            if category not in self.categories:
                logger.error(f"Invalid category: {category}")
                return False

            # Create preset data structure
            preset_data = {
                'name': name,
                'description': description,
                'timestamp': datetime.now().isoformat(),
                'category': category,
                'version': '1.0',
                'data': data
            }

            # Sanitize filename
            safe_name = self._sanitize_filename(name)
            file_path = self.categories[category] / f"{safe_name}.json"

            # Save to file
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(preset_data, f, indent=2, ensure_ascii=False)

            logger.info(f"Preset saved: {file_path}")
            return True

        except Exception as e:
            logger.error(f"Failed to save preset {name}: {e}")
            return False

    def load_preset(self, category: str, name: str) -> Optional[Dict[str, Any]]:
        """
        Load a preset from file.

        Args:
            category: Preset category
            name: Preset name

        Returns:
            Preset data dictionary or None if not found
        """
        try:
            if category not in self.categories:
                logger.error(f"Invalid category: {category}")
                return None

            safe_name = self._sanitize_filename(name)
            file_path = self.categories[category] / f"{safe_name}.json"

            if not file_path.exists():
                logger.warning(f"Preset not found: {file_path}")
                return None

            with open(file_path, 'r', encoding='utf-8') as f:
                preset_data = json.load(f)

            logger.info(f"Preset loaded: {file_path}")
            return preset_data

        except Exception as e:
            logger.error(f"Failed to load preset {name}: {e}")
            return None

    def list_presets(self, category: str) -> List[Dict[str, Any]]:
        """
        List all presets in a category.

        Args:
            category: Preset category

        Returns:
            List of preset info dictionaries
        """
        try:
            if category not in self.categories:
                logger.error(f"Invalid category: {category}")
                return []

            category_dir = self.categories[category]
            presets = []

            for file_path in category_dir.glob("*.json"):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        preset_data = json.load(f)

                    # Add file info
                    preset_info = {
                        'name': preset_data.get('name', file_path.stem),
                        'description': preset_data.get('description', ''),
                        'timestamp': preset_data.get('timestamp', ''),
                        'category': preset_data.get('category', category),
                        'filename': file_path.name
                    }
                    presets.append(preset_info)

                except Exception as e:
                    logger.warning(f"Could not load preset file {file_path}: {e}")

            # Sort by timestamp (newest first)
            presets.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
            return presets

        except Exception as e:
            logger.error(f"Failed to list presets for category {category}: {e}")
            return []

    def delete_preset(self, category: str, name: str) -> bool:
        """
        Delete a preset file.

        Args:
            category: Preset category
            name: Preset name

        Returns:
            True if successful, False otherwise
        """
        try:
            if category not in self.categories:
                logger.error(f"Invalid category: {category}")
                return False

            safe_name = self._sanitize_filename(name)
            file_path = self.categories[category] / f"{safe_name}.json"

            if file_path.exists():
                file_path.unlink()
                logger.info(f"Preset deleted: {file_path}")
                return True
            else:
                logger.warning(f"Preset not found for deletion: {file_path}")
                return False

        except Exception as e:
            logger.error(f"Failed to delete preset {name}: {e}")
            return False

    def save_session_preset(self, session_data: Dict[str, Any],
                           name: str = None) -> bool:
        """
        Save a complete session preset with all current settings.

        Args:
            session_data: Dictionary containing all component states
            name: Optional session name (auto-generated if None)

        Returns:
            True if successful, False otherwise
        """
        if name is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            name = f"Session_{timestamp}"

        return self.save_preset(
            category='sessions',
            name=name,
            data=session_data,
            description="Complete session configuration"
        )

    def load_session_preset(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Load a complete session preset.

        Args:
            name: Session preset name

        Returns:
            Session data dictionary or None if not found
        """
        preset = self.load_preset('sessions', name)
        return preset.get('data') if preset else None

    def get_preset_stats(self) -> Dict[str, int]:
        """
        Get statistics about stored presets.

        Returns:
            Dictionary with preset counts per category
        """
        stats = {}
        for category in self.categories:
            presets = self.list_presets(category)
            stats[category] = len(presets)
        return stats

    def _sanitize_filename(self, name: str) -> str:
        """
        Sanitize a string to be used as a filename.

        Args:
            name: Input string

        Returns:
            Sanitized filename-safe string
        """
        # Replace invalid characters with underscores
        invalid_chars = '<>:"/\\|?*'
        safe_name = name
        for char in invalid_chars:
            safe_name = safe_name.replace(char, '_')

        # Remove leading/trailing spaces and dots
        safe_name = safe_name.strip(' .')

        # Ensure not empty
        if not safe_name:
            safe_name = "unnamed_preset"

        return safe_name


# Global preset manager instance
_preset_manager = None

def get_preset_manager() -> PresetManager:
    """Get the global preset manager instance."""
    global _preset_manager
    if _preset_manager is None:
        _preset_manager = PresetManager()
    return _preset_manager