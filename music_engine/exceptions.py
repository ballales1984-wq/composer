"""
Custom exceptions for the Music Theory Engine.

This module defines custom exception classes for better error handling
and more informative error messages throughout the package.
"""


class MusicEngineError(Exception):
    """Base exception for all Music Theory Engine errors."""
    
    def __init__(self, message: str, details: dict = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}


class InvalidNoteError(MusicEngineError):
    """Raised when an invalid note is provided."""
    pass


class InvalidChordError(MusicEngineError):
    """Raised when an invalid chord is provided."""
    pass


class InvalidScaleError(MusicEngineError):
    """Raised when an invalid scale is provided."""
    pass


class InvalidProgressionError(MusicEngineError):
    """Raised when an invalid chord progression is provided."""
    pass


class InvalidIntervalError(MusicEngineError):
    """Raised when an invalid interval is provided."""
    pass


class UnsupportedTuningError(MusicEngineError):
    """Raised when an unsupported guitar tuning is requested."""
    pass


class InvalidQualityError(MusicEngineError):
    """Raised when an invalid chord/scale quality is provided."""
    pass


class ValidationError(MusicEngineError):
    """Raised when input validation fails."""
    pass


class IntegrationError(MusicEngineError):
    """Raised when an external integration (music21, mingus) fails."""
    pass


class ConfigurationError(MusicEngineError):
    """Raised when there's a configuration issue."""
    pass

