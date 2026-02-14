"""
Chords API Blueprint
REST API endpoints for chord operations.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Blueprint, jsonify, request
from music_engine.models import Chord, Note

bp = Blueprint('chords', __name__, url_prefix='/api/chords')


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
                'intervals': chord.intervals,
                'semitones': chord.semitones,
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


@bp.route('/inversions', methods=['GET'])
def get_inversions():
    root = request.args.get('root', 'C')
    quality = request.args.get('quality', 'maj')
    
    try:
        chord = Chord(root, quality)
        inversions = chord.get_all_inversions()
        
        inversions_data = []
        for i, inv in enumerate(inversions):
            inversions_data.append({
                'position': i,
                'bass': inv.notes[0].name if inv.notes else root,
                'notes': [n.name for n in inv.notes],
            })
        
        return jsonify({
            'success': True,
            'inversions': inversions_data
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@bp.route('/voicing', methods=['GET'])
def get_voicing():
    root = request.args.get('root', 'C')
    quality = request.args.get('quality', 'maj')
    octave = int(request.args.get('octave', 4))
    
    try:
        chord = Chord(root, quality)
        voicing = chord.get_voicing(octave=octave, spread=True)
        
        voicing_data = []
        for note, note_octave in voicing:
            voicing_data.append({
                'note': note.name,
                'octave': note_octave,
            })
        
        return jsonify({
            'success': True,
            'voicing': voicing_data
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400
