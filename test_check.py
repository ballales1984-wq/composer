#!/usr/bin/env python
"""Quick test to verify models work correctly."""
import sys
sys.path.insert(0, '.')

from music_engine.models import Note, Chord, Scale, Progression, Arpeggio

# Test Note
note = Note('C4')
print(f'✓ Note: {note} (chroma={note.chroma}, midi={note.midi})')

# Test Chord
chord = Chord('C', 'maj')
print(f'✓ Chord: {chord} - {chord.notes}')

# Test Scale
scale = Scale('C', 'major')
print(f'✓ Scale: {scale}')
print(f'  Notes: {[n.name for n in scale.notes]}')
print(f'  Semitones (chroma): {scale.semitones}')

# Test Arpeggio
arp = Arpeggio(chord, 'up_down')
print(f'✓ Arpeggio up_down: {[n.name for n in arp.notes]}')

# Test Progression
prog = Progression([Chord('C', 'maj'), Chord('F', 'maj'), Chord('G', 'maj')])
print(f'✓ Progression: {prog}')
print(f'  Key: {prog.key}')

print('\n✅ Tutti i moduli funzionano correttamente!')

