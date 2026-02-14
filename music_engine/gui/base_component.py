"""
Base component class for GUI components.

This module provides a base class for all GUI components in the Music Theory Engine,
reducing code duplication and providing common functionality.
"""

import customtkinter as ctk
from typing import Optional, Callable, Any
from abc import ABC, abstractmethod


class BaseComponent(ctk.CTkFrame, ABC):
    """
    Base class for all GUI components in the Music Theory Engine.

    Provides common functionality like:
    - Standard layout structure
    - Fretboard integration
    - Error handling
    - Tooltips support
    - Keyboard shortcuts
    """

    def __init__(self, parent, title: str = "", **kwargs):
        """
        Initialize the base component.

        Args:
            parent: Parent widget
            title: Component title
            **kwargs: Additional arguments for CTkFrame
        """
        super().__init__(parent, **kwargs)

        # Pack this frame to fill the parent tab
        self.pack(fill="both", expand=True)

        # Component data
        self.title = title
        self.fretboard_callback: Optional[Callable] = None

        # Common UI elements
        self.main_frame = None
        self.title_label = None
        self.controls_frame = None
        self.info_frame = None

        # Setup common UI structure
        self._setup_common_ui()

    def _setup_common_ui(self):
        """Setup the common UI structure shared by all components."""
        # Main container
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Title (if provided)
        if self.title:
            self.title_label = ctk.CTkLabel(
                self.main_frame,
                text=self.title,
                font=ctk.CTkFont(size=18, weight="bold")
            )
            self.title_label.pack(pady=(10, 15))

        # Controls section (to be customized by subclasses)
        self.controls_frame = ctk.CTkFrame(self.main_frame)
        self.controls_frame.pack(fill="x", padx=10, pady=(0, 10))

        # Info display section
        self.info_frame = ctk.CTkFrame(self.main_frame)
        self.info_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # Call subclass-specific setup
        self.setup_ui()

    @abstractmethod
    def setup_ui(self):
        """Setup component-specific UI. Must be implemented by subclasses."""
        pass

    def set_fretboard_callback(self, callback: Callable):
        """
        Set the callback for fretboard integration.

        Args:
            callback: Function to call when showing on fretboard
        """
        self.fretboard_callback = callback

    def show_on_fretboard(self):
        """Show current data on the fretboard."""
        if self.fretboard_callback:
            try:
                self.fretboard_callback()
            except Exception as e:
                print(f"Error showing on fretboard: {e}")
        else:
            print("Fretboard callback not set")

    def add_tooltip(self, widget: ctk.CTkBaseClass, text: str):
        """
        Add a tooltip to a widget.

        Args:
            widget: The widget to add tooltip to
            text: Tooltip text
        """
        def on_enter(event):
            # Create tooltip window
            tooltip = ctk.CTkToplevel(widget)
            tooltip.title("")
            tooltip.geometry("200x50")
            tooltip.overrideredirect(True)

            # Position tooltip near widget
            x = widget.winfo_rootx() + 20
            y = widget.winfo_rooty() + widget.winfo_height() + 5
            tooltip.geometry(f"+{x}+{y}")

            # Add tooltip text
            label = ctk.CTkLabel(tooltip, text=text, font=ctk.CTkFont(size=10))
            label.pack(padx=5, pady=2)

            self._current_tooltip = tooltip

        def on_leave(event):
            if hasattr(self, '_current_tooltip'):
                self._current_tooltip.destroy()
                delattr(self, '_current_tooltip')

        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)

    def create_action_button(self, parent, text: str, command: Callable,
                           tooltip: str = "", **kwargs) -> ctk.CTkButton:
        """
        Create a standardized action button.

        Args:
            parent: Parent widget
            text: Button text
            command: Button command
            tooltip: Optional tooltip text
            **kwargs: Additional button arguments

        Returns:
            The created button
        """
        button = ctk.CTkButton(parent, text=text, command=command, **kwargs)

        if tooltip:
            self.add_tooltip(button, tooltip)

        return button

    def create_info_label(self, parent, text: str, value: str = "",
                         font_size: int = 12, bold: bool = False) -> tuple:
        """
        Create a standardized info label pair (label + value).

        Args:
            parent: Parent widget
            text: Label text
            value: Value text
            font_size: Font size
            bold: Whether to make text bold

        Returns:
            Tuple of (label_widget, value_widget)
        """
        # Label
        label = ctk.CTkLabel(
            parent,
            text=f"{text}:",
            font=ctk.CTkFont(size=font_size, weight="bold" if bold else "normal")
        )
        label.pack(anchor="w", padx=10, pady=(5, 2))

        # Value
        weight = "bold" if bold else "normal"
        value_label = ctk.CTkLabel(
            parent,
            text=value,
            font=ctk.CTkFont(size=font_size, weight=weight)
        )
        value_label.pack(anchor="w", padx=20, pady=(0, 5))

        return label, value_label

    def handle_error(self, error: Exception, context: str = ""):
        """
        Handle errors in a standardized way.

        Args:
            error: The exception that occurred
            context: Context where the error occurred
        """
        error_msg = f"Error in {context}: {str(error)}" if context else f"Error: {str(error)}"
        print(error_msg)

        # In a real application, you might want to show a dialog
        # ctk.CTkMessagebox(title="Error", message=error_msg, icon="error")

    @abstractmethod
    def get_export_data(self) -> str:
        """
        Get data for export. Must be implemented by subclasses.

        Returns:
            String representation of component data
        """
        pass