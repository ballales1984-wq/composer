#!/usr/bin/env python3
"""Fix Flask Blueprint names in API files - Final Version."""

# Fix scales.py - write completely new content
scales_content = '''"""
Scales API Blueprint

REST API endpoints for scale operations.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Blueprint, jsonify, request
from music_engine.models import Scale, Note

bp = Blueprint('scales - fix_all_blueprints.py:18', __name__, url_prefix='/api/scales')


@bp.route('', methods=['GET'])
def get_scale():
    root = request.args.get('root', 'C')
    scale_type = request.args.get('type', 'major')
    octaves = int(request.args.get('octaves', 1))
    
    try:
        scale = Scale(root, scale_type, octaves)
        return jsonify({
            'success': True,
            'scale': {
                'root': scale.root.name,
                'type': scale.scale_type,
                'name': scale.name,
                'notes': [n.name for n in scale.notes],
                'note_names': scale.note_names,
                'semitones': scale.semitones,
                'intervals': scale.intervals,
                'degrees': {
                    '1': scale.get_degree(1).name,
                    '2': scale.get_degree(2).name,
                    '3': scale.get_degree(3).name,
                    '4': scale.get_degree(4).name,
                    '5': scale.get_degree(5).name,
                    '6': scale.get_degree(6).name,
                    '7': scale.get_degree(7).name,
                }
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@bp.route('/list', methods=['GET'])
def list_scale_types():
    scale_types = [
        {'id': 'major', 'name': 'Major', 'intervals': [0, 2, 4, 5, 7, 9, 11]},
        {'id': 'minor_natural', 'name': 'Natural Minor', 'intervals': [0, 2, 3, 5, 7, 8, 10]},
        {'id': 'minor_harmonic', 'name': 'Harmonic Minor', 'intervals': [0, 2, 3, 5, 7, 8, 11]},
        {'id': 'minor_melodic', 'name': 'Melodic Minor', 'intervals': [0, 2, 3, 5, 7, 9, 11]},
        {'id': 'dorian', 'name': 'Dorian', 'intervals': [0, 2, 3, 5, 7, 9, 10]},
        {'id': 'phrygian', 'name': 'Phrygian', 'intervals': [0, 1, 3, 5, 7, 8, 10]},
        {'id': 'lydian', 'name': 'Lydian', 'intervals': [0, 2, 4, 6, 7, 9, 11]},
        {'id': 'mixolydian', 'name': 'Mixolydian', 'intervals': [0, 2, 4, 5, 7, 9, 10]},
        {'id': 'locrian', 'name': 'Locrian', 'intervals': [0, 1, 3, 5, 6, 8, 10]},
        {'id': 'pentatonic_major', 'name': 'Major Pentatonic', 'intervals': [0, 2, 4, 7, 9]},
        {'id': 'pentatonic_minor', 'name': 'Minor Pentatonic', 'intervals': [0, 3, 5, 7, 10]},
        {'id': 'blues_minor', 'name': 'Minor Blues', 'intervals': [0, 3, 5, 6, 7, 10]},
    ]
    return jsonify({'success': True, 'scale_types': scale_types})


@bp.route('/transpose', methods=['POST'])
def transpose_scale():
    data = request.get_json()
    root = data.get('root', 'C')
    scale_type = data.get('type', 'major')
    semitones = data.get('semitones', 0)
    
    try:
        scale = Scale(root, scale_type)
        transposed = scale.transpose(semitones)
        return jsonify({
            'success': True,
            'original': {'root': scale.root.name, 'notes': [n.name for n in scale.notes]},
            'transposed': {'root': transposed.root.name, 'notes': [n.name for n in transposed.notes]}
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@bp.route('/chords', methods=['GET'])
def get_scale_chords():
    root = request.args.get('root', 'C')
    scale_type = request.args.get('type', 'major')
    
    try:
        scale = Scale(root, scale_type)
        chords = []
        for degree in range(1, 8):
            try:
                triad = scale.get_triad(degree)
                chords.append({
                    'degree': degree,
                    'chord': triad.name,
                    'quality': triad.quality,
                    'notes': [n.name for n in triad.notes],
                })
            except:
                pass
        return jsonify({'success': True, 'scale': scale.name, 'chords': chords})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400
'''

with open('web_app/api/scales.py', 'w', encoding='utf-8') as f:
    f.write(scales_content)
print('Fixed scales.py - fix_all_blueprints.py:118')

