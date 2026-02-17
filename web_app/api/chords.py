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
# Using only OPEN and A-shape barre (more reliable)
CAGED_SHAPES = {
    'maj': {
        'C': {'open': [None, 3, 2, 0, 1, 0], 'A_barre': [None, 3, 5, 5, 5, 3]},
        'D': {'open': [None, None, 0, 2, 3, 2], 'A_barre': [None, 5, 7, 7, 7, 5]},
        'E': {'open': [0, 2, 2, 1, 0, 0], 'A_barre': [None, 7, 9, 9, 9, 7]},
        'F': {'open': [1, 3, 3, 2, 1, 1], 'A_barre': [None, 8, 10, 10, 10, 8]},
        'G': {'open': [3, 2, 0, 0, 0, 3], 'A_barre': [None, 10, 12, 12, 12, 10]},
        'A': {'open': [None, 0, 2, 2, 2, 0], 'A_barre': [None, 0, 2, 2, 2, 0]},
        'B': {'open': [None, 2, 4, 4, 4, 2], 'A_barre': [None, 2, 4, 4, 4, 2]},
        # Add sharp/flat major chords - use realistic lower-fret barre
        'C#': {'open': [None, 4, 3, 1, 1, 1], 'A_barre': [None, 4, 6, 6, 6, 4]},
        'D#': {'open': [None, None, 1, 3, 4, 3], 'A_barre': [None, 6, 8, 8, 8, 6]},
        'F#': {'open': [2, 4, 4, 3, 2, 2], 'A_barre': [None, 9, 11, 11, 11, 9]},
        'G#': {'open': [4, 3, 1, 1, 1, 4], 'A_barre': [None, 4, 6, 6, 6, 4]},  # G# at 4th fret
        'A#': {'open': [None, 1, 3, 3, 3, 1], 'A_barre': [None, 1, 3, 3, 3, 1]},  # Bb at 1st fret
    },
    'min': {
        'C': {'open': [None, 3, 5, 5, 4, 3], 'A_barre': [None, 3, 5, 5, 4, 3]},
        'D': {'open': [None, None, 0, 2, 3, 1], 'A_barre': [None, 5, 7, 7, 6, 5]},
        'E': {'open': [0, 2, 2, 0, 0, 0], 'A_barre': [None, 7, 9, 9, 8, 7]},
        'F': {'open': [1, 3, 3, 1, 1, 1], 'A_barre': [None, 8, 10, 10, 9, 8]},
        'G': {'open': [3, 5, 5, 3, 3, 3], 'A_barre': [None, 10, 12, 12, 11, 10]},
        'A': {'open': [None, 0, 2, 2, 1, 0], 'A_barre': [None, 0, 2, 2, 1, 0]},
        'B': {'open': [None, 2, 4, 4, 3, 2], 'A_barre': [None, 2, 4, 4, 3, 2]},
    },
    '7': {
        # Dominant 7th chords - using correct CAGED voicings
        'C': {'open': [None, 3, 2, 3, 1, 0], 'A_barre': [None, 3, 5, 3, 5, 3]},
        'D': {'open': [None, None, 0, 2, 1, 2], 'A_barre': [None, None, 0, 2, 1, 2]},
        'E': {'open': [0, 2, 0, 1, 0, 0], 'A_barre': [None, 7, 9, 7, 9, 7]},
        'F': {'open': [1, 3, 1, 2, 1, 1], 'A_barre': [None, 8, 10, 8, 10, 8]},
        'G': {'open': [3, 2, 0, 0, 0, 1], 'A_barre': [None, 10, 12, 10, 12, 10]},
        'A': {'open': [None, 0, 2, 0, 1, 0], 'A_barre': [None, 12, 14, 12, 14, 12]},
        'B': {'open': [None, 2, 1, 2, 0, 2], 'A_barre': [None, 14, 16, 14, 16, 14]},
        # Add sharps/flats with correct voicings
        'C#': {'open': [None, 4, 3, 4, 2, 1], 'A_barre': [None, 4, 6, 4, 6, 4]},
        'D#': {'open': [None, None, 1, 3, 2, 3], 'A_barre': [None, 6, 8, 6, 8, 6]},
        'F#': {'open': [2, 4, 2, 3, 2, 2], 'A_barre': [None, 9, 11, 9, 11, 9]},
        'G#': {'open': [4, 6, 4, 5, 4, 4], 'A_barre': [None, 4, 6, 4, 6, 4]},
        'A#': {'open': [None, 1, 3, 1, 2, 1], 'A_barre': [None, 1, 3, 1, 2, 1]},
    },
    'maj7': {
        # Major 7th chords
        'C': {'open': [None, 3, 2, 0, 0, 0], 'A_barre': [None, 3, 5, 4, 5, 3]},
        'D': {'open': [None, None, 0, 2, 2, 0], 'A_barre': [None, 5, 7, 6, 7, 5]},
        'E': {'open': [0, 2, 2, 1, 0, 0], 'A_barre': [None, 7, 9, 8, 9, 7]},
        'F': {'open': [1, 3, 3, 2, 1, 0], 'A_barre': [None, 8, 10, 9, 10, 8]},
        'G': {'open': [3, 2, 0, 0, 0, 2], 'A_barre': [None, 10, 12, 11, 12, 10]},
        'A': {'open': [None, 0, 2, 1, 2, 0], 'A_barre': [None, 12, 14, 13, 14, 12]},
        'B': {'open': [None, 3, 2, 3, 2, 2], 'A_barre': [None, 14, 16, 15, 16, 14]},
        # Add sharps/flats
        'C#': {'open': [None, 4, 3, 1, 1, 1], 'A_barre': [None, 4, 6, 5, 6, 4]},
        'D#': {'open': [None, None, 1, 3, 2, 1], 'A_barre': [None, 6, 8, 7, 8, 6]},
        'F#': {'open': [2, 4, 4, 3, 2, 2], 'A_barre': [None, 9, 11, 10, 11, 9]},
        'G#': {'open': [4, 3, 1, 1, 1, 3], 'A_barre': [None, 11, 13, 12, 13, 11]},
        'A#': {'open': [None, 1, 3, 2, 3, 1], 'A_barre': [None, 1, 3, 2, 3, 1]},
    },
    'min7': {
        # Minor 7th chords
        'C': {'open': [None, 3, 5, 3, 4, 3], 'A_barre': [None, 3, 5, 3, 4, 3]},
        'D': {'open': [None, None, 0, 2, 1, 1], 'A_barre': [None, 5, 7, 5, 6, 5]},
        'E': {'open': [0, 2, 0, 0, 0, 0], 'A_barre': [None, 7, 9, 7, 10, 7]},
        'G': {'open': [3, 5, 3, 3, 3, 3], 'A_barre': [None, 10, 12, 10, 11, 10]},
        'A': {'open': [None, 0, 2, 0, 1, 0], 'A_barre': [None, 12, 14, 12, 13, 12]},
        # Add more
        'C#': {'open': [None, 4, 6, 4, 5, 4], 'A_barre': [None, 4, 6, 4, 5, 4]},
        'D#': {'open': [None, None, 1, 3, 2, 2], 'A_barre': [None, 6, 8, 6, 7, 6]},
        'F#': {'open': [2, 4, 2, 2, 2, 2], 'A_barre': [None, 9, 11, 9, 10, 9]},
        'G#': {'open': [4, 6, 4, 4, 4, 4], 'A_barre': [None, 11, 13, 11, 12, 11]},
        'A#': {'open': [None, 1, 3, 1, 2, 1], 'A_barre': [None, 1, 3, 1, 2, 1]},
    },
}

