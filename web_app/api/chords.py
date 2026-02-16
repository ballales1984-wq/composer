"""
Chords API Blueprint - Versione migliorata con modalità realistic/theoretical
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
    """Costruisce un singolo voicing combinando le note sugli 6 strings (theoretical mode)."""
    chord_notes = chord.notes
    rotated_notes = chord_notes[inversion:] + chord_notes[:inversion] if inversion else chord_notes

    frets = [None] * 6
    used_strings = set()

    for note in rotated_notes:
        note_name = note.name
        if note_name not in note_positions:
            continue
        for pos in note_positions[note_name]:
            string_num = pos['string']
            string_idx = 6 - string_num
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


# Standard chord shapes
STANDARD_CHORD_SHAPES = {
    'C_maj': [None, 3, 2, 0, 1, 0],
    'D_maj': [None, None, 0, 2, 3, 2],
    'E_maj': [0, 2, 2, 1, 0, 0],
    'F_maj': [1, 3, 3, 2, 1, 1],
    'G_maj': [3, 2, 0, 0, 0, 3],
    'A_maj': [None, 0, 2, 2, 2, 0],
    'B_maj': [None, 2, 4, 4, 4, 2],
    'C_min': [None, 3, 5, 5, 4, 3],
    'D_min': [None, None, 0, 2, 3, 1],
    'E_min': [0, 2, 2, 0, 0, 0],
    'F_min': [1, 3, 3, 1, 1, 1],
    'G_min': [3, 5, 5, 3, 3, 3],
    'A_min': [None, 0, 2, 2, 1, 0],
    'B_min': [None, 2, 4, 4, 3, 2],
    'C_dom7': [None, 3, 2, 3, 1, 0],
    'D_dom7': [None, None, 0, 2, 1, 2],
    'E_dom7': [0, 2, 0, 1, 0, 0],
    'G_dom7': [3, 1, 0, 0, 0, 1],
    'A_dom7': [None, 0, 2, 0, 2, 0],
    'B_dom7': [None, 2, 1, 2, 0, 2],
    'C_maj7': [None, 3, 2, 0, 0, 0],
    'A_maj7': [None, 0, 2, 1, 2, 0],
    'C_min7': [None, 3, 5, 3, 4, 3],
    'A_min7': [None, 0, 2, 0, 1, 0],
}


# Note to fret mapping for barre chords
# E-shape: root is on string 6 (low E), form is like E major shape
# A-shape: root is on string 5 (A string), form is like A major shape
NOTE_TO_FRET_E_SHAPE = {
    'C': 8, 'C#': 9, 'D': 10, 'D#': 11, 'E': 12, 'F': 1, 'F#': 2, 'G': 3, 'G#': 4, 'A': 5, 'A#': 6, 'B': 7
}
NOTE_TO_FRET_A_SHAPE = {
    'C': 3, 'C#': 4, 'D': 5, 'D#': 6, 'E': 7, 'F': 8, 'F#': 9, 'G': 10, 'G#': 11, 'A': 12, 'A#': 1, 'B': 2
}


def _get_chord_shape(root, quality):
    """Get standard chord shape for a chord."""
    q = quality.lower().replace('maj', 'maj').replace('min', 'min').replace('dom', 'dom').replace('dim', 'dim').replace('aug', 'aug')
    key = root + '_' + q
    
    if key in STANDARD_CHORD_SHAPES:
        return STANDARD_CHORD_SHAPES[key].copy()
    
    for q_var in [q, q.replace('7', '_dom7'), q.replace('maj7', '_maj7'), q.replace('min7', '_min7')]:
        if root + '_' + q_var in STANDARD_CHORD_SHAPES:
            return STANDARD_CHORD_SHAPES[root + '_' + q_var].copy()
    
    return None


# CAGED system chord shapes - known correct voicings
# Format: quality -> {shape_name: [frets]}
# Frets format: [string6, string5, string4, string3, string2, string1]
CAGED_SHAPES = {
    'maj': {
        'C': {'open': [None, 3, 2, 0, 1, 0], 'E_barre': [8, 10, 10, 9, 8, 8], 'A_barre': [None, 3, 5, 5, 5, 3]},
        'D': {'open': [None, None, 0, 2, 3, 2], 'E_barre': [10, 12, 12, 11, 10, 10], 'A_barre': [None, 5, 7, 7, 7, 5]},
        'E': {'open': [0, 2, 2, 1, 0, 0], 'E_barre': [12, 14, 14, 13, 12, 12], 'A_barre': [None, 7, 9, 9, 9, 7]},
        'F': {'open': [1, 3, 3, 2, 1, 1], 'E_barre': [1, 3, 3, 2, 1, 1], 'A_barre': [None, 8, 10, 10, 10, 8]},
        'G': {'open': [3, 2, 0, 0, 0, 3], 'E_barre': [3, 5, 5, 4, 3, 3], 'A_barre': [None, 10, 12, 12, 12, 10]},
        'A': {'open': [None, 0, 2, 2, 2, 0], 'E_barre': [5, 7, 7, 6, 5, 5], 'A_barre': [None, 0, 2, 2, 2, 0]},
        'B': {'open': [None, 2, 4, 4, 4, 2], 'E_barre': [7, 9, 9, 8, 7, 7], 'A_barre': [None, 2, 4, 4, 4, 2]},
    },
    'min': {
        'C': {'open': [None, 3, 5, 5, 4, 3], 'E_barre': [8, 10, 10, 8, 8, 8], 'A_barre': [None, 3, 5, 5, 4, 3]},
        'D': {'open': [None, None, 0, 2, 3, 1], 'E_barre': [10, 12, 12, 10, 10, 10], 'A_barre': [None, 5, 7, 7, 6, 5]},
        'E': {'open': [0, 2, 2, 0, 0, 0], 'E_barre': [12, 14, 14, 12, 12, 12], 'A_barre': [None, 7, 9, 9, 8, 7]},
        'F': {'open': [1, 3, 3, 1, 1, 1], 'E_barre': [1, 3, 3, 1, 1, 1], 'A_barre': [None, 8, 10, 10, 9, 8]},
        'G': {'open': [3, 5, 5, 3, 3, 3], 'E_barre': [3, 5, 5, 3, 3, 3], 'A_barre': [None, 10, 12, 12, 11, 10]},
        'A': {'open': [None, 0, 2, 2, 1, 0], 'E_barre': [5, 7, 7, 5, 5, 5], 'A_barre': [None, 0, 2, 2, 1, 0]},
        'B': {'open': [None, 2, 4, 4, 3, 2], 'E_barre': [7, 9, 9, 7, 7, 7], 'A_barre': [None, 2, 4, 4, 3, 2]},
    },
}

def _get_caged_shape(root, quality, shape_type, max_fret=12):
    """Get CAGED shape for chord if valid."""
    root_upper = root.upper()
    
    # Handle enharmonics
    enharmonic_map = {
        'C#': 'D#', 'DB': 'C#',
        'D#': 'D#', 'EB': 'D#',
        'F#': 'F#', 'GB': 'F#',
        'G#': 'G#', 'AB': 'G#',
        'A#': 'A#', 'BB': 'A#',
    }
    
    # For B, use C shape shifted by 2 frets
    is_b_transposed = False
    if root_upper == 'B':
        root_upper = 'C'
        is_b_transposed = True
    elif root_upper in enharmonic_map:
        root_upper = enharmonic_map[root_upper]
    
    # Map common notations
    quality_map = {'maj': 'maj', 'min': 'min', 'm': 'min'}
    q = quality_map.get(quality, quality)
    
    if q in CAGED_SHAPES and root_upper in CAGED_SHAPES[q]:
        if shape_type in CAGED_SHAPES[q][root_upper]:
            frets = CAGED_SHAPES[q][root_upper][shape_type]
            # For transposed B, shift all frets by 2
            if is_b_transposed and frets:
                frets = [f + 2 if f is not None else None for f in frets]
            # Check if all frets are within range
            if all(f is None or f <= max_fret for f in frets):
                return frets
    return None


def _generate_realistic_voicings(chord, max_fret=12):
    """Generate voicings using REAL guitar chord shapes (CAGED-based)."""
    root = chord.root.name
    if root[-1].isdigit():
        root = root[:-1]
    quality = chord.quality
    
    voicings = []
    root_upper = root.upper()
    
    # Get open chord if available
    standard_shape = _get_chord_shape(root, quality)
    if standard_shape:
        voicings.append({
            'position': 0,
            'name': 'Open Position',
            'frets': standard_shape,
            'notes': [f for f in standard_shape if f is not None],
            'fingers': _suggest_fingers(standard_shape),
            'is_barre': False,
            'base_fret': 1,
        })
    
    # Generate CAGED barre chords using correct shapes
    # Use hardcoded CAGED shapes that are known to be correct
    e_frets = _get_caged_shape(root, quality, 'E_barre', max_fret)
    if e_frets:
        voicings.append({
            'position': -1,
            'name': f'Barre E-Shape (fret {e_frets[0]})',
            'frets': e_frets,
            'notes': [f for f in e_frets if f is not None],
            'fingers': _suggest_fingers(e_frets),
            'is_barre': True,
            'base_fret': e_frets[0],
        })
    
    # A-shape barre
    a_frets = _get_caged_shape(root, quality, 'A_barre', max_fret)
    if a_frets:
        # Find the first non-None fret for base_fret
        base_fret = next((f for f in a_frets if f is not None), 1)
        voicings.append({
            'position': -1,
            'name': f'Barre A-Shape (fret {base_fret})',
            'frets': a_frets,
            'notes': [f for f in a_frets if f is not None],
            'fingers': _suggest_fingers(a_frets),
            'is_barre': True,
            'base_fret': base_fret,
        })
    
    # Add triad voicings (movable shapes)
    if quality in ['maj', 'min', 'dim', 'aug']:
        triad_voicings = [
            {'name': 'Triad (D-shape)', 'frets': [None, None, 0, 2, 3, 2]},
            {'name': 'Triad (A-shape)', 'frets': [None, 0, 2, 2, 1, 0]},
            {'name': 'Triad (E-shape)', 'frets': [0, 2, 2, 1, 0, 0]},
            {'name': 'Triad (1st inv)', 'frets': [None, 0, 0, 2, 3, 2]},
            {'name': 'Triad (2nd inv)', 'frets': [0, 0, 2, 2, 1, 0]},
        ]
        for tv in triad_voicings:
            voicings.append({
                'position': 0,
                'name': tv['name'],
                'frets': tv['frets'],
                'notes': [f for f in tv['frets'] if f is not None],
                'fingers': _suggest_fingers(tv['frets']),
                'is_barre': False,
                'base_fret': 1,
            })
    
    # Add seventh chord voicings
    if '7' in quality or quality in ['maj7', 'min7', 'dom7']:
        seventh_voicings = [
            {'name': '7th (1st string)', 'frets': [None, 3, 2, 3, 1, 0]},
            {'name': '7th (2nd string)', 'frets': [None, 3, 1, 3, 2, 0]},
            {'name': '7th (barre)', 'frets': [None, 5, 7, 5, 7, 5]},
        ]
        for sv in seventh_voicings:
            voicings.append({
                'position': 0,
                'name': sv['name'],
                'frets': sv['frets'],
                'notes': [f for f in sv['frets'] if f is not None],
                'fingers': _suggest_fingers(sv['frets']),
                'is_barre': 'barre' in sv['name'].lower(),
                'base_fret': 5 if 'barre' in sv['name'].lower() else 1,
            })
    
    return voicings[:8]


def _generate_theoretical_voicings(chord, engine, max_fret=12):
    """Generate voicings using THEORETICAL algorithm (all possible combinations)."""
    root = chord.root.name
    if root[-1].isdigit():
        root = root[:-1]
    quality = chord.quality
    
    voicings = []
    
    standard_shape = _get_chord_shape(root, quality)
    
    if standard_shape:
        voicings.append({
            'position': 0,
            'name': 'Standard Shape',
            'frets': standard_shape,
            'notes': [f for f in standard_shape if f is not None],
            'fingers': _suggest_fingers(standard_shape),
            'is_barre': False,
            'base_fret': 1,
        })
    
    note_positions = {}
    for note in chord.notes:
        pos_list = engine.fretboard.find_note_positions(note, max_fret=max_fret)
        note_positions[note.name] = [{'string': p.string, 'fret': p.fret, 'midi': p.midi} for p in pos_list]

    root_voicing = _build_voicing(chord, 0, note_positions)
    if root_voicing and root_voicing not in voicings:
        root_voicing['is_barre'] = False
        root_voicing['base_fret'] = 1
        voicings.append(root_voicing)

    inversions = chord.get_all_inversions()
    for i, _ in enumerate(inversions[1:], 1):
        inv_voicing = _build_voicing(chord, i, note_positions)
        if inv_voicing and inv_voicing not in voicings:
            inv_voicing['is_barre'] = False
            inv_voicing['base_fret'] = 1
            voicings.append(inv_voicing)

    barre_shapes = [
        {'name': 'Barre E-Shape', 'base_fret': 5, 'root_string': 5},
        {'name': 'Barre A-Shape', 'base_fret': 5, 'root_string': 4},
    ]
    
    for shape in barre_shapes:
        frets = [None] * 6
        base_fret = shape['base_fret']
        if base_fret <= max_fret:
            for i in range(shape['root_string'], 6):
                if frets[i] is None:
                    frets[i] = base_fret + (5 - i)
            
            voicings.append({
                'position': -1,
                'name': shape['name'],
                'frets': frets,
                'notes': [f for f in frets if f is not None],
                'fingers': _suggest_fingers(frets),
                'is_barre': True,
                'base_fret': base_fret,
            })

    return voicings[:8]


def _generate_practical_voicings(chord, engine, max_fret=12, mode='realistic'):
    """Generate voicings based on mode: 'realistic' or 'theoretical'."""
    if mode == 'theoretical':
        return _generate_theoretical_voicings(chord, engine, max_fret)
    else:
        return _generate_realistic_voicings(chord, max_fret)


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
    import logging
    logger = logging.getLogger(__name__)
    
    root = sanitize_root(request.args.get('root'))
    quality = request.args.get('quality', 'maj')
    max_fret = int(request.args.get('max_fret', 12))
    mode = request.args.get('mode', 'realistic')
    
    logger.info(f"[DEBUG] /positions called with root={root}, quality={quality}, mode={mode}")
    
    if mode not in ['realistic', 'theoretical']:
        mode = 'realistic'
    
    chord, error = get_chord_object(root, quality)
    if error:
        return jsonify({'success': False, 'error': error}), 400

    from music_engine.core.harmony import HarmonyEngine
    engine = HarmonyEngine()
    voicings = _generate_practical_voicings(chord, engine, max_fret, mode)

    positions = {}
    for note in chord.notes:
        note_positions = engine.fretboard.find_note_positions(note, max_fret=max_fret)
        positions[note.name] = [{'string': p.string, 'fret': p.fret, 'midi': p.midi} for p in note_positions]

    return jsonify({
        'success': True,
        'mode': mode,
        'chord': {
            'name': chord.name,
            'root': chord.root.name,
            'quality': chord.quality,
            'notes': chord.note_names,
        },
        'note_positions': positions,
        'voicings': voicings,
    })

