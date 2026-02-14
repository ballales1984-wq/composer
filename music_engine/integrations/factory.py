"""
Integration factory for music21 and mingus adapters.

This module provides a unified factory interface for accessing conversion
functionalities between the internal music engine models and external
music theory libraries.
"""

from typing import Optional, Union, List, TYPE_CHECKING


class IntegrationFactory:
    """
    Factory class for creating converters to external music theory libraries.
    
    This provides a unified interface for:
    - music21: MIDI, notation, harmonic analysis
    - mingus: Roman numeral analysis, diatonic chord generation
    
    Example usage:
        >>> from music_engine.integrations import IntegrationFactory
        >>> 
        >>> # Get a music21 converter
        >>> m21_converter = IntegrationFactory.get_music21_converter()
        >>> m21_note = m21_converter.note_to_music21(note)
        >>> 
        >>> # Get a mingus converter
        >>> mingus_converter = IntegrationFactory.get_mingus_converter()
        >>> roman_numerals = mingus_converter.chords_to_roman_numerals(chords, 'C')
    """
    
    _music21_converter = None
    _mingus_converter = None
    
    @classmethod
    def get_music21_converter(cls):
        """
        Get the music21 converter instance.
        
        Returns:
            Music21Converter: Converter for music21 integration
            
        Raises:
            ImportError: If music21 is not installed
        """
        if cls._music21_converter is None:
            from .music21_adapter import Music21Converter
            cls._music21_converter = Music21Converter()
        return cls._music21_converter
    
    @classmethod
    def get_mingus_converter(cls):
        """
        Get the mingus converter instance.
        
        Returns:
            MingusConverter: Converter for mingus integration
            
        Raises:
            ImportError: If mingus is not installed
        """
        if cls._mingus_converter is None:
            from .mingus_adapter import MingusConverter
            cls._mingus_converter = MingusConverter()
        return cls._mingus_converter
    
    @classmethod
    def convert(cls, library: str, data, conversion_type: str = 'to'):
        """
        Convert data to or from an external library.
        
        Args:
            library: Library name ('music21' or 'mingus')
            data: Data to convert
            conversion_type: 'to' (internal -> library) or 'from' (library -> internal)
            
        Returns:
            Converted data
            
        Raises:
            ValueError: If library is not supported
        """
        if library.lower() == 'music21':
            converter = cls.get_music21_converter()
            if conversion_type == 'to':
                return cls._convert_to_music21(converter, data)
            else:
                return cls._convert_from_music21(converter, data)
        
        elif library.lower() == 'mingus':
            converter = cls.get_mingus_converter()
            if conversion_type == 'to':
                return cls._convert_to_mingus(converter, data)
            else:
                return cls._convert_from_mingus(converter, data)
        
        else:
            raise ValueError(f"Unsupported library: {library}. Use 'music21' or 'mingus'.")
    
    @classmethod
    def _convert_to_music21(cls, converter, data):
        """Convert internal model to music21 object."""
        from music_engine.models import Note, Chord, Scale, Progression
        
        if isinstance(data, Note):
            return converter.note_to_music21(data)
        elif isinstance(data, Chord):
            return converter.chord_to_music21(data)
        elif isinstance(data, Scale):
            return converter.scale_to_music21(data)
        elif isinstance(data, Progression):
            return converter.progression_to_music21_stream(data)
        else:
            raise ValueError(f"Unsupported type: {type(data)}")
    
    @classmethod
    def _convert_from_music21(cls, converter, data):
        """Convert music21 object to internal model."""
        import music21
        
        if isinstance(data, music21.note.Note):
            return converter.music21_to_note(data)
        elif isinstance(data, music21.chord.Chord):
            return converter.music21_to_chord(data)
        elif isinstance(data, music21.stream.Stream):
            return converter.stream_to_progression(data)
        else:
            raise ValueError(f"Unsupported type: {type(data)}")
    
    @classmethod
    def _convert_to_mingus(cls, converter, data):
        """Convert internal model to mingus object."""
        from music_engine.models import Note, Chord, Progression
        
        if isinstance(data, Note):
            return converter.note_to_mingus(data)
        elif isinstance(data, Chord):
            return converter.chord_to_mingus(data)
        elif isinstance(data, Progression):
            return converter.progression_to_mingus(data)
        else:
            raise ValueError(f"Unsupported type: {type(data)}")
    
    @classmethod
    def _convert_from_mingus(cls, converter, data):
        """Convert mingus object to internal model."""
        import mingus
        
        if isinstance(data, mingus.containers.Note):
            return converter.mingus_to_note(data)
        elif isinstance(data, mingus.containers.Chord):
            return converter.mingus_to_chord(data)
        elif isinstance(data, mingus.containers.Progressions):
            return converter.mingus_to_progression(data)
        else:
            raise ValueError(f"Unsupported type: {type(data)}")
    
    @classmethod
    def is_library_available(cls, library: str) -> bool:
        """
        Check if a library is available (installed).
        
        Args:
            library: Library name ('music21' or 'mingus')
            
        Returns:
            bool: True if library is available
        """
        try:
            if library.lower() == 'music21':
                import music21
                return True
            elif library.lower() == 'mingus':
                import mingus
                return True
        except ImportError:
            pass
        return False
    
    @classmethod
    def get_available_libraries(cls) -> List[str]:
        """
        Get list of available integration libraries.
        
        Returns:
            List of available library names
        """
        available = []
        
        if cls.is_library_available('music21'):
            available.append('music21')
        if cls.is_library_available('mingus'):
            available.append('mingus')
        
        return available
    
    @classmethod
    def reset(cls):
        """Reset converter instances (useful for testing)."""
        cls._music21_converter = None
        cls._mingus_converter = None


# Convenience functions
def get_music21_converter():
    """Get music21 converter instance."""
    return IntegrationFactory.get_music21_converter()


def get_mingus_converter():
    """Get mingus converter instance."""
    return IntegrationFactory.get_mingus_converter()


def convert(library: str, data, conversion_type: str = 'to'):
    """Convert data to or from a library."""
    return IntegrationFactory.convert(library, data, conversion_type)


def is_library_available(library: str) -> bool:
    """Check if a library is available."""
    return IntegrationFactory.is_library_available(library)


def get_available_libraries() -> List[str]:
    """Get list of available libraries."""
    return IntegrationFactory.get_available_libraries()