# Map any root to the closest CAGED shape using the fret number
ROOT_TO_BASE = {
    'C': 0, 'C#': 1, 'DB': 1,
    'D': 2, 'D#': 3, 'EB': 3,
    'E': 4, 'F': 5, 'F#': 6, 'GB': 6,
    'G': 7, 'G#': 8, 'AB': 8,
    'A': 9, 'A#': 10, 'BB': 10,
    'B': 11,
}

# Reference shapes for transposing (using E shape as base)
# These are the barre chord root positions on the fretboard
REFERENCE_BARRE_ROOTS = {
    'E': 0,   # E at nut
    'F': 1,   # F at 1st fret
    'F#': 2,  # Gb/F# at 2nd fret
    'G': 3,   # G at 3rd fret
    'G#': 4,  # Ab/G# at 4th fret
    'A': 5,   # A at 5th fret
    'A#': 6,  # Bb/A# at 6th fret
    'B': 7,   # B at 7th fret
    'C': 8,   # C at 8th fret
    'C#': 9,  # Db/C# at 9th fret
    'D': 10,  # D at 10th fret
    'D#': 11, # Eb/D# at 11th fret
}

def _get_caged_shape(root, quality, shape_type, max_fret=12):
    """Get CAGED shape for chord - with transposing for all 12 roots."""
    root_upper = root.upper()
    
    # Handle enharmonics
    enharmonic_map = {
        'C#': 'C#', 'DB': 'C#',
        'D#': 'D#', 'EB': 'D#',
        'F#': 'F#', 'GB': 'F#',
        'G#': 'G#', 'AB': 'G#',
        'A#': 'A#', 'BB': 'A#',
    }
    
    original_root = root_upper
    if root_upper in enharmonic_map:
        root_upper = enharmonic_map[root_upper]
    
    # Map common notations
    quality_map = {
        'maj': 'maj', 
        'min': 'min', 
        'm': 'min',
        '7': '7',
        'dom7': '7',
        'maj7': 'maj7',
        'min7': 'min7',
        'm7': 'min7',
    }
    q = quality_map.get(quality, quality)
    
    # First try: direct match in CAGED_SHAPES
    if q in CAGED_SHAPES and root_upper in CAGED_SHAPES[q]:
        if shape_type in CAGED_SHAPES[q][root_upper]:
            frets = CAGED_SHAPES[q][root_upper][shape_type]
            if all(f is None or f <= max_fret for f in frets):
                return frets
    
    # Second try: transpose from a reference root
    # Use E-shape barre as reference (it's at the lowest fret for E)
    if shape_type == 'A_barre':
        # Get target fret position for this root
        target_fret = REFERENCE_BARRE_ROOTS.get(root_upper, REFERENCE_BARRE_ROOTS.get(original_root, 0))
        
        # Try transposing from each available reference
        for ref_root in ['E', 'A', 'C', 'D', 'F', 'G']:
            if q in CAGED_SHAPES and ref_root in CAGED_SHAPES[q]:
                if 'A_barre' in CAGED_SHAPES[q][ref_root]:
                    ref_frets = CAGED_SHAPES[q][ref_root]['A_barre']
                    ref_fret = REFERENCE_BARRE_ROOTS.get(ref_root, 0)
                    fret_shift = target_fret - ref_fret
                    if fret_shift >= 0:
                        transposed = [f + fret_shift if f is not None else None for f in ref_frets]
                        if all(f is None or f <= max_fret for f in transposed):
                            return transposed
    
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
    
    # Use only A-shape barre (E-shape was removed due to incorrect formulas)
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
    
    # Add seventh chord voicings using CAGED shapes
    seventh_qualities = ['7', 'dom7', 'maj7', 'min7', 'm7']
    if any(q in quality for q in seventh_qualities) or quality in seventh_qualities:
        # First try CAGED shapes for 7th chords
        seventh_frets = _get_caged_shape(root, quality, 'A_barre', max_fret)
        if seventh_frets:
            base_fret = next((f for f in seventh_frets if f is not None), 1)
            voicings.append({
                'position': -1,
                'name': f'A-Barren (fret {base_fret})',
                'frets': seventh_frets,
                'notes': [f for f in seventh_frets if f is not None],
                'fingers': _suggest_fingers(seventh_frets),
                'is_barre': True,
                'base_fret': base_fret,
            })
        
        # Also try open shape if available
        open_frets = _get_caged_shape(root, quality, 'open', max_fret)
        if open_frets:
            voicings.append({
                'position': 0,
                'name': 'Open Position',
                'frets': open_frets,
                'notes': [f for f in open_frets if f is not None],
                'fingers': _suggest_fingers(open_frets),
                'is_barre': False,
                'base_fret': 1,
            })
        
        # Add common movable 7th voicings as fallback
        seventh_voicings = [
            {'name': '7th (E-shape)', 'frets': [0, 2, 0, 1, 0, 0]},
            {'name': '7th (A-shape)', 'frets': [None, 0, 2, 0, 1, 0]},
            {'name': '7th (D-shape)', 'frets': [None, None, 0, 2, 1, 2]},
        ]
        for sv in seventh_voicings:
            voicings.append({
                'position': 0,
                'name': sv['name'],
                'frets': sv['frets'],
                'notes': [f for f in sv['frets'] if f is not None],
                'fingers': _suggest_fingers(sv['frets']),
                'is_barre': False,
                'base_fret': 1,
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


@bp.route('/play', methods=['POST'])
def play_chord():
    """Play a chord using audio. Accepts JSON with chord notes."""
    try:
        data = request.get_json()
        notes = data.get('notes', [])
        duration = data.get('duration', 2.0)
        
        if not notes:
            return jsonify({'success': False, 'error': 'No notes provided'}), 400
        
        # Try to play using the music_engine audio system
        try:
            import sys
            import os
            sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
            from music_engine.utils.audio import play_chord as engine_play_chord
            
            # Convert notes to proper format and play
            # Notes can be like 'C4', 'E4', 'G4'
            play_notes = [str(n) for n in notes]
            engine_play_chord(play_notes, duration)
            
            return jsonify({
                'success': True, 
                'message': f'Playing chord: {" ".join(play_notes)}',
                'notes': play_notes
            })
        except ImportError as e:
            return jsonify({
                'success': False, 
                'error': f'Audio not available: {str(e)}'
            }), 500
        except Exception as e:
            return jsonify({
                'success': False, 
                'error': f'Error playing chord: {str(e)}'
            }), 500
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


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

