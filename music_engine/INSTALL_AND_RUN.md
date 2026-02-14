# 🎵 Music Theory Engine - Installation & Usage Guide

## 📦 Installation

### Option 1: Run as Python Application (Recommended for Development)

#### Prerequisites
- Python 3.8 or higher
- pip package manager

#### Install Dependencies
```bash
# Navigate to the music_engine directory
cd music_engine

# Install required packages
pip install -r requirements.txt
```

#### Run the GUI Application
```bash
# Run the graphical interface
python main_gui.py
```

### Option 2: Build Standalone Executable (.exe)

#### Prerequisites
- Python 3.8 or higher
- PyInstaller (included in requirements.txt)

#### Build the Executable
```bash
# Navigate to the music_engine directory
cd music_engine

# Install dependencies (including PyInstaller)
pip install -r requirements.txt

# Build the executable
python build_exe.py
```

#### Run the Executable
```bash
# The executable will be created in the 'dist' folder
# Double-click MusicTheoryEngine.exe to run
dist/MusicTheoryEngine.exe

# Or use the batch file for convenience
dist/Run_Music_Theory_Engine.bat
```

## 🎯 Features Overview

### Scale Explorer
- **Select root note**: Choose from C, C#, D, Eb, E, F, F#, G, Ab, A, Bb, B
- **Choose scale type**: Major, Minor, Modal, Pentatonic, Blues scales
- **View details**: Notes, intervals, scale degrees, compatible chords
- **Export results**: Save scale information to text file

### Chord Builder
- **Select root note**: Same note selection as scales
- **Choose chord quality**: Triads, 7ths, extended chords, suspensions
- **View inversions**: Root position, 1st, 2nd, 3rd inversions
- **Guitar voicings**: Suggestions for guitar playing
- **Extensions**: Possible chord extensions and alterations

### Progression Analyzer
- **Enter chord progression**: Type chords like "C F G C"
- **Automatic analysis**: Key detection, complexity assessment
- **Scale suggestions**: Compatible scales for improvisation
- **Load examples**: Pre-built common progressions
- **Export analysis**: Save detailed progression analysis

### Arpeggio Viewer
- **Choose source**: Create arpeggios from chords or scales
- **Select direction**: Up, Down, Up-Down, Down-Up patterns
- **Set octaves**: 1-3 octave ranges
- **Guitar techniques**: Playing tips and technique suggestions
- **Note sequence**: Visual display of arpeggio patterns

## 🎸 Usage Tips for Guitarists

### Scale Practice
1. Choose a root note and scale type
2. Practice the notes in order
3. Use the scale degrees to understand positions
4. Try compatible chords within the scale

### Chord Learning
1. Start with basic triads (Major, Minor, Diminished)
2. Progress to 7th chords (dom7, maj7, min7)
3. Experiment with inversions for smoother voice leading
4. Use guitar voicing suggestions for playability

### Improvisation
1. Analyze a chord progression
2. Choose suggested scales for improvisation
3. Practice arpeggios from the chord tones
4. Experiment with different directions and octaves

### Technique Development
1. Use arpeggio viewer for finger independence
2. Practice alternate picking with up/down patterns
3. Work on sweep picking for fast passages
4. Focus on smooth position shifts

## 🛠️ Troubleshooting

### GUI Won't Start
```
Error: ModuleNotFoundError: No module named 'customtkinter'
```
**Solution**: Install dependencies
```bash
pip install -r requirements.txt
```

### Executable Build Fails
```
Error: PyInstaller not found
```
**Solution**: Install PyInstaller
```bash
pip install pyinstaller
```

### Application Runs but GUI is Blank
**Solution**: Check Python version (requires 3.8+)
```bash
python --version
```

### Export Function Doesn't Work
**Solution**: Check write permissions in current directory
- Try running as administrator (Windows)
- Choose a different export location

## 📁 Project Structure

```
music_engine/
├── core/                    # Music theory logic
│   ├── notes.py            # Note system
│   ├── scales.py           # Scale construction
│   ├── chords.py           # Chord construction
│   ├── arpeggios.py        # Arpeggio generation
│   └── progressions.py     # Progression analysis
├── models/                 # Data models
│   ├── note.py             # Note class
│   ├── chord.py            # Chord class
│   ├── scale.py            # Scale class
│   ├── arpeggio.py         # Arpeggio class
│   └── progression.py      # Progression class
├── gui/                    # Graphical interface
│   ├── main_window.py      # Main GUI window
│   ├── scale_explorer.py   # Scale exploration tab
│   ├── chord_builder.py    # Chord building tab
│   ├── progression_analyzer.py # Progression analysis tab
│   └── arpeggio_viewer.py  # Arpeggio viewing tab
├── utils/                  # Utilities
│   ├── constants.py        # Music theory constants
│   ├── music_math.py       # Mathematical functions
│   └── validators.py       # Input validation
├── examples/               # Usage examples
├── tests/                  # Unit tests
├── main_gui.py             # GUI launcher
├── build_exe.py            # Executable builder
├── setup.py               # Package setup
├── requirements.txt        # Dependencies
├── README.md              # Documentation
└── demo.py                # Command-line demo
```

## 🎵 Music Theory Resources

### Built-in Scale Types
- **Major**: Ionian mode
- **Minor**: Natural, Harmonic, Melodic
- **Modal**: Dorian, Phrygian, Lydian, Mixolydian, Locrian
- **Pentatonic**: Major and Minor
- **Blues**: Major and Minor blues scales
- **Special**: Whole tone, Chromatic, Diminished, Augmented

### Supported Chord Types
- **Triads**: Major, Minor, Diminished, Augmented
- **7th Chords**: Dominant, Major, Minor, Diminished
- **Extended**: 9, 11, 13 and variations
- **Added Tone**: 6, 6/9, sus2, sus4
- **Altered**: 7♭9, 7♯11

### Arpeggio Patterns
- **Directions**: Up, Down, Up-Down, Down-Up
- **Sources**: Any chord or scale
- **Ranges**: 1-3 octaves
- **Techniques**: Alternate picking, sweep picking, economy picking

## 🔧 Advanced Configuration

### Custom Icon
To add a custom icon to the executable:
1. Create an `icon.ico` file (256x256 recommended)
2. Place it in the `music_engine` directory
3. Run `build_exe.py`

### Theme Customization
The GUI uses CustomTkinter with a dark theme by default. To change:
```python
import customtkinter as ctk
ctk.set_appearance_mode("light")  # or "dark"
ctk.set_default_color_theme("green")  # blue, green, dark-blue
```

### Development Mode
For development and testing:
```bash
# Run tests
python demo.py

# Run GUI in development mode
python main_gui.py
```

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Verify Python version (3.8+)
3. Ensure all dependencies are installed
4. Try running the demo script first
5. Check the console output for error messages

## 🎼 Musical Applications

This engine is perfect for:
- **Music Students**: Learn theory interactively
- **Guitarists**: Improve technique and improvisation
- **Composers**: Analyze and create progressions
- **Teachers**: Demonstrate music concepts visually
- **Developers**: Build music applications

## 📈 Future Enhancements

Potential additions:
- MIDI file import/export
- Audio playback of scales/chords/arpeggios
- Guitar tablature generation
- MusicXML support
- Real-time guitar input analysis
- AI-powered composition suggestions

---

**🎸 Enjoy exploring music theory with your new digital companion!**
