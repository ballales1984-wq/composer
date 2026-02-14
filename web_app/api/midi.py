"""MIDI API Blueprint
REST API endpoints for MIDI import/export operations.
"""
import sys
import os
import io
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Blueprint, jsonify, request, send_file
from music_engine.models import Scale, Chord

bp = Blueprint('midi', __name__, url_prefix='/api/midi')

def _get_midi_library():
    try:
        import music21
        return 'music21'
    except ImportError:
        pass
    try:
        import mido
        return 'mido'
    except ImportError:
        return None

def _create_midi_fallback(notes, tempo=120, simultaneous=False):
    header = b'MThd'
    header += (6).to_bytes(4, 'big')
    header += (0).to_bytes(2, 'big')
    header += (1).to_bytes(2, 'big')
    header += (480).to_bytes(2, 'big')
    track = b'MTrk'
    track_data = bytearray()
    microseconds = int(60000000 / tempo)
    track_data.extend([0x00, 0xFF, 0x51, 0x03])
    track_data.extend(microseconds.to_bytes(3, 'big'))
    note_map = {'C':60,'C#':61,'Db':61,'D':62,'D#':63,'Eb':63,'E':64,'F':65,'F#':66,'Gb':66,'G':67,'G#':68,'Ab':68,'A':69,'A#':70,'Bb':70,'B':71}
    parsed = []
    for note in notes:
        if isinstance(note, str):
            octave, note_name = 4, note
            if len(note) > 1 and note[-1].isdigit():
                note_name, octave = note[:-1], int(note[-1])
            if note_name in note_map:
                parsed.append(note_map[note_name] + (octave - 4) * 12)
    time = 0
    if simultaneous and parsed:
        for midi in parsed: track_data.extend([0, 0x90, midi, 64])
        time = 480
        for midi in parsed: track_data.extend([time, 0x80, midi, 0]); time = 0
    else:
        for midi in parsed:
            track_data.extend([time, 0x90, midi, 64]); time = 240
            track_data.extend([time, 0x80, midi, 0]); time = 0
    track_data.extend([0x00, 0xFF, 0x2F, 0x00])
    track += len(track_data).to_bytes(4, 'big') + bytes(track_data)
    return header + track

@bp.route('/status', methods=['GET'])
def get_status():
    return jsonify({'success': True, 'library': _get_midi_library(), 'available': _get_midi_library() is not None})

@bp.route('/export/scale', methods=['GET'])
def export_scale_midi():
    root = request.args.get('root', 'C')
    scale_type = request.args.get('type', 'major')
    octaves = int(request.args.get('octaves', 1))
    try:
        scale = Scale(root, scale_type, octaves)
        note_names = [n.name + str(n.octave) for n in scale.notes]
        midi_data = _create_midi_fallback(note_names, tempo=120)
        return send_file(io.BytesIO(midi_data), mimetype='audio/midi', as_attachment=True, download_name=root + '_' + scale_type + '_scale.mid')
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@bp.route('/export/chord', methods=['GET'])
def export_chord_midi():
    root = request.args.get('root', 'C')
    quality = request.args.get('quality', 'maj')
    try:
        chord = Chord(root, quality)
        note_names = [n.name + str(n.octave) for n in chord.notes]
        midi_data = _create_midi_fallback(note_names, tempo=120, simultaneous=True)
        return send_file(io.BytesIO(midi_data), mimetype='audio/midi', as_attachment=True, download_name=root + '_' + quality + '_chord.mid')
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@bp.route('/frequencies', methods=['GET'])
def get_frequencies():
    octave = int(request.args.get('octave', 4))
    return jsonify({'success': True, 'octave': octave, 'frequencies': {n: round(440*2**(((octave+1)*12+i-69)/12),2) for i,n in enumerate(['C','C#','D','D#','E','F','F#','G','G#','A','A#','B'])}})