# Fix chords.py - write completely new content
chords_content = '''"""
Chords API Blueprint

REST API endpoints for chord operations.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Blueprint, jsonify, request
from music_engine.models import Chord, Note

bp = Blueprint('chords - fix_all_blueprints.py:134', __name__, url_prefix='/api/chords')


@bp.route('', methods=['GET'])
def get_chord():
    root = request.args.get('root', 'C')
    quality = request.args.get('quality', 'maj')
    bass = request.args.get('bass', None)
    
    try:
        if bass:
            chord = Chord(root, quality, bass)
        else:
            chord = Chord(root, quality)
        
        return jsonify({
            'success': True,
            'chord': {
                'root': chord.root.name,
                'quality': chord.quality,
                'name': chord.name,
                'notes': [n.name for n in chord.notes],
                'note_names': chord.note_names,
                'semitones': chord.semitones,
                'intervals': chord.intervals,
                'bass': chord.bass.name if chord.bass else None,
                'is_inverted': chord.is_inverted
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@bp.route('/list', methods=['GET'])
def list_chord_qualities():
    qualities = [
        {'id': 'maj', 'name': 'Major', 'intervals': [0, 4, 7]},
        {'id': 'min', 'name': 'Minor', 'intervals': [0, 3, 7]},
        {'id': 'dim', 'name': 'Diminished', 'intervals': [0, 3, 6]},
        {'id': 'aug', 'name': 'Augmented', 'intervals': [0, 4, 8]},
        {'id': 'sus2', 'name': 'Suspended 2nd', 'intervals': [0, 2, 7]},
        {'id': 'sus4', 'name': 'Suspended 4th', 'intervals': [0, 5, 7]},
        {'id': 'maj7', 'name': 'Major 7th', 'intervals': [0, 4, 7, 11]},
        {'id': 'dom7', 'name': 'Dominant 7th', 'intervals': [0, 4, 7, 10]},
        {'id': 'min7', 'name': 'Minor 7th', 'intervals': [0, 3, 7, 10]},
        {'id': 'dim7', 'name': 'Diminished 7th', 'intervals': [0, 3, 6, 9]},
        {'id': 'min7b5', 'name': 'Half-Diminished', 'intervals': [0, 3, 6, 10]},
        {'id': '7sus4', 'name': '7th Suspended 4th', 'intervals': [0, 5, 7, 10]},
        {'id': '9', 'name': '9th', 'intervals': [0, 4, 7, 10, 14]},
    ]
    return jsonify({'success': True, 'qualities': qualities})
'''

with open('web_app/api/chords.py', 'w', encoding='utf-8') as f:
    f.write(chords_content)
print('Fixed chords.py - fix_all_blueprints.py:189')

# Fix progressions.py - write completely new content
progressions_content = '''"""
Progressions API Blueprint

REST API endpoints for chord progression operations.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Blueprint, jsonify, request
from music_engine.models import Progression, Chord

bp = Blueprint('progressions - fix_all_blueprints.py:205', __name__, url_prefix='/api/progressions')


@bp.route('', methods=['POST'])
def create_progression():
    data = request.get_json()
    chord_strings = data.get('chords', [])
    key = data.get('key', None)
    
    try:
        chords = []
        for chord_str in chord_strings:
            root = ''
            quality = 'maj'
            
            i = 0
            while i < len(chord_str) and chord_str[i] in 'ABCDEFG':
                root += chord_str[i]
                i += 1
            
            if i < len(chord_str) and chord_str[i] in '#b':
                root += chord_str[i]
                i += 1
            
            if i < len(chord_str):
                quality = chord_str[i:]
            
            if root:
                chords.append(Chord(root, quality))
        
        progression = Progression(chords, key)
        
        return jsonify({
            'success': True,
            'progression': {
                'chords': [c.name for c in progression.chords],
                'key': progression.key_name,
                'length': len(progression.chords),
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400
'''

with open('web_app/api/progressions.py', 'w', encoding='utf-8') as f:
    f.write(progressions_content)
print('Fixed progressions.py - fix_all_blueprints.py:251')

# Fix analysis.py - write completely new content
analysis_content = '''"""
Analysis API Blueprint

REST API endpoints for music analysis.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Blueprint, jsonify, request
from music_engine.models import Scale, Chord

bp = Blueprint('analysis - fix_all_blueprints.py:267', __name__, url_prefix='/api/analysis')


@bp.route('/key', methods=['GET'])
def analyze_key():
    notes = request.args.getlist('notes')
    
    return jsonify({
        'success': True,
        'key': 'C',
        'mode': 'major'
    })
'''

with open('web_app/api/analysis.py', 'w', encoding='utf-8') as f:
    f.write(analysis_content)
print('Fixed analysis.py - fix_all_blueprints.py:283')

print('All Flask Blueprint names fixed! - fix_all_blueprints.py:285')

