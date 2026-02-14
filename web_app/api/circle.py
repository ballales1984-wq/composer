"""
Circle of Fifths API Blueprint
REST API endpoints for circle of fifths operations.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Blueprint, jsonify, request
from music_engine.models import Note, Chord, Scale

# Blueprint name
BLUEPRINT_NAME = 'circle'

bp = Blueprint('circle', __name__, url_prefix='/api/circle')


# Circle of Fifths data
# Major keys in order (clockwise): C, G, D, A, E, B, F#/Gb, Db, Ab, Eb, Bb, F
MAJOR_KEYS = [
    {'root': 'C', 'position': 0, 'fifths': 0, 'key_signature': 0, 'color': '#74c0fc'},
    {'root': 'G', 'position': 1, 'fifths': 7, 'key_signature': 1, 'color': '#69db7c'},
    {'root': 'D', 'position': 2, 'fifths': 14, 'key_signature': 2, 'color': '#ffd43b'},
    {'root': 'A', 'position': 3, 'fifths': 21, 'key_signature': 3, 'color': '#ff8787'},
    {'root': 'E', 'position': 4, 'fifths': 28, 'key_signature': 4, 'color': '#da77f2'},
    {'root': 'B', 'position': 5, 'fifths': 35, 'key_signature': 5, 'color': '#63e6be'},
    {'root': 'F#', 'position': 6, 'fifths': 42, 'key_signature': 6, 'color': '#4dabf7'},
    {'root': 'Gb', 'position': 7, 'fifths': -6, 'key_signature': -6, 'color': '#f783ac'},
    {'root': 'Db', 'position': 8, 'fifths': -12, 'key_signature': -5, 'color': '#f783ac'},
    {'root': 'Ab', 'position': 9, 'fifths': -18, 'key_signature': -4, 'color': '#a9e34b'},
    {'root': 'Eb', 'position': 10, 'fifths': -24, 'key_signature': -3, 'color': '#ffc078'},
    {'root': 'Bb', 'position': 11, 'fifths': -30, 'key_signature': -2, 'color': '#b197fc'},
    {'root': 'F', 'position': 12, 'fifths': -36, 'key_signature': -1, 'color': '#38d9a9'},
]

# Minor keys (relative minors - 3 semitones below their major)
MINOR_KEYS = [
    {'root': 'Am', 'relative_major': 'C', 'position': 0, 'color': '#e599f7'},
    {'root': 'Em', 'relative_major': 'G', 'position': 1, 'color': '#a5d8ff'},
    {'root': 'Bm', 'relative_major': 'D', 'position': 2, 'color': '#b2f2bb'},
    {'root': 'F#m', 'relative_major': 'A', 'position': 3, 'color': '#ffe066'},
    {'root': 'C#m', 'relative_major': 'E', 'position': 4, 'color': '#ffa8a8'},
    {'root': 'G#m', 'relative_major': 'B', 'position': 5, 'color': '#d0bfff'},
    {'root': 'D#m', 'relative_major': 'F#', 'position': 6, 'color': '#7be9ad'},
    {'root': 'A#m', 'relative_major': 'Gb', 'position': 7, 'color': '#4dabf7'},
    {'root': 'Fm', 'relative_major': 'Ab', 'position': 8, 'color': '#f783ac'},
    {'root': 'Cm', 'relative_major': 'Db', 'position': 9, 'color': '#a9e34b'},
    {'root': 'Gm', 'relative_major': 'Eb', 'position': 10, 'color': '#ffc078'},
    {'root': 'Dm', 'relative_major': 'F', 'position': 11, 'color': '#b197fc'},
]

# Common chord progressions by key
COMMON_PROGRESSIONS = {
    'major': [
        {'name': 'I-IV-V-I', 'chords': ['I', 'IV', 'V', 'I'], 'description': 'Basic progression'},
        {'name': 'I-V-vi-IV', 'chords': ['I', 'V', 'vi', 'IV'], 'description': 'Popular pop progression'},
        {'name': 'I-vi-IV-V', 'chords': ['I', 'vi', 'IV', 'V'], 'description': '50s progression'},
        {'name': 'ii-V-I', 'chords': ['ii', 'V', 'I'], 'description': 'Jazz turnaround'},
        {'name': 'I-IV-vi-V', 'chords': ['I', 'IV', 'vi', 'V'], 'description': 'Circle progression'},
    ],
    'minor': [
        {'name': 'i-iv-v-i', 'chords': ['i', 'iv', 'v', 'i'], 'description': 'Basic minor progression'},
        {'name': 'i-VI-III-VII', 'chords': ['i', 'VI', 'III', 'VII'], 'description': 'Natural minor progression'},
        {'name': 'i-iv-VII-III', 'chords': ['i', 'iv', 'VII', 'III'], 'description': 'Ascending minor'},
    ]
}


@bp.route('', methods=['GET'])
def get_circle_of_fifths():
    """Get the complete circle of fifths data."""
    try:
        return jsonify({
            'success': True,
            'major_keys': MAJOR_KEYS,
            'minor_keys': MINOR_KEYS,
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@bp.route('/key/<root>', methods=['GET'])
def get_key_info(root):
    """Get detailed information about a specific key."""
    try:
        root = root.title()  # Capitalize first letter
        
        # Check if it's a minor key
        is_minor = root.endswith('m')
        if is_minor:
            root_note = root[:-1]  # Remove 'm'
        else:
            root_note = root
            
        # Find in major or minor keys
        key_data = None
        if is_minor:
            for key in MINOR_KEYS:
                if key['root'].replace('m', '') == root_note:
                    key_data = key
                    break
        else:
            for key in MAJOR_KEYS:
                if key['root'] == root_note:
                    key_data = key
                    break
        
        if not key_data:
            return jsonify({'success': False, 'error': 'Key not found'}), 404
        
        # Get diatonic chords for this key
        scale_type = 'minor_natural' if is_minor else 'major'
        scale = Scale(root_note, scale_type)
        chords = []
        
        # Roman numeral mapping
        roman_numerals = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII']
        if is_minor:
            roman_numerals = ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii']
        
        for degree in range(1, 8):
            try:
                triad = scale.get_triad(degree)
                chords.append({
                    'degree': degree,
                    'roman': roman_numerals[degree - 1],
                    'chord': triad.name,
                    'quality': triad.quality,
                    'notes': [n.name for n in triad.notes],
                })
            except Exception as e:
                pass
        
        # Get relative key
        relative_key = None
        if not is_minor:
            # Major -> relative minor (3 semitones down)
            n = Note(root_note)
            relative_semitone = (n.semitone - 3) % 12
            relative_key = {
                'key': Note.from_semitone(relative_semitone).name + 'm',
                'type': 'minor'
            }
        else:
            # Minor -> relative major (3 semitones up)
            n = Note(root_note)
            relative_semitone = (n.semitone + 3) % 12
            relative_key = {
                'key': Note.from_semitone(relative_semitone).name,
                'type': 'major'
            }
        
        # Get common progressions
        progressions = COMMON_PROGRESSIONS['minor' if is_minor else 'major']
        
        return jsonify({
            'success': True,
            'key': {
                'root': root,
                'type': 'minor' if is_minor else 'major',
                'position': key_data.get('position'),
                'key_signature': key_data.get('key_signature', 0),
            },
            'relative_key': relative_key,
            'diatonic_chords': chords,
            'common_progressions': progressions,
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@bp.route('/relationships/<root>', methods=['GET'])
def get_key_relationships(root):
    """Get relationships for a key (dominant, subdominant, relative)."""
    try:
        root = root.title()
        is_minor = root.endswith('m')
        root_note = root[:-1] if is_minor else root
        
        n = Note(root_note)
        semitone = n.semitone
        
        if is_minor:
            # For minor keys
            relative_major = (semitone + 3) % 12  # Relative major is 3 semitones up
            dominant = (semitone + 7) % 12  # Dominant is 7 semitones up
            subdominant = (semitone + 5) % 12  # Subdominant is 5 semitones up
            
            return jsonify({
                'success': True,
                'key': root,
                'type': 'minor',
                'relationships': {
                    'relative_major': Note.from_semitone(relative_major).name,
                    'dominant': Note.from_semitone(dominant).name + 'm',
                    'subdominant': Note.from_semitone(subdominant).name + 'm',
                }
            })
        else:
            # For major keys
            relative_minor = (semitone - 3) % 12  # Relative minor is 3 semitones down
            dominant = (semitone + 7) % 12  # Dominant is 7 semitones up (perfect 5th)
            subdominant = (semitone + 5) % 12  # Subdominant is 5 semitones up (perfect 4th)
            
            return jsonify({
                'success': True,
                'key': root,
                'type': 'major',
                'relationships': {
                    'relative_minor': Note.from_semitone(relative_minor).name + 'm',
                    'dominant': Note.from_semitone(dominant).name,  # V chord
                    'subdominant': Note.from_semitone(subdominant).name,  # IV chord
                }
            })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@bp.route('/neighbors/<root>', methods=['GET'])
def get_neighbors(root):
    """Get neighboring keys on the circle of fifths."""
    try:
        root = root.title()
        is_minor = root.endswith('m')
        root_note = root[:-1] if is_minor else root
        
        keys = MINOR_KEYS if is_minor else MAJOR_KEYS
        
        # Find position
        position = None
        for i, key in enumerate(keys):
            key_root = key['root'].replace('m', '') if is_minor else key['root']
            if key_root == root_note:
                position = i
                break
        
        if position is None:
            return jsonify({'success': False, 'error': 'Key not found'}), 404
        
        # Get neighbors (1 step clockwise and counter-clockwise)
        prev_pos = (position - 1) % len(keys)
        next_pos = (position + 1) % len(keys)
        
        return jsonify({
            'success': True,
            'key': root,
            'neighbors': {
                'counter_clockwise': keys[prev_pos]['root'],  # Subdominant side
                'clockwise': keys[next_pos]['root'],  # Dominant side
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

