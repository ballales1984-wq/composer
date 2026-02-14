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
        {'id': 'whole_tone', 'name': 'Whole Tone', 'intervals': [0, 2, 4, 6, 8, 10]},
        {'id': 'chromatic', 'name': 'Chromatic', 'intervals': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]},
        {'id': 'diminished', 'name': 'Diminished', 'intervals': [0, 2, 3, 5, 6, 8, 9, 11]},
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

