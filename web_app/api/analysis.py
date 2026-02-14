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
    """
    Analyze the key of a sequence of notes.
    
    Query params:
        notes: List of note names (e.g., ?notes=C&notes=E&notes=G)
    
    Returns:
        JSON with key, mode, and confidence score
    """
    notes = request.args.getlist('notes')
    
    if not notes:
        return jsonify({
            'success': False,
            'error': 'No notes provided. Use ?notes=C&notes=E&notes=G'
        }), 400
    
    try:
        # Use music21 for key detection
        from music21 import stream, note as m21note, analysis
        
        # Create a stream from the input notes
        s = stream.Stream()
        for note_name in notes:
            try:
                n = m21note.Note(note_name)
                s.append(n)
            except Exception:
                pass  # Skip invalid notes
        
        if len(s) == 0:
            return jsonify({
                'success': False,
                'error': 'No valid notes found'
            }), 400
        
        # Analyze key
        key = s.analyze('key')
        
        return jsonify({
            'success': True,
            'key': key.tonic.name,
            'mode': key.mode,
            'confidence': round(key.correlationCoefficient, 2) if hasattr(key, 'correlationCoefficient') else 0.9,
            ' альтернативні': [
                {'key': alt.tonic.name, 'mode': alt.mode, 'score': round(alt.correlationCoefficient, 2)}
                for alt in key.alternateInterpretations[:3]
            ] if hasattr(key, 'alternateInterpretations') else []
        })
        
    except ImportError:
        return jsonify({
            'success': False,
            'error': 'music21 not installed'
        }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@bp.route('/compatibility', methods=['GET'])
def check_compatibility():
    """
    Check if a chord is compatible with a scale.
    
    Query params:
        scale: Scale name (e.g., "C Major")
        chord: Chord name (e.g., "C Major")
    
    Returns:
        JSON with compatibility status
    """
    scale_name = request.args.get('scale', 'C Major')
    chord_name = request.args.get('chord', 'C Major')
    
    try:
        from music_engine.models import Scale, Chord
        from music_engine.integrations import IntegrationFactory
        
        # Parse scale
        scale_parts = scale_name.split()
        scale_root = scale_parts[0] if scale_parts else 'C'
        scale_type = ' '.join(scale_parts[1:]) if len(scale_parts) > 1 else 'major'
        
        # Parse chord  
        chord_parts = chord_name.split()
        chord_root = chord_parts[0] if chord_parts else 'C'
        chord_quality = ' '.join(chord_parts[1:]) if len(chord_parts) > 1 else 'maj'
        
        # Get scale notes
        s = Scale(scale_root, scale_type)
        scale_notes = set(n.name for n in s.notes)
        
        # Get chord notes
        c = Chord(chord_root, chord_quality)
        chord_notes = set(n.name for n in c.notes)
        
        # Check compatibility
        compatible = chord_notes.issubset(scale_notes)
        
        # Get degree if compatible
        degree = None
        if compatible:
            try:
                degree_index = scale_notes.index(chord_root)
                degree = s.degrees[degree_index] if hasattr(s, 'degrees') else degree_index + 1
            except:
                pass
        
        return jsonify({
            'success': True,
            'compatible': compatible,
            'scale': scale_name,
            'chord': chord_name,
            'scale_notes': list(scale_notes),
            'chord_notes': list(chord_notes),
            'degree': degree
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@bp.route('/progressions', methods=['GET'])
def get_progressions():
    """
    Get common chord progressions in a given key.
    
    Query params:
        key: Key name (e.g., "C Major")
        type: Progression type (common, jazz, blues)
    
    Returns:
        JSON with common progressions
    """
    key_name = request.args.get('key', 'C Major')
    prog_type = request.args.get('type', 'common')
    
    # Common progressions
    progressions = {
        'common': [
            {'name': 'I-IV-V-I', 'chords': ['I', 'IV', 'V', 'I'], 'degrees': [1, 4, 5, 1]},
            {'name': 'I-V-vi-IV', 'chords': ['I', 'V', 'vi', 'IV'], 'degrees': [1, 5, 6, 4]},
            {'name': 'I-vi-IV-V', 'chords': ['I', 'vi', 'IV', 'V'], 'degrees': [1, 6, 4, 5]},
            {'name': 'ii-V-I', 'chords': ['ii', 'V', 'I'], 'degrees': [2, 5, 1]},
            {'name': 'I-IV-vi-V', 'chords': ['I', 'IV', 'vi', 'V'], 'degrees': [1, 4, 6, 5]},
        ],
        'jazz': [
            {'name': 'ii-V-I', 'chords': ['ii7', 'V7', 'Imaj7'], 'degrees': [2, 5, 1]},
            {'name': 'I-vi-ii-V', 'chords': ['Imaj7', 'vi7', 'ii7', 'V7'], 'degrees': [1, 6, 2, 5]},
            {'name': 'I-III-vi-II', 'chords': ['Imaj7', 'III7', 'vi7', 'ii7'], 'degrees': [1, 3, 6, 2]},
            {'name': 'vi-ii-V-I', 'chords': ['vi7', 'ii7', 'V7', 'Imaj7'], 'degrees': [6, 2, 5, 1]},
        ],
        'blues': [
            {'name': 'Basic Blues', 'chords': ['I7', 'IV7', 'I7', 'V7', 'IV7', 'I7'], 'degrees': [1, 4, 1, 5, 4, 1]},
        ]
    }
    
    # Get chords for each progression in the given key
    try:
        from music_engine.models import Scale
        
        key_parts = key_name.split()
        key_root = key_parts[0] if key_parts else 'C'
        
        s = Scale(key_root, 'major')
        scale_notes = s.note_names
        
        result = []
        for prog in progressions.get(prog_type, progressions['common']):
            prog_chords = []
            for degree in prog['degrees']:
                idx = (degree - 1) % 7
                root = scale_notes[idx]
                # Determine quality based on degree
                if degree in [1, 4]:
                    quality = 'maj'
                elif degree in [2, 3, 6]:
                    quality = 'min'
                else:
                    quality = 'dom7'
                prog_chords.append(f"{root}{quality}")
            
            result.append({
                'name': prog['name'],
                'roman': prog['chords'],
                'chords': prog_chords
            })
        
        return jsonify({
            'success': True,
            'key': key_name,
            'type': prog_type,
            'progressions': result
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

