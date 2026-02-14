"""
Orchestrator API Blueprint

API endpoints for the orchestrator module.
Provides suggestions, expansions, and genre-specific rules.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from flask import Blueprint, jsonify, request
from music_engine.orchestrator import (
    Coordinator, InputController, OutputFormatter,
    ScaleSolver, ChordSolver, ConflictResolver,
    ProgressionExpander, ContinuationGenerator, SubstitutionHandler,
    GenreDetector, JazzRules, PopRules, RockRules, BluesRules
)
from music_engine.models import Chord, Scale, Progression

# Blueprint name
BLUEPRINT_NAME = 'orchestrator'

bp = Blueprint('orchestrator', __name__, url_prefix='/api/orchestrator')


@bp.route('/suggest', methods=['POST'])
def suggest():
    """
    Get suggestions based on input and context.
    
    Request body:
        input: Chord, scale, or progression string
        genre: Optional genre (jazz, pop, rock, blues)
        key: Optional key
        
    Returns:
        JSON with suggestions
    """
    data = request.get_json() or {}
    
    input_str = data.get('input', '')
    genre = data.get('genre', 'jazz')
    key = data.get('key', 'C')
    
    if not input_str:
        return jsonify({
            'success': False,
            'error': 'Please provide an input parameter'
        }), 400
    
    try:
        coordinator = Coordinator()
        result = coordinator.process(input_str, {'genre': genre, 'key': key})
        
        return jsonify({
            'success': True,
            'result': result,
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@bp.route('/expand', methods=['POST'])
def expand():
    """
    Expand a short progression.
    
    Request body:
        chords: List of chord strings
        target_length: Target length for expansion
        
    Returns:
        JSON with expanded progressions
    """
    data = request.get_json() or {}
    
    chord_strings = data.get('chords', [])
    target_length = data.get('target_length', 8)
    
    if not chord_strings:
        return jsonify({
            'success': False,
            'error': 'Please provide chords to expand'
        }), 400
    
    try:
        # Parse chords
        chords = []
        for cs in chord_strings:
            root = cs.replace('maj7', '').replace('min7', 'm').replace('dom7', '7').replace('m7', 'm').replace('7', '').replace('maj', '').replace('min', 'm').replace('m', '')[:1]
            quality = cs[len(root):] or 'maj'
            
            # Simplify quality
            if quality == 'm':
                quality = 'min'
            
            try:
                chord = Chord(root, quality)
                chords.append(chord)
            except:
                pass
        
        if len(chords) < 2:
            return jsonify({
                'success': False,
                'error': 'Need at least 2 valid chords'
            }), 400
        
        # Expand
        from music_engine.core.harmony import HarmonyEngine
        expander = ProgressionExpander(HarmonyEngine())
        expansions = expander.expand(chords, target_length)
        
        return jsonify({
            'success': True,
            'original': chord_strings,
            'expansions': expansions,
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@bp.route('/next-chords', methods=['GET'])
def next_chords():
    """
    Get suggested next chords.
    
    Query parameters:
        chord: Current chord
        genre: Optional genre
        
    Returns:
        JSON with next chord suggestions
    """
    chord_str = request.args.get('chord', 'Cmaj7')
    genre = request.args.get('genre', 'jazz')
    
    try:
        # Parse chord
        root = chord_str.replace('maj7', '').replace('min7', 'm').replace('dom7', '7').replace('m7', 'm').replace('7', '').replace('maj', '').replace('min', 'm').replace('m', '')[:1]
        quality = chord_str[len(root):] or 'maj'
        
        chord = Chord(root, quality)
        
        # Get suggestions
        from music_engine.core.harmony import HarmonyEngine
        harmony_engine = HarmonyEngine()
        solver = ChordSolver(harmony_engine)
        
        next_chords = solver.suggest_next_chords(chord)
        
        # Apply genre filter
        genre_rules = get_genre_rules(genre)
        filtered = genre_rules.filter_chords(next_chords)
        
        return jsonify({
            'success': True,
            'current_chord': chord_str,
            'suggestions': filtered[:10],
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@bp.route('/compatible-scales', methods=['GET'])
def compatible_scales():
    """
    Get scales compatible with a chord.
    
    Query parameters:
        chord: Chord string
        genre: Optional genre
        
    Returns:
        JSON with compatible scales
    """
    chord_str = request.args.get('chord', 'Cmaj7')
    genre = request.args.get('genre', 'jazz')
    
    try:
        # Parse chord
        root = chord_str.replace('maj7', '').replace('min7', 'm').replace('dom7', '7').replace('m7', 'm').replace('7', '').replace('maj', '').replace('min', 'm').replace('m', '')[:1]
        quality = chord_str[len(root):] or 'maj'
        
        chord = Chord(root, quality)
        
        # Get scales
        from music_engine.core.harmony import HarmonyEngine
        harmony_engine = HarmonyEngine()
        compatible = harmony_engine.find_compatible_scales(chord)
        
        # Apply genre filter
        genre_rules = get_genre_rules(genre)
        
        scales = []
        for scale_info in compatible.get('all_scales', []):
            scale = scale_info.get('scale')
            if scale:
                scales.append({
                    'name': scale.name,
                    'notes': scale.note_names,
                    'type': scale.scale_type,
                    'score': scale_info.get('compatibility', {}).get('score', 0),
                })
        
        filtered = genre_rules.filter_scales(scales)
        
        return jsonify({
            'success': True,
            'chord': chord_str,
            'scales': filtered[:10],
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@bp.route('/genre/detect', methods=['POST'])
def detect_genre():
    """
    Detect genre from input or progression.
    
    Request body:
        input: Input string or progression
        
    Returns:
        JSON with detected genre
    """
    data = request.get_json() or {}
    input_str = data.get('input', '')
    
    if not input_str:
        return jsonify({
            'success': False,
            'error': 'Please provide input'
        }), 400
    
    try:
        detector = GenreDetector()
        genre = detector.detect_from_input(input_str)
        
        return jsonify({
            'success': True,
            'genre': genre,
            'confidence': 0.8,
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@bp.route('/genre/progressions', methods=['GET'])
def genre_progressions():
    """
    Get common progressions for a genre.
    
    Query parameters:
        genre: Genre name
        
    Returns:
        JSON with common progressions
    """
    genre = request.args.get('genre', 'jazz')
    
    try:
        genre_rules = get_genre_rules(genre)
        
        return jsonify({
            'success': True,
            'genre': genre,
            'progressions': genre_rules.common_progressions,
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@bp.route('/substitute/tritone', methods=['GET'])
def tritone_substitute():
    """
    Get tritone substitute for a dominant chord.
    
    Query parameters:
        chord: Dominant 7th chord
        
    Returns:
        JSON with substitute chord
    """
    chord_str = request.args.get('chord', 'G7')
    
    try:
        # Parse chord
        root = chord_str.replace('7', '')[:1]
        
        chord = Chord(root, 'dom7')
        
        from music_engine.core.harmony import HarmonyEngine
        handler = SubstitutionHandler(HarmonyEngine())
        
        substitute = handler.get_tritone_substitute(chord)
        
        if substitute:
            return jsonify({
                'success': True,
                'original': chord_str,
                'substitute': substitute.name,
                'notes': substitute.note_names,
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Not a dominant 7th chord'
            }), 400
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@bp.route('/continuation', methods=['POST'])
def get_continuation():
    """
    Get continuation suggestions for a progression.
    
    Request body:
        chords: List of chord strings
        num_chords: Number of continuation chords
        
    Returns:
        JSON with continuation options
    """
    data = request.get_json() or {}
    
    chord_strings = data.get('chords', [])
    num_chords = data.get('num_chords', 4)
    
    if not chord_strings:
        return jsonify({
            'success': False,
            'error': 'Please provide chords'
        }), 400
    
    try:
        # Parse chords
        chords = []
        for cs in chord_strings:
            root = cs.replace('maj7', '').replace('min7', 'm').replace('dom7', '7').replace('m7', 'm').replace('7', '').replace('maj', '').replace('min', 'm').replace('m', '')[:1]
            quality = cs[len(root):] or 'maj'
            
            if quality == 'm':
                quality = 'min'
            
            try:
                chord = Chord(root, quality)
                chords.append(chord)
            except:
                pass
        
        # Get continuations
        from music_engine.core.harmony import HarmonyEngine
        generator = ContinuationGenerator(HarmonyEngine())
        continuations = generator.generate_continuations(chords, num_chords)
        
        return jsonify({
            'success': True,
            'original': chord_strings,
            'continuations': continuations[:5],
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# Helper functions
def get_genre_rules(genre: str):
    """Get genre rules for a specific genre."""
    rules_map = {
        'jazz': JazzRules,
        'pop': PopRules,
        'rock': RockRules,
        'blues': BluesRules,
    }
    
    return rules_map.get(genre, JazzRules)()

