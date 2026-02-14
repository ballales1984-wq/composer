"""Core music theory logic modules."""

# Lazy imports to avoid import issues when running as script
# from . import notes, scales, chords, arpeggios, progressions

__all__ = ['notes', 'scales', 'chords', 'arpeggios', 'progressions', 'intervals', 'harmony']

# Import new modules when available
try:
    from .intervals import Interval
    from .harmony import HarmonyEngine, analyze, create_harmony_engine
    __all__.extend(['Interval', 'HarmonyEngine', 'analyze', 'create_harmony_engine'])
except ImportError:
    pass
