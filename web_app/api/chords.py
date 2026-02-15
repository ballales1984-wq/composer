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


def _generate_movable_shapes(chord, note_positions):
    """Genera forme comuni di barre chord."""
    shapes = []
    barre_shapes = [
        {'name': 'Barre (Root 5th)', 'root_string': 5, 'root_fret': 5},
        {'name': 'Barre (Root 5th)', 'root_string': 5, 'root_fret': 7},
    ]
    for shape in barre_shapes:
        frets = [None] * 6
        frets[shape['root_string']] = shape['root_fret']
        shapes.append({
            'position': -1,
            'name': shape['name'],
            'frets': frets,
            'fingers': _suggest_fingers(frets),
        })
    return shapes


def _generate_practical_voicings(chord, engine, max_fret=12):
    """Genera voicings pratici combinando le posizioni delle note."""
    note_positions = {}
    for note in chord.notes:
        pos_list = engine.fretboard.find_note_positions(note, max_fret=max_fret)
        note_positions[note.name] = [{'string': p.string, 'fret': p.fret, 'midi': p.midi} for p in pos_list]

    voicings = []

    # Voicing root position
    root_voicing = _build_voicing(chord, 0, note_positions)
    if root_voicing:
        voicings.append(root_voicing)

    # Voicing inversioni
    inversions = chord.get_all_inversions()
    for i, _ in enumerate(inversions[1:], 1):
        inv_voicing = _build_voicing(chord, i, note_positions)
        if inv_voicing:
            voicings.append(inv_voicing)

    # Barre chord shapes
    movable_shapes = _generate_movable_shapes(chord, note_positions)
    voicings.extend(movable_shapes)

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

