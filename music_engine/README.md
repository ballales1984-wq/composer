# 🎵 Music Theory Engine

A comprehensive Python library for music theory analysis designed specifically for guitarists and musicians. This engine provides tools for scale construction, chord analysis, arpeggio generation, and harmonic progression analysis.

## ✨ Features

### 🎼 Scale Construction
- **Major & Minor Scales**: Natural, harmonic, and melodic minors
- **Modal Scales**: Dorian, Phrygian, Lydian, Mixolydian, Locrian
- **Pentatonic Scales**: Major and minor pentatonic
- **Blues Scales**: Major and minor blues scales
- **Special Scales**: Whole tone, diminished, augmented, chromatic

### 🎸 Chord Construction
- **Triads**: Major, minor, diminished, augmented
- **Seventh Chords**: Major 7, dominant 7, minor 7, diminished 7, minor 7♭5
- **Extended Chords**: 9, 11, 13 and their variations
- **Added Tone Chords**: 6, 6/9, suspended 2nd/4th
- **Chord Inversions**: Full support for all inversions

### 🎶 Arpeggio Generation
- **Triad Arpeggios**: All directions (up, down, up-down, down-up)
- **Seventh Arpeggios**: From any seventh chord
- **Scale Arpeggios**: Full scale runs as arpeggios
- **Custom Patterns**: Build your own arpeggio patterns

### 🎼 Harmonic Analysis
- **Progression Analysis**: Key detection and harmonic function
- **Scale Compatibility**: Find scales that work over progressions
- **Roman Numeral Analysis**: Convert progressions to Roman numerals
- **Cadence Detection**: Identify authentic, plagal, and deceptive cadences

## 🚀 Quick Start

### Installation
```bash
# Clone the repository
git clone <repository-url>
cd music_engine

# Install dependencies (if any)
pip install -r requirements.txt
```

### Basic Usage

```python
from music_engine.core import scales, chords, arpeggios, progressions

# Create a scale
c_major = scales.major('C')
print(f"C Major: {[n.name for n in c_major.notes]}")
# Output: C Major: ['C', 'D', 'E', 'F', 'G', 'A', 'B']

# Create a chord
g_dom7 = chords.dominant7('G')
print(f"G7: {[n.name for n in g_dom7.notes]}")
# Output: G7: ['G', 'B', 'D', 'F']

# Build an arpeggio
c_maj_arp = arpeggios.major_triad('C', 'up')
print(f"C Major arpeggio: {[n.name for n in c_maj_arp.notes]}")
# Output: C Major arpeggio: ['C', 'E', 'G']

# Analyze a progression
prog = progressions.analyze(['C', 'F', 'G', 'C'])
scales_for_prog = progressions.suggest_scales(['C', 'F', 'G', 'C'], 3)
print(f"Suggested scales: {[str(s) for s in scales_for_prog]}")
```

## 📖 Documentation

### Scale Types
```python
# Major scales
c_major = scales.major('C')
ionian = scales.ionian('C')  # Same as major

# Minor scales
a_natural = scales.minor('A', 'natural')
a_harmonic = scales.minor('A', 'harmonic')
a_melodic = scales.minor('A', 'melodic')

# Modal scales
d_dorian = scales.dorian('D')
e_phrygian = scales.phrygian('E')
f_lydian = scales.lydian('F')
g_mixolydian = scales.mixolydian('G')
a_locrian = scales.locrian('A')

# Pentatonic scales
a_pent_minor = scales.pentatonic_minor('A')
c_pent_major = scales.pentatonic_major('C')

# Blues scales
a_blues = scales.blues_minor('A')
c_blues_maj = scales.blues_major('C')
```

### Chord Types
```python
# Triads
c_maj = chords.major('C')
d_min = chords.minor('D')
eb_dim = chords.diminished('Eb')
f_aug = chords.augmented('F')

# Seventh chords
g7 = chords.dominant7('G')
f_maj7 = chords.major7('F')
a_min7 = chords.minor7('A')
b_dim7 = chords.diminished7('B')
g_min7b5 = chords.minor7b5('G')

# Extended chords
c9 = chords.dom9('C')
d_min9 = chords.min9('D')
f_maj11 = chords.major11('F')
bb_min13 = chords.min13('Bb')
```

### Arpeggio Patterns
```python
# Triad arpeggios
c_maj_arp = arpeggios.major_triad('C', 'up')
d_min_arp = arpeggios.minor_triad('D', 'up_down')

# Seventh arpeggios
g7_arp = arpeggios.dominant7('G', 'up')
f_maj7_arp = arpeggios.major7('F', 'down')

# Scale arpeggios
a_minor_arp = arpeggios.minor_scale('A', 'up')
c_blues_arp = arpeggios.blues_scale('C', 'up_down')
```

### Progression Analysis
```python
# Analyze a progression
progression = progressions.analyze(['C', 'F', 'G', 'C'])
print(f"Key: {progression.key_name}")
print(f"All notes: {sorted([n.name for n in progression.all_notes])}")

# Find compatible scales
compatible = progressions.find_scales(['C', 'F', 'G', 'C'])
print(f"Compatible scales: {len(compatible)} found")

# Get scale suggestions for improvisation
suggestions = progressions.suggest_scales(['Cmaj7', 'Dm7', 'G7', 'Cmaj7'], 5)
for scale in suggestions:
    print(f"  - {scale}")
```

## 🏗️ Architecture

The engine is built with a modular architecture:

```
music_engine/
├── core/           # Business logic (scales, chords, arpeggios, progressions)
├── models/         # Data models (Note, Chord, Scale, Arpeggio, Progression)
├── utils/          # Utilities (constants, math helpers, validators)
├── analysis/       # Advanced analysis algorithms
├── tests/          # Unit tests
├── examples/       # Usage examples
└── docs/           # Documentation
```

### Design Principles
- **Separation of Concerns**: Logic separated from data models
- **Extensibility**: Easy to add new scales, chords, and features
- **Music Theory Accuracy**: Based on proper music theory principles
- **Guitar-Friendly**: Designed with guitarists' needs in mind
- **Educational**: Clear, documented code for learning music theory

## 🎸 Guitar-Specific Features

### Chord Voicings
```python
c_maj = chords.major('C')
voicing = c_maj.get_voicing(octave=4)
# Returns guitar-friendly voicing positions
```

### Arpeggio Positions
```python
c_arp = arpeggios.major_triad('C', 'up')
positions = c_arp.get_guitar_positions()
# Returns string/fret positions for guitar
```

### Scale Patterns
```python
c_major = scales.major('C')
# Access scale degrees for guitar patterns
third_degree = c_major.get_degree(3)  # Returns E
```

## 🧪 Testing

Run the test suite:
```bash
python -m pytest tests/
```

Run the basic demo:
```python
python examples/basic_usage.py
```

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for new features
4. Ensure all tests pass
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🎵 Music Theory Resources

- [Music Theory for Guitarists](https://www.musictheoryforguitar.com/)
- [Open Music Theory](https://viva.pressbooks.pub/openmusictheory/)
- [Teoria](https://github.com/saebekassebil/teoria) - JavaScript music theory library

## 🙏 Acknowledgments

- Built for guitarists and musicians who want to understand music theory
- Inspired by the need for accurate, programmatic music analysis
- Designed to be both educational and practical

---

**🎸 Happy playing and coding!**
