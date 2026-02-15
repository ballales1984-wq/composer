"""Progressions API Blueprint
REST API endpoints for chord progression operations.
"""
import sys
import os
import re
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Blueprint, jsonify, request
from music_engine.models import Progression, Chord

bp = Blueprint('progressions', __name__, url_prefix='/api/progressions')


@bp.route('', methods=['GET', 'POST'])
def handle_progression():
    """Handle GET (list progressions) and POST (create progression) requests."""
    if request.method == 'GET':
        # Return list of available progressions
        progressions = [
            {'id': 'i-iv-v-i', 'name': 'I-IV-V-I', 'chords': ['C', 'F', 'G', 'C']},
            {'id': 'i-vi-iv-v', 'name': 'I-VI-IV-V', 'chords': ['C', 'Am', 'F', 'G']},
            {'id': 'ii-v-i', 'name': 'ii-V-I', 'chords': ['Dm', 'G', 'C']},
            {'id': 'i-iv-vi-v', 'name': 'I-IV-vi-V', 'chords': ['C', 'F', 'Am', 'G']},
        ]
        return jsonify({'success': True, 'progressions': progressions})
    
    # POST - create progression
    data = request.get_json()
    chord_strings = data.get('chords', [])
    
    try:
        chords = []
        for chord_str in chord_strings:
            # Parse chord string like "Cmaj7", "Cmin", "F#m", "Bb"
            # Format: root (letter + optional # or b) + quality
            match = re.match(r'^([A-G][#b]?)(.*)$', chord_str)
            if match:
                root = match.group(1)
                quality = match.group(2) if match.group(2) else 'maj'
                # Normalize common quality names
                if quality == 'm':
                    quality = 'min'
                elif quality in ['7', '9', '11', '13']:
                    quality = f'dom{quality}'
            else:
                root = chord_str
                quality = 'maj'
            chords.append(Chord(root, quality))
        
        progression = Progression(chords)
        return jsonify({
            'success': True,
            'progression': {
                'chords': [c.name for c in progression.chords],
                'key': progression.key_name,
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@bp.route('/list', methods=['GET'])
def list_progressions():
    progressions = [
        {'id': 'i-iv-v-i', 'name': 'I-IV-V-I'},
        {'id': 'i-vi-iv-v', 'name': 'I-VI-IV-V'},
        {'id': 'ii-v-i', 'name': 'ii-V-I'},
    ]
    return jsonify({'success': True, 'progressions': progressions})


@bp.route('/analyze', methods=['GET'])
def analyze_progression():
    """
    Analyze a chord progression.
    
    Query parameters:
        chords: List of chord strings (can be repeated for multiple)
        key: Optional key for analysis (e.g., 'C', 'Am')
        
    Returns:
        JSON with analysis results including key, notes, complexity
    """
    chord_strings = request.args.getlist('chords')
    key = request.args.get('key', None)
    
    if not chord_strings:
        return jsonify({
            'success': False,
            'error': 'Please provide at least one chord'
        }), 400
    
    try:
        # Parse chords
        chords = _parse_chord_list(chord_strings)
        
        if not chords:
            return jsonify({
                'success': False,
                'error': 'Could not parse any valid chords'
            }), 400
        
        # Create progression
        progression = Progression(chords, key=key)
        
        # Build analysis result
        # Get key name without octave for cleaner display
        key_name = progression.key_name
        if key_name and key_name.endswith(tuple(str(i) for i in range(10))):
            # Remove trailing numbers (octaves)
            key_name = ''.join(c for c in key_name if not c.isdigit())
        
        # Get clean chord names (without "Major"/"Minor" suffix)
        clean_chord_names = []
        for c in progression.chords:
            name = c.name
            # Remove "Major" and "Minor" suffixes for cleaner display
            if name.endswith('Major'):
                name = name[:-5]
            elif name.endswith('Minor'):
                name = name[:-5]
            clean_chord_names.append(name)
        
        analysis = {
            'key': key_name if key_name else key or 'Unknown',
            'chords': clean_chord_names,
            'all_notes': sorted(list(progression.all_note_names)),
            'complexity': progression.analysis.get('complexity', 'simple'),
            'num_chords': len(progression.chords),
        }
        
        # Add detected key if different from provided
        if progression.key and progression.key.name:
            detected = progression.key.name
            if detected.endswith(tuple(str(i) for i in range(10))):
                detected = ''.join(c for c in detected if not c.isdigit())
            analysis['detected_key'] = detected
        
        return jsonify({
            'success': True,
            'analysis': analysis
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@bp.route('/roman', methods=['GET'])
def get_roman_numerals():
    """
    Convert chords to Roman numeral notation.
    
    Query parameters:
        key: The key for conversion (e.g., 'C', 'Am')
        chords: List of chord strings to convert
        
    Returns:
        JSON with Roman numeral notation
    """
    key = request.args.get('key', 'C')
    chord_strings = request.args.getlist('chords')
    
    if not chord_strings:
        return jsonify({
            'success': False,
            'error': 'Please provide at least one chord'
        }), 400
    
    try:
        # Parse chords
        chords = _parse_chord_list(chord_strings)
        
        if not chords:
            return jsonify({
                'success': False,
                'error': 'Could not parse any valid chords'
            }), 400
        
        # Create progression in the given key
        progression = Progression(chords, key=key)
        
        # Get Roman numerals
        roman_numerals = progression.to_roman_numerals()
        
        # Get clean chord names (without "Major"/"Minor" suffix)
        clean_chord_names = []
        for c in progression.chords:
            name = c.name
            if name.endswith('Major'):
                name = name[:-5]
            elif name.endswith('Minor'):
                name = name[:-5]
            clean_chord_names.append(name)
        
        return jsonify({
            'success': True,
            'key': key,
            'chords': clean_chord_names,
            'roman_numerals': roman_numerals
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


def _parse_chord_list(chord_strings):
    """Parse a list of chord strings into Chord objects."""
    chords = []
    for chord_str in chord_strings:
        if not chord_str or not chord_str.strip():
            continue
            
        try:
            # Try to parse using Chord constructor
            # Handle common formats: C, Cmaj7, Cm, Cmin, C7, etc.
            chord_str = chord_str.strip()
            
            # Use regex to extract root and quality
            match = re.match(r'^([A-G][#b]?)(.*)$', chord_str)
            if match:
                root = match.group(1)
                quality = match.group(2) if match.group(2) else 'maj'
                
                # Normalize quality names
                quality_map = {
                    'maj7': 'maj7',
                    'maj': 'maj',
                    'm': 'min',
                    'min': 'min',
                    'm7': 'min7',
                    'min7': 'min7',
                    'dom7': 'dom7',
                    '7': 'dom7',
                    'dim': 'dim',
                    'dim7': 'dim7',
                    'aug': 'aug',
                    'sus2': 'sus2',
                    'sus4': 'sus4',
                    '9': 'dom9',
                    '11': 'dom11',
                    '13': 'dom13',
                }
                
                quality = quality_map.get(quality, quality)
                if quality == 'maj' and root + 'maj' == chord_str:
                    quality = 'maj7'
                    
                chord = Chord(root, quality)
                chords.append(chord)
            else:
                # Try direct construction
                chord = Chord(chord_str)
                chords.append(chord)
        except Exception as e:
            # Skip invalid chords but continue with valid ones
            continue
    
    return chords

