"""
Scales API Blueprint
REST API endpoints for scale operations.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Blueprint, jsonify, request
from music_engine.models import Scale, Note

# Blueprint name
BLUEPRINT_NAME = 'scales'

bp = Blueprint('scales', __name__, url_prefix='/api/scales')



@bp.route('', methods=['GET'])
def get_scale():
    root = request.args.get('root', 'C')
    scale_type = request.args.get('type', 'major')
    octaves = int(request.args.get('octaves', 1))
    
    try:
        scale = Scale(root, scale_type, octaves)

        # Generate degrees data
        degrees = {}
        for i, note in enumerate(scale.notes[:7]):
            degrees[str(i + 1)] = note.name
        
        # Format intervals as strings
        intervals = [str(i) for i in scale.intervals]
        
        return jsonify({
            'success': True,
            'scale': {
                'root': scale.root.name,
                'type': scale.scale_type,
                'name': scale.name,
                'notes': [n.name for n in scale.notes],
                'intervals': intervals,
                'degrees': degrees,
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@bp.route('/list', methods=['GET'])
def list_scale_types():
    scale_types = [
        {'id': 'major', 'name': 'Major'},
        {'id': 'minor_natural', 'name': 'Natural Minor'},
        {'id': 'minor_harmonic', 'name': 'Harmonic Minor'},
        {'id': 'minor_melodic', 'name': 'Melodic Minor'},
        {'id': 'dorian', 'name': 'Dorian'},
        {'id': 'phrygian', 'name': 'Phrygian'},
        {'id': 'lydian', 'name': 'Lydian'},
        {'id': 'mixolydian', 'name': 'Mixolydian'},
        {'id': 'locrian', 'name': 'Locrian'},
        {'id': 'pentatonic_major', 'name': 'Major Pentatonic'},
        {'id': 'pentatonic_minor', 'name': 'Minor Pentatonic'},
        {'id': 'blues_major', 'name': 'Major Blues'},
        {'id': 'blues_minor', 'name': 'Minor Blues'},
        {'id': 'whole_tone', 'name': 'Whole Tone'},
        {'id': 'chromatic', 'name': 'Chromatic'},
        {'id': 'diminished', 'name': 'Diminished'},
    ]
    return jsonify({'success': True, 'scale_types': scale_types})

