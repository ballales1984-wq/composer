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


@bp.route('/positions', methods=['GET'])
def get_chord_positions():
    """
    Get guitar fretboard positions for chord voicings.
    
    Query parameters:
        root: Root note (e.g., 'C', 'D#')
        quality: Chord quality (e.g., 'maj7', 'min', 'dom7')
        max_fret: Maximum fret position (default 12)
    
    Returns:
        JSON with chord positions for each string/fret combination
    """
    root = request.args.get('root', 'C')
    quality = request.args.get('quality', 'maj')
    max_fret = int(request.args.get('max_fret', 12))
    
    try:
        chord = Chord(root, quality)
        
        # Import here to avoid circular imports
        from music_engine.core.harmony import HarmonyEngine
        engine = HarmonyEngine()
        
        # Get basic positions for each note
        positions = {}
        for note in chord.notes:
            note_positions = engine.fretboard.find_note_positions(note, max_fret=max_fret)
            positions[note.name] = [
                {
                    'string': p.string, 
                    'fret': p.fret,
                    'midi': p.midi
                } 
                for p in note_positions
            ]
        
        # Generate practical voicings (combinations of positions that work together)
        voicings = _generate_practical_voicings(chord, max_fret)
        
        return jsonify({
            'success': True,
            'chord': {
                'name': chord.name,
                'root': chord.root.name,
                'quality': chord.quality,
                'notes': chord.note_names,
            },
            'note_positions': positions,
            'voicings': voicings,
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


def _generate_practical_voicings(chord, max_fret=12):
    """
    Generate practical guitar voicings for a chord.
    
    Returns a list of voicing objects, each containing:
    - position: root position or inversion number
    - name: display name
    - fingers: suggested finger positions
    - frets: fret numbers for each string (6 strings)
    - barre: optional barre information
    """
    from music_engine.core.harmony import HarmonyEngine
    engine = HarmonyEngine()
    
    voicings = []
    chord_semitones = chord.semitones
    root_semitone = chord.root.semitone
    
    # Standard tuning: E2, A2, D3, G3, B3, E4 (MIDI: 40, 45, 50, 55, 59, 64)
    string_bases = [40, 45, 50, 55, 59, 64]  # Low E to high e
    
    # Find positions for each note in the chord
    note_positions = {}
    for note in chord.notes:
        pos_list = engine.fretboard.find_note_positions(note, max_fret=max_fret)
        note_positions[note.name] = [
            {'string': p.string, 'fret': p.fret, 'midi': p.midi}
            for p in pos_list
        ]
    
    # Generate voicings by combining positions
    # Strategy: Start from low strings and find valid positions
    
    # Get all unique notes in chord
    unique_notes = list(set(chord.note_names))
    
    # Generate root position voicing
    root_voicing = _build_voicing(chord, 0, note_positions, string_bases)
    if root_voicing:
        voicings.append(root_voicing)
    
    # Generate inversion voicings
    inversions = chord.get_all_inversions()
    for i, inv in enumerate(inversions[1:], 1):  # Skip root position (already added)
        inv_voicing = _build_voicing(chord, i, note_positions, string_bases)
        if inv_voicing:
            voicings.append(inv_voicing)
    
    # Add some common movable shapes
    movable_shapes = _generate_movable_shapes(chord, note_positions)
    voicings.extend(movable_shapes)
    
    return voicings[:8]  # Return max 8 voicings


def _build_voicing(chord, inversion, note_positions, string_bases):
    """Build a single voicing combining chord notes across strings."""
    chord_notes = chord.notes
    
    # For inversion, rotate the notes
    if inversion > 0 and len(chord_notes) > 1:
        rotated_notes = chord_notes[inversion:] + chord_notes[:inversion]
    else:
        rotated_notes = chord_notes
    
    # Try to build a voicing from low strings to high
    frets = [None] * 6  # 6 strings
    used_strings = []
    
    # Try each note on each string (prefer lower strings for bass)
    for note_idx, note in enumerate(rotated_notes):
        note_name = note.name
        if note_name not in note_positions:
            continue
            
        for pos in note_positions[note_name]:
            string_idx = pos['string']  # 0 = high E, 5 = low E
            
            if string_idx not in used_strings:
                frets[string_idx] = pos['fret']
                used_strings.append(string_idx)
                break
        
        if len(used_strings) >= 3:  # Need at least 3 notes
            break
    
    # Check if we have enough notes
    if sum(1 for f in frets if f is not None) < 3:
        return None
    
    # Create the voicing object
    inversion_names = ['Root Position', '1st Inversion', '2nd Inversion', '3rd Inversion']
    
    return {
        'position': inversion,
        'name': inversion_names[inversion] if inversion < len(inversion_names) else f'Inversion {inversion}',
        'frets': frets,
        'notes': [f for f in frets if f is not None],
        'fingers': _suggest_fingers(frets),
    }


def _suggest_fingers(frets):
    """Suggest finger positions for given fret numbers."""
    fingers = []
    for fret in frets:
        if fret is None:
            fingers.append(0)  # X (don't play)
        elif fret == 0:
            fingers.append(0)  # Open string
        elif fret <= 3:
            fingers.append(1)  # Index
        elif fret <= 5:
            fingers.append(2)  # Middle
        elif fret <= 8:
            fingers.append(3)  # Ring
        else:
            fingers.append(4)  # Pinky
    return fingers


def _generate_movable_shapes(chord, note_positions):
    """Generate common movable chord shapes."""
    shapes = []
    
    # barre chord shapes
    barre_shapes = [
        {'name': 'Barre (Root 5th)', 'root_string': 5, 'root_fret': 5},
        {'name': 'Barre (Root 7th)', 'root_string': 5, 'root_fret': 7},
    ]
    
    return shapes
