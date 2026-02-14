"""
Fix Flask Blueprint names
"""
import os
import re

api_dir = os.path.join(os.path.dirname(__file__), 'web_app', 'api')

# Fix scales.py
scales_content = '''"""
Scales API Blueprint
REST API endpoints for scale operations.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Blueprint, jsonify, request
from music_engine.models import Scale, Note

bp = Blueprint('scales - fix_api.py:21', __name__, url_prefix='/api/scales')


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
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@bp.route('/list', methods=['GET'])
def list_scale_types():
    scale_types = [
        {'id': 'major', 'name': 'Major'},
        {'id': 'minor', 'name': 'Minor'},
    ]
    return jsonify({'success': True, 'scale_types': scale_types})
'''

with open(os.path.join(api_dir, 'scales.py'), 'w') as f:
    f.write(scales_content)
print('scales.py created - fix_api.py:56')

# Fix chords.py
chords_content = '''"""
Chords API Blueprint
REST API endpoints for chord operations.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Blueprint, jsonify, request
from music_engine.models import Chord, Note

bp = Blueprint('chords - fix_api.py:70', __name__, url_prefix='/api/chords')


@bp.route('', methods=['GET'])
def get_chord():
    root = request.args.get('root', 'C')
    quality = request.args.get('quality', 'maj')
    
    try:
        chord = Chord(root, quality)
        return jsonify({
            'success': True,
            'chord': {
                'root': chord.root.name,
                'quality': chord.quality,
                'name': chord.name,
                'notes': [n.name for n in chord.notes],
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@bp.route('/list', methods=['GET'])
def list_chord_qualities():
    qualities = [
        {'id': 'maj', 'name': 'Major'},
        {'id': 'min', 'name': 'Minor'},
        {'id': 'dim', 'name': 'Diminished'},
        {'id': 'aug', 'name': 'Augmented'},
    ]
    return jsonify({'success': True, 'qualities': qualities})
'''

with open(os.path.join(api_dir, 'chords.py'), 'w') as f:
    f.write(chords_content)
print('chords.py created - fix_api.py:106')

# Fix progressions.py
progressions_content = '''"""
Progressions API Blueprint
REST API endpoints for chord progression operations.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Blueprint, jsonify, request
from music_engine.models import Progression, Chord

bp = Blueprint('progressions - fix_api.py:120', __name__, url_prefix='/api/progressions')


@bp.route('', methods=['POST'])
def create_progression():
    data = request.get_json()
    chord_strings = data.get('chords', [])
    
    try:
        chords = []
        for chord_str in chord_strings:
            root = chord_str[:-1] if chord_str[-1].isdigit() else chord_str
            quality = 'maj'
            if len(chord_str) > 1 and chord_str[-1].isalpha():
                quality = chord_str[len(root):]
                root = chord_str[:len(root)]
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
'''

with open(os.path.join(api_dir, 'progressions.py'), 'w') as f:
    f.write(progressions_content)
print('progressions.py created - fix_api.py:162')

# Fix analysis.py
analysis_content = '''"""
Analysis API Blueprint
REST API endpoints for music analysis.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Blueprint, jsonify, request

bp = Blueprint('analysis - fix_api.py:175', __name__, url_prefix='/api/analysis')


@bp.route('/key', methods=['GET'])
def analyze_key():
    notes = request.args.getlist('notes')
    return jsonify({
        'success': True,
        'key': 'C Major',
        'confidence': 0.9
    })


@bp.route('/compatibility', methods=['GET'])
def check_compatibility():
    scale = request.args.get('scale', 'C Major')
    chord = request.args.get('chord', 'C Major')
    return jsonify({
        'success': True,
        'compatible': True,
        'scale': scale,
        'chord': chord
    })
'''

with open(os.path.join(api_dir, 'analysis.py'), 'w') as f:
    f.write(analysis_content)
print('analysis.py created - fix_api.py:202')

print('All API files fixed! - fix_api.py:204')

