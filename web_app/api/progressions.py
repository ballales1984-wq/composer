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


@bp.route('', methods=['POST'])
def create_progression():
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

