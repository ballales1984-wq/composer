"""
Analysis API Blueprint
REST API endpoints for music analysis.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Blueprint, jsonify, request

bp = Blueprint('analysis', __name__, url_prefix='/api/analysis')


@bp.route('/libraries', methods=['GET'])
def get_libraries():
    """Check available music libraries."""
    libraries = {
        'music21': False,
        'mingus': False
    }
    
    try:
        import music21
        libraries['music21'] = True
    except ImportError:
        pass
    
    try:
        import mingus
        libraries['mingus'] = True
    except ImportError:
        pass
    
    return jsonify(libraries)


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

