"""
Chords API Blueprint - Versione migliorata
REST API endpoints per operazioni sugli accordi.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Blueprint, jsonify, request
from music_engine.models import Chord

bp = Blueprint('chords', __name__, url_prefix='/api/chords')


# --- Helper Functions ---

def sanitize_root(root: str) -> str:
    """Pulizia della root note da URL-encoded accidentals."""
    if not root:
        root = "C"
    return root.replace('%23', '#').replace('%20', ' ').replace('+', ' ')


def get_chord_object(root: str, quality: str):
    """Crea un oggetto Chord e gestisce eccezioni."""
    try:
        chord = Chord(root, quality)
        return chord, None
    except Exception as e:
        return None, str(e)


def _suggest_fingers(frets):
    """Suggerisce dita per i fret (0=open/X, 1=index, 2=middle, 3=ring, 4=pinky)"""
    def mapping(f):
        if f is None or f == 0:
            return 0
        elif f <= 3:
            return 1
        elif f <= 5:
            return 2
        elif f <= 8:
            return 3
        else:
            return 4
    return [mapping(f) for f in frets]


def _build_voicing(chord, inversion, note_positions):
    """Costruisce un singolo voicing combinando le note sugli 6 strings."""
    chord_notes = chord.notes
    rotated_notes = chord_notes[inversion:] + chord_notes[:inversion] if inversion else chord_notes

    frets = [None] * 6
    used_strings = set()

    for note in rotated_notes:
        note_name = note.name
        if note_name not in note_positions:
            continue
        for pos in note_positions[note_name]:
            string_idx = pos['string']
            if string_idx not in used_strings:
                frets[string_idx] = pos['fret']
                used_strings.add(string_idx)
                break
        if len(used_strings) >= 3:
            break

    if sum(1 for f in frets if f is not None) < 3:
        return None

    inversion_names = ['Root Position', '1st Inversion', '2nd Inversion', '3rd Inversion']
    return {
        'position': inversion,
        'name': inversion_names[inversion] if inversion < len(inversion_names) else f'Inversion {inversion}',
        'frets': frets,
        'notes': [f for f in frets if f is not None],
        'fingers': _suggest_fingers(frets),
    }


# Standard chord shapes for common chords (from low E to high E: string 6 to 1)
# Format: [string_6, string_5, string_4, string_3, string_2, string_1]
# null = muted, 0 = open
STANDARD_CHORD_SHAPES = {
    # Major chords
    'C_maj': [None, 3, 2, 0, 1, 0],  # X32010
    'D_maj': [None, None, 0, 2, 3, 2],  # XX0232
    'E_maj': [0, 2, 2, 1, 0, 0],  # 022100
    'F_maj': [1, 3, 3, 2, 1, 1],  # 133211
    'G_maj': [3, 2, 0, 0, 0, 3],  # 320003
    'A_maj': [None, 0, 2, 2, 2, 0],  # X02220
    'B_maj': [None, 2, 4, 4, 4, 2],  # X24442
    
    # Minor chords
    'C_min': [None, 3, 5, 5, 4, 3],  # X35543
    'D_min': [None, None, 0, 2, 3, 1],  # XX0231
    'E_min': [0, 2, 2, 0, 0, 0],  # 022000
    'F_min': [1, 3, 3, 1, 1, 1],  # 133111
    'G_min': [3, 5, 5, 3, 3, 3],  # 355533
    'A_min': [None, 0, 2, 2, 1, 0],  # X02210
    'B_min': [None, 2, 4, 4, 3, 2],  # X24432
    
    # Dominant 7th
    'C_dom7': [None, 3, 2, 3, 1, 0],  # X3231
    'D_dom7': [None, None, 0, 2, 1, 2],  # XX0212
    'E_dom7': [0, 2, 0, 1, 0, 0],  # 020100
    'G_dom7': [3, 1, 0, 0, 0, 1],  # 310001
    'A_dom7': [None, 0, 2, 0, 2, 0],  # X02020
    'B_dom7': [None, 2, 1, 2, 0, 2],  # X21202
    
    # Major 7th
    'C_maj7': [None, 3, 2, 0, 0, 0],  # X32000
    'A_maj7': [None, 0, 2, 1, 2, 0],  # X02120
    
    # Minor 7th
    'C_min7': [None, 3, 5, 3, 4, 3],  # X35343
    'A_min7': [None, 0, 2, 0, 1, 0],  # X02010
}


def _get_chord_shape(root, quality):
    """Get standard chord shape for a chord."""
    # Normalize quality
    q = quality.lower().replace('maj', 'maj').replace('min', 'min').replace('dom', 'dom').replace('dim', 'dim').replace('aug', 'aug')
    
    # Build the key
    key = root + '_' + q
    
    # Try to find exact match first
    if key in STANDARD_CHORD_SHAPES:
        return STANDARD_CHORD_SHAPES[key].copy()
    
    # Try variations
    for q_var in [q, q.replace('7', '_dom7'), q.replace('maj7', '_maj7'), q.replace('min7', '_min7')]:
        if root + '_' + q_var in STANDARD_CHORD_SHAPES:
            return STANDARD_CHORD_SHAPES[root + '_' + q_var].copy()
    
    return None


def _generate_practical_voicings(chord, engine, max_fret=12):
    """Genera voicings pratici combinando le posizioni delle note."""
    # Extract just the note name without octave (e.g., 'C4' -> 'C')
    root = chord.root.name
    if root[-1].isdigit():
        root = root[:-1]
    quality = chord.quality
    
    # First, try to get standard chord shape
    standard_shape = _get_chord_shape(root, quality)
    
    voicings = []
    
    # Add standard shape if available
    if standard_shape:
        voicings.append({
            'position': 0,
            'name': 'Standard Shape',
            'frets': standard_shape,
            'notes': [f for f in standard_shape if f is not None],
            'fingers': _suggest_fingers(standard_shape),
        })
    
    # Also generate algorithmic voicings as backup
    note_positions = {}
    for note in chord.notes:
        pos_list = engine.fretboard.find_note_positions(note, max_fret=max_fret)
        note_positions[note.name] = [{'string': p.string, 'fret': p.fret, 'midi': p.midi} for p in pos_list]

    # Root position
    root_voicing = _build_voicing(chord, 0, note_positions)
    if root_voicing and root_voicing not in voicings:
        # Only add if significantly different from standard
        voicings.append(root_voicing)

    # Inversions
    inversions = chord.get_all_inversions()
    for i, _ in enumerate(inversions[1:], 1):
        inv_voicing = _build_voicing(chord, i, note_positions)
        if inv_voicing and inv_voicing not in voicings:
            voicings.append(inv_voicing)

    # Barre chord shapes - common movable shapes
    barre_shapes = [
        {'name': 'Barre E-Shape', 'base_fret': 5, 'root_string': 5},
        {'name': 'Barre A-Shape', 'base_fret': 5, 'root_string': 4},
    ]
    
    for shape in barre_shapes:
        frets = [None] * 6
        # Simplified barre shape
        base_fret = shape['base_fret']
        if base_fret <= max_fret:
            # Root on the specified string
            for i in range(shape['root_string'], 6):
                if frets[i] is None:
                    frets[i] = base_fret + (5 - i)
            
            voicings.append({
                'position': -1,
                'name': shape['name'],
                'frets': frets,
                'notes': [f for f in frets if f is not None],
                'fingers': _suggest_fingers(frets),
            })

    return voicings[:8]  # massimo 8 voicings


# --- Endpoints ---

@bp.route('', methods=['GET'])
def get_chord():
    root = sanitize_root(request.args.get('root'))
    quality = request.args.get('quality', 'maj')
    chord, error = get_chord_object(root, quality)
    if error:
        return jsonify({'success': False, 'error': error}), 400

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


@bp.route('/list', methods=['GET'])
def list_chord_qualities():
    from music_engine.models.chord import CHORD_INTERVALS, CHORD_NAMES
    qualities = [{'id': q, 'name': CHORD_NAMES.get(q, q.upper()), 'intervals': i} for q, i in CHORD_INTERVALS.items()]
    return jsonify({'success': True, 'qualities': qualities})


@bp.route('/inversions', methods=['GET'])
def get_inversions():
    root = sanitize_root(request.args.get('root'))
    quality = request.args.get('quality', 'maj')
    chord, error = get_chord_object(root, quality)
    if error:
        return jsonify({'success': False, 'error': error}), 400

    inversions_data = []
    for i, inv in enumerate(chord.get_all_inversions()):
        inversions_data.append({
            'position': i,
            'bass': inv.notes[0].name if inv.notes else root,
            'notes': [n.name for n in inv.notes],
        })
    return jsonify({'success': True, 'inversions': inversions_data})


@bp.route('/voicing', methods=['GET'])
def get_voicing():
    root = sanitize_root(request.args.get('root'))
    quality = request.args.get('quality', 'maj')
    octave = int(request.args.get('octave', 4))
    chord, error = get_chord_object(root, quality)
    if error:
        return jsonify({'success': False, 'error': error}), 400

    voicing_data = [{'note': n.name, 'octave': o} for n, o in chord.get_voicing(octave=octave, spread=True)]
    return jsonify({'success': True, 'voicing': voicing_data})


@bp.route('/positions', methods=['GET'])
def get_chord_positions():
    root = sanitize_root(request.args.get('root'))
    quality = request.args.get('quality', 'maj')
    max_fret = int(request.args.get('max_fret', 12))
    chord, error = get_chord_object(root, quality)
    if error:
        return jsonify({'success': False, 'error': error}), 400

    from music_engine.core.harmony import HarmonyEngine
    engine = HarmonyEngine()
    voicings = _generate_practical_voicings(chord, engine, max_fret)

    # Posizioni di ogni nota
    positions = {}
    for note in chord.notes:
        note_positions = engine.fretboard.find_note_positions(note, max_fret=max_fret)
        positions[note.name] = [{'string': p.string, 'fret': p.fret, 'midi': p.midi} for p in note_positions]

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

