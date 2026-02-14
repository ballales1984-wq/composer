"""
Analyzer API Blueprint

Unified API endpoint for analyzing chords and scales.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from flask import Blueprint, jsonify, request
from music_engine.core.harmony import HarmonyEngine
from music_engine.models import Chord, Scale

# Blueprint name
BLUEPRINT_NAME = 'analyzer'

bp = Blueprint('analyzer', __name__, url_prefix='/api/analyzer')


@bp.route('', methods=['GET'])
def analyze_input():
    """
    Analyze an input string (chord or scale).
    
    Query parameters:
        input: The chord or scale to analyze (e.g., 'Cmaj7', 'C major')
    
    Returns:
        JSON with analysis results including:
        - type: 'chord' or 'scale'
        - notes: list of notes
        - intervals: list of intervals
        - For chords: compatible scales
        - For scales: diatonic chords and compatible chords
        - fretboard_positions: positions on guitar fretboard
    """
    input_str = request.args.get('input', '').strip()
    
    if not input_str:
        return jsonify({
            'success': False,
            'error': 'Please provide an input parameter'
        }), 400
    
    try:
        engine = HarmonyEngine()
        result = engine.analyze_input(input_str)
        
        if not result.get('success', False):
            return jsonify({
                'success': False,
                'error': result.get('error', 'Could not parse input')
            }), 400
        
        # Format response
        if result['type'] == 'chord':
            return jsonify(format_chord_result(result))
        else:
            return jsonify(format_scale_result(result))
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@bp.route('/chord', methods=['GET'])
def analyze_chord():
    """
    Analyze a chord and find compatible scales.
    
    Query parameters:
        root: Root note (e.g., 'C', 'D#')
        quality: Chord quality (e.g., 'maj7', 'min', 'dom7')
    
    Returns:
        JSON with chord analysis and compatible scales
    """
    root = request.args.get('root', 'C')
    quality = request.args.get('quality', 'maj')
    
    try:
        chord = Chord(root, quality)
        engine = HarmonyEngine()
        
        # Get compatible scales
        compatible = engine.find_compatible_scales(chord)
        
        # Format results
        return jsonify({
            'success': True,
            'type': 'chord',
            'chord': {
                'name': chord.name,
                'root': chord.root.name,
                'quality': chord.quality,
                'notes': chord.note_names,
                'intervals': chord.intervals,
            },
            'compatible_scales': format_compatible_scales(compatible),
            'fretboard_positions': format_fretboard_positions(
                engine._get_chord_positions(chord)
            ),
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@bp.route('/scale', methods=['GET'])
def analyze_scale():
    """
    Analyze a scale and find compatible chords.
    
    Query parameters:
        root: Root note (e.g., 'C', 'A')
        type: Scale type (e.g., 'major', 'minor_natural', 'dorian')
    
    Returns:
        JSON with scale analysis and compatible chords
    """
    root = request.args.get('root', 'C')
    scale_type = request.args.get('type', 'major')
    
    try:
        scale = Scale(root, scale_type)
        engine = HarmonyEngine()
        
        # Get compatible chords
        compatible = engine.find_compatible_chords(scale)
        diatonic = engine._get_diatonic_chords(scale)
        
        # Format results
        return jsonify({
            'success': True,
            'type': 'scale',
            'scale': {
                'name': scale.name,
                'root': scale.root.name,
                'type': scale.scale_type,
                'notes': scale.note_names,
                'intervals': scale.intervals,
                'degrees': {str(i+1): n.name for i, n in enumerate(scale.notes[:7])},
            },
            'diatonic_chords': diatonic,
            'compatible_chords': format_compatible_chords(compatible),
            'fretboard_positions': format_fretboard_positions(
                engine._get_scale_positions(scale)
            ),
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@bp.route('/compatibility', methods=['GET'])
def check_compatibility():
    """
    Check compatibility between a specific chord and scale.
    
    Query parameters:
        chord_root: Root note of chord
        chord_quality: Quality of chord
        scale_root: Root note of scale
        scale_type: Type of scale
    
    Returns:
        JSON with tonal and modal compatibility analysis
    """
    chord_root = request.args.get('chord_root', 'C')
    chord_quality = request.args.get('chord_quality', 'maj7')
    scale_root = request.args.get('scale_root', 'C')
    scale_type = request.args.get('scale_type', 'major')
    
    try:
        chord = Chord(chord_root, chord_quality)
        scale = Scale(scale_root, scale_type)
        engine = HarmonyEngine()
        
        # Get compatibility analysis
        tonal = engine.tonal_compatibility(chord, scale)
        modal = engine.modal_compatibility(chord, scale)
        
        return jsonify({
            'success': True,
            'chord': chord.name,
            'scale': scale.name,
            'tonal_compatibility': {
                'score': tonal['score'],
                'relationship': tonal['relationship'],
                'root_in_scale': tonal['root_in_scale'],
                'all_tones_in_scale': tonal['all_tones_in_scale'],
            },
            'modal_compatibility': {
                'relationship': modal['modal_relationship'],
                'tension_score': modal['tension_score'],
            },
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@bp.route('/scales/for-chord', methods=['GET'])
def scales_for_chord():
    """
    Get all scales compatible with a chord.
    
    Query parameters:
        root: Root note of chord
        quality: Quality of chord
    
    Returns:
        JSON with list of compatible scales
    """
    root = request.args.get('root', 'C')
    quality = request.args.get('quality', 'maj')
    
    try:
        chord = Chord(root, quality)
        engine = HarmonyEngine()
        
        # Get tonal scales
        tonal_scales = engine.get_tonal_scales(chord)
        
        # Get modal scales
        modal_scales = engine.get_modal_scales(chord)
        
        return jsonify({
            'success': True,
            'chord': chord.name,
            'tonal_scales': format_scales_list(tonal_scales),
            'modal_scales': format_scales_list(modal_scales[:5]),
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@bp.route('/chords/for-scale', methods=['GET'])
def chords_for_scale():
    """
    Get all chords compatible with a scale.
    
    Query parameters:
        root: Root note of scale
        type: Type of scale
    
    Returns:
        JSON with list of compatible chords
    """
    root = request.args.get('root', 'C')
    scale_type = request.args.get('type', 'major')
    
    try:
        scale = Scale(root, scale_type)
        engine = HarmonyEngine()
        
        # Get compatible chords
        chords = engine.find_compatible_chords(scale)
        
        return jsonify({
            'success': True,
            'scale': scale.name,
            'diatonic_chords': chords[:14],  # 7 triads + 7 seventh chords
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


# ==================== Real-time Analysis Endpoints ====================

@bp.route('/realtime/analyze', methods=['POST'])
def realtime_analyze():
    """
    Analyze notes in real-time.
    
    Request body:
        notes: Array of note objects or MIDI numbers
        timeout: Optional timeout in ms (default 500)
    
    Returns:
        JSON with real-time analysis
    """
    data = request.get_json() or {}
    notes_input = data.get('notes', [])
    timeout = data.get('timeout', 500)
    
    if not notes_input:
        return jsonify({
            'success': False,
            'error': 'Please provide notes to analyze'
        }), 400
    
    try:
        engine = HarmonyEngine()
        
        # Parse notes (can be MIDI numbers or note names)
        parsed_notes = _parse_notes(notes_input)
        
        if not parsed_notes:
            return jsonify({
                'success': False,
                'error': 'Could not parse notes'
            }), 400
        
        # Get note information
        note_info = _get_note_info(parsed_notes)
        
        # Try to detect chord
        chord_result = _detect_chord_from_notes(parsed_notes, engine)
        
        # Try to suggest scales
        scale_result = _suggest_scales_from_notes(parsed_notes, engine)
        
        return jsonify({
            'success': True,
            'notes': note_info,
            'detected_chord': chord_result,
            'suggested_scales': scale_result,
            'timeout_ms': timeout,
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@bp.route('/realtime/chord-detect', methods=['POST'])
def detect_chord_from_notes():
    """
    Detect chord from an array of notes.
    
    Request body:
        notes: Array of note names or MIDI numbers
    
    Returns:
        JSON with detected chord information
    """
    data = request.get_json() or {}
    notes_input = data.get('notes', [])
    
    if not notes_input:
        return jsonify({
            'success': False,
            'error': 'Please provide notes'
        }), 400
    
    try:
        engine = HarmonyEngine()
        parsed_notes = _parse_notes(notes_input)
        
        if not parsed_notes:
            return jsonify({
                'success': False,
                'error': 'Could not parse notes'
            }), 400
        
        result = _detect_chord_from_notes(parsed_notes, engine)
        
        return jsonify({
            'success': True,
            'result': result,
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@bp.route('/realtime/scale-suggest', methods=['POST'])
def suggest_scales_from_notes():
    """
    Suggest scales from an array of notes.
    
    Request body:
        notes: Array of note names or MIDI numbers
    
    Returns:
        JSON with suggested scales
    """
    data = request.get_json() or {}
    notes_input = data.get('notes', [])
    
    if not notes_input:
        return jsonify({
            'success': False,
            'error': 'Please provide notes'
        }), 400
    
    try:
        engine = HarmonyEngine()
        parsed_notes = _parse_notes(notes_input)
        
        if not parsed_notes:
            return jsonify({
                'success': False,
                'error': 'Could not parse notes'
            }), 400
        
        result = _suggest_scales_from_notes(parsed_notes, engine)
        
        return jsonify({
            'success': True,
            'scales': result,
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ==================== Helper Functions ====================

def format_chord_result(result):
    """Format chord analysis result for JSON response."""
    tonal = result.get('compatible_scales', {}).get('tonal_scales', [])
    modal = result.get('compatible_scales', {}).get('modal_scales', [])
    
    return {
        'success': True,
        'type': 'chord',
        'input': result.get('name'),
        'chord': {
            'name': result['name'],
            'root': result['root'],
            'quality': result['quality'],
            'notes': result['notes'],
            'intervals': result['intervals'],
        },
        'tonal_scales': format_scales_list(tonal),
        'modal_scales': format_scales_list(modal[:5]),
        'fretboard_positions': format_fretboard_positions(result.get('fretboard_positions', {})),
    }


def format_scale_result(result):
    """Format scale analysis result for JSON response."""
    return {
        'success': True,
        'type': 'scale',
        'input': result.get('name'),
        'scale': {
            'name': result['name'],
            'root': result['root'],
            'type': result['scale_type'],
            'notes': result['notes'],
            'intervals': result['intervals'],
            'degrees': result.get('degrees', {}),
        },
        'diatonic_chords': result.get('diatonic_chords', []),
        'compatible_chords': format_compatible_chords(
            result.get('compatible_chords', [])[:14]
        ),
        'fretboard_positions': format_fretboard_positions(result.get('fretboard_positions', {})),
    }


def format_compatible_scales(compatible):
    """Format compatible scales for JSON response."""
    return {
        'tonal': format_scales_list(compatible.get('tonal_scales', [])),
        'modal': format_scales_list(compatible.get('modal_scales', [])[:5]),
    }


def format_scales_list(scales):
    """Format a list of scales for JSON response."""
    result = []
    for item in scales:
        if isinstance(item, dict):
            scale = item.get('scale')
            if scale:
                result.append({
                    'name': scale.name,
                    'root': scale.root.name,
                    'type': scale.scale_type,
                    'notes': scale.note_names,
                    'score': item.get('compatibility', {}).get('score', 
                           item.get('modal_compatibility', {}).get('tension_score', 100)),
                })
        elif hasattr(item, 'name'):
            result.append({
                'name': item.name,
                'root': item.root.name,
                'type': item.scale_type,
                'notes': item.note_names,
            })
    return result


def format_compatible_chords(chords):
    """Format compatible chords for JSON response."""
    result = []
    for item in chords:
        if isinstance(item, dict):
            chord = item.get('chord')
            if chord:
                result.append({
                    'name': chord.name,
                    'root': chord.root.name,
                    'quality': chord.quality,
                    'notes': chord.note_names,
                    'degree': item.get('degree'),
                    'function': item.get('function', ''),
                })
        elif hasattr(item, 'name'):
            result.append({
                'name': item.name,
                'root': item.root.name,
                'quality': item.quality,
                'notes': item.note_names,
            })
    return result


def format_fretboard_positions(positions):
    """Format fretboard positions for JSON response."""
    if not positions:
        return {}
    
    formatted = {}
    for note, pos_list in positions.items():
        formatted[note] = [
            {'string': p['string'], 'fret': p['fret']}
            for p in pos_list
        ]
    return formatted


# ==================== Real-time Analysis Helper Functions ====================

def _get_note_class():
    """Get Note class with proper imports."""
    from music_engine.models.note import Note
    return Note


def _parse_notes(notes_input):
    """
    Parse notes from various input formats.
    
    Args:
        notes_input: List of MIDI numbers, note names, or note objects
        
    Returns:
        List of Note objects
    """
    Note = _get_note_class()
    
    parsed = []
    
    for note_input in notes_input:
        if isinstance(note_input, int):
            # MIDI number
            note = Note.from_midi(note_input)
            if note:
                parsed.append(note)
        elif isinstance(note_input, str):
            # Note name (e.g., "C4", "C#", "Db")
            try:
                note = Note(note_input)
                parsed.append(note)
            except:
                # Try parsing as MIDI
                try:
                    note = Note.from_midi(int(note_input))
                    if note:
                        parsed.append(note)
                except:
                    pass
        elif isinstance(note_input, dict):
            # Note object with 'name' or 'midi' key
            if 'midi' in note_input:
                note = Note.from_midi(note_input['midi'])
                if note:
                    parsed.append(note)
            elif 'name' in note_input:
                try:
                    note = Note(note_input['name'])
                    parsed.append(note)
                except:
                    pass
    
    return parsed


def _get_note_info(notes):
    """
    Get detailed information about notes.
    
    Args:
        notes: List of Note objects
        
    Returns:
        List of note information dictionaries
    """
    return [{
        'name': note.name,
        'name_with_octave': note.name,  # Note.name already includes octave
        'midi': note.midi,
        'frequency': round(note.frequency, 2),
        'octave': note.octave,
        'semitone': note.semitone,
    } for note in notes]


def _detect_chord_from_notes(notes, engine):
    """
    Detect chord from an array of notes.
    
    Args:
        notes: List of Note objects
        engine: HarmonyEngine instance
        
    Returns:
        Dictionary with detected chord information
    """
    Note = _get_note_class()
    
    if len(notes) < 3:
        return {
            'detected': False,
            'reason': 'Need at least 3 notes to detect chord',
            'notes': [n.name for n in notes],
        }
    
    # Get unique semitones (within one octave)
    semitones = sorted(set(n.semitone % 12 for n in notes))
    
    # Try to match against known chord patterns
    chord_patterns = {
        # Major triads
        (0, 4, 7): ('maj', 'Major'),
        # Minor triads
        (0, 3, 7): ('min', 'Minor'),
        # Diminished triads
        (0, 3, 6): ('dim', 'Diminished'),
        # Augmented triads
        (0, 4, 8): ('aug', 'Augmented'),
        # Major 7th
        (0, 4, 7, 11): ('maj7', 'Major 7th'),
        # Dominant 7th
        (0, 4, 7, 10): ('dom7', 'Dominant 7th'),
        # Minor 7th
        (0, 3, 7, 10): ('min7', 'Minor 7th'),
        # Diminished 7th
        (0, 3, 6, 9): ('dim7', 'Diminished 7th'),
        # Half-diminished
        (0, 3, 6, 10): ('min7b5', 'Half-Diminished'),
        # Suspended 2nd
        (0, 2, 7): ('sus2', 'Suspended 2nd'),
        # Suspended 4th
        (0, 5, 7): ('sus4', 'Suspended 4th'),
        # 6th chords
        (0, 4, 7, 9): ('6', 'Major 6th'),
        (0, 3, 7, 9): ('min6', 'Minor 6th'),
    }
    
    # Try to find matching pattern
    for pattern, (quality, quality_name) in chord_patterns.items():
        if _pattern_matches(semitones, pattern):
            # Found a match, now determine the root
            root_semitone = pattern[0]
            
            # Find the actual root in the played notes
            possible_roots = [n.semitone % 12 for n in notes]
            
            # Try each note as potential root
            for root_semitone in possible_roots:
                # Calculate intervals from this root
                intervals = tuple(sorted((s - root_semitone) % 12 for s in semitones))
                
                if intervals == pattern or intervals == _normalize_pattern(pattern):
                    # Found the root
                    root_note = Note.from_midi(60 + root_semitone)
                    
                    try:
                        chord = Chord(root_note.name.replace('b', '#').replace('#b', '').replace('##', '#'), quality)
                        
                        # Check how many notes match
                        chord_semitones = set(chord.semitones)
                        played_semitones = set(semitones)
                        match_count = len(chord_semitones.intersection(played_semitones))
                        
                        return {
                            'detected': True,
                            'chord': chord.name,
                            'root': chord.root.name,
                            'quality': quality,
                            'quality_name': quality_name,
                            'notes': chord.note_names,
                            'intervals': chord.intervals,
                            'match_score': match_count / len(chord_semitones) * 100,
                            'inversion': _detect_inversion(notes, chord),
                        }
                    except:
                        pass
    
    # Try with different root positions (inversions)
    for i in range(len(semitones)):
        rotated = tuple(sorted(((s - semitones[i]) % 12 for s in semitones)))
        for pattern, (quality, quality_name) in chord_patterns.items():
            if rotated == pattern:
                root_note = Note.from_midi(60 + semitones[i])
                try:
                    chord = Chord(root_note.name.replace('b', '#').replace('#b', '').replace('##', '#'), quality)
                    return {
                        'detected': True,
                        'chord': chord.name,
                        'root': chord.root.name,
                        'quality': quality,
                        'quality_name': quality_name,
                        'notes': chord.note_names,
                        'intervals': chord.intervals,
                        'match_score': 100,
                        'inversion': i,
                    }
                except:
                    pass
    
    return {
        'detected': False,
        'reason': 'Could not identify chord pattern',
        'semitones': semitones,
        'note_names': [n.name for n in notes],
    }


def _pattern_matches(played, pattern):
    """Check if played notes match a pattern."""
    return set(played) == set(pattern)


def _normalize_pattern(pattern):
    """Normalize a chord pattern to start from 0."""
    return tuple((p - pattern[0]) % 12 for p in pattern)


def _detect_inversion(notes, chord):
    """Detect chord inversion from played notes."""
    Note = _get_note_class()
    
    if len(notes) < 3:
        return 0
    
    # Get bass note (lowest)
    bass_midi = min(n.midi for n in notes)
    bass_note = Note.from_midi(bass_midi)
    
    # Check if bass matches chord root
    if bass_note.semitone % 12 == chord.root.semitone:
        return 0  # Root position
    
    # Check inversions
    chord_notes_sorted = sorted(chord.semitones)
    bass_semitone = bass_note.semitone % 12
    
    for i, note in enumerate(chord_notes_sorted):
        if bass_semitone == note:
            return i
    
    return 0


def _suggest_scales_from_notes(notes, engine):
    """
    Suggest scales based on played notes.
    
    Args:
        notes: List of Note objects
        engine: HarmonyEngine instance
        
    Returns:
        List of suggested scales with match scores
    """
    if not notes:
        return []
    
    # Get unique semitones
    semitones = set(n.semitone % 12 for n in notes)
    
    # Get all note names
    note_names = [n.name for n in notes]
    
    results = []
    
    # Try common scale types
    scale_types = ['major', 'minor_natural', 'dorian', 'mixolydian', 'lydian', 
                  'pentatonic_major', 'pentatonic_minor', 'blues_minor']
    
    for root in ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']:
        for scale_type in scale_types:
            try:
                scale = Scale(root, scale_type)
                scale_semitones = set(scale.semitones)
                
                # Calculate match score
                matching = len(semitones.intersection(scale_semitones))
                score = (matching / len(semitones)) * 100 if semitones else 0
                
                # Add scale if there's a reasonable match
                if score >= 30:
                    # Check if it's a proper match
                    results.append({
                        'scale': scale.name,
                        'root': root,
                        'type': scale_type,
                        'notes': scale.note_names,
                        'match_score': round(score, 1),
                        'matching_notes': list(semitones.intersection(scale_semitones)),
                    })
            except:
                continue
    
    # Sort by score and return top results
    results.sort(key=lambda x: x['match_score'], reverse=True)
    
    # Remove duplicates and return top 10
    seen = set()
    unique_results = []
    for r in results:
        key = (r['root'], r['type'])
        if key not in seen:
            seen.add(key)
            unique_results.append(r)
    
    return unique_results[:10]

