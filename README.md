# Music Theory Engine

[![Tests](https://github.com/blackboxai/music-theory-engine/actions/workflows/test.yml/badge.svg)](https://github.com/blackboxai/music-theory-engine/actions/workflows/test.yml)
[![Coverage](https://codecov.io/gh/blackboxai/music-theory-engine/branch/main/graph/badge.svg)](https://codecov.io/gh/blackboxai/music-theory-engine)
[![Python Version](https://img.shields.io/pypi/pyversions/music-theory-engine.svg)](https://pypi.org/project/music-theory-engine/)

A comprehensive Python library and web application for music theory analysis, composition, and education.

## Features

- **Scale Explorer**: Browse and analyze musical scales with interactive visualizations
- **Chord Builder**: Create and explore chord structures with detailed interval information
- **Progression Analyzer**: Analyze and generate chord progressions
- **Learn Music Theory**: Educational content inspired by Open Music Theory
- **Fretboard Visualization**: Interactive guitar fretboard display
- **Harmony Analyzer**: Real-time harmonic analysis with virtual keyboard
- **MIDI Support**: Generate and export MIDI files
- **Integration Adapters**: Connect with music21 and mingus libraries

## Installation

```bash
# Clone the repository
git clone https://github.com/blackboxai/music-theory-engine.git
cd music-theory-engine

# Install dependencies
pip install -r music_engine/requirements.txt

# For the web app
pip install flask
```

## Usage

### Web Application

```bash
cd web_app
python app.py
```

Then open your browser at http://127.0.0.1:5000

### Library Usage

```python
from music_engine.models import Note, Chord, Scale

# Create a note
note = Note("C4")

# Create a chord
chord = Chord("Cmaj7")

# Create a scale
scale = Scale("C", "major")

# Get chord tones
print(chord.notes)  # ['C4', 'E4', 'G4', 'B4']

# Get scale degrees
print(scale.notes)  # ['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4']
```

## Web App Pages

- **/** - Home dashboard
- **/learn** - Learn Music Theory (educational content)
- **/scales** - Scale Explorer
- **/chords** - Chord Builder
- **/progressions** - Progression Analyzer
- **/fretboard** - Guitar Fretboard Visualization
- **/realtime** - Real-time analysis with virtual keyboard

## Project Structure

```
music-theory-engine/
├── music_engine/       # Core library
│   ├── core/          # Music theory core (chords, scales, intervals)
│   ├── models/        # Data models (Note, Chord, Scale, Progression)
│   ├── integrations/  # Third-party integrations (music21, mingus)
│   ├── orchestrator/  # Composition and analysis orchestration
│   ├── audio/         # Audio synthesis and MIDI rendering
│   └── tests/        # Unit tests
├── web_app/           # Flask web application
│   ├── api/          # REST API endpoints
│   ├── templates/    # HTML templates
│   └── static/       # CSS and JavaScript
└── presets/           # Musical presets
```

## API Endpoints

- `/api/scales` - Scale information and analysis
- `/api/chords` - Chord building and information
- `/api/progressions` - Chord progression tools
- `/api/analysis` - Harmonic analysis
- `/api/midi` - MIDI file generation
- `/api/orchestrator` - Advanced composition tools
- `/api/circle` - Circle of Fifths utilities

## Technologies

- **Python 3.8+**
- **Flask** - Web framework
- **music21** - Music notation library
- **mingus** - Music theory library
- **Web Audio API** - Browser-based audio synthesis

## Testing

```bash
# Run all tests
pytest music_engine/tests/ -v

# Run specific test file
pytest music_engine/tests/test_models.py -v
```

## License

Licensed under the Apache License, Version 2.0. See the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Author

Music Theory Engine - 2024
