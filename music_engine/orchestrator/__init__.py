"""
Orchestrator Module

This module coordinates the music theory engine components,
providing high-level interfaces for chord/scale suggestions,
progression expansion, and genre-specific rules.
"""

from .controller import InputController, OutputFormatter, Coordinator
from .solver import ScaleSolver, ChordSolver, ConflictResolver
from .expansion import ProgressionExpander, ContinuationGenerator, SubstitutionHandler
from .genre_rules import GenreDetector, JazzRules, PopRules, RockRules, BluesRules

__all__ = [
    'InputController',
    'OutputFormatter', 
    'Coordinator',
    'ScaleSolver',
    'ChordSolver',
    'ConflictResolver',
    'ProgressionExpander',
    'ContinuationGenerator',
    'SubstitutionHandler',
    'GenreDetector',
    'JazzRules',
    'PopRules',
    'RockRules',
    'BluesRules',
]

