# 🤝 Contributing to Music Theory Engine

We welcome contributions! This document provides guidelines for contributing to the Music Theory Engine project.

## 📋 Table of Contents
- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [How to Contribute](#how-to-contribute)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)

## 🤟 Code of Conduct

This project follows a code of conduct to ensure a welcoming environment for all contributors. By participating, you agree to:
- Be respectful and inclusive
- Focus on constructive feedback
- Accept responsibility for mistakes
- Show empathy towards other contributors

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Git
- Basic knowledge of music theory (helpful but not required)

### Development Setup

1. **Fork the repository** on GitHub
2. **Clone your fork**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/music-theory-engine.git
   cd music-theory-engine
   ```

3. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   pip install -e .  # Install in development mode
   ```

5. **Run the application**:
   ```bash
   python app_standalone.py
   ```

## 🛠️ How to Contribute

### Types of Contributions
- 🐛 **Bug fixes** - Fix existing issues
- ✨ **New features** - Add new functionality
- 📚 **Documentation** - Improve docs or add examples
- 🎨 **UI/UX improvements** - Enhance user interface
- 🧪 **Tests** - Add or improve test coverage
- 🔧 **Code quality** - Refactor or optimize code

### Finding Issues
- Check the [Issues](../../issues) tab on GitHub
- Look for issues labeled `good first issue` or `help wanted`
- Comment on issues to indicate you're working on them

## 📝 Coding Standards

### Python Style Guide
We follow PEP 8 with some modifications:
- Use 4 spaces for indentation
- Line length: 100 characters
- Use type hints where possible
- Write descriptive docstrings

### Naming Conventions
```python
# Classes
class MusicTheoryEngine:
    pass

# Functions and methods
def calculate_scale_notes():
    pass

# Variables
scale_notes = []
current_bpm = 120

# Constants
MAX_BPM = 200
DEFAULT_TUNING = "Standard"
```

### Commit Messages
Use clear, descriptive commit messages:
```
feat: add chord progression analysis feature
fix: resolve thread-safety issue in scale builder
docs: update installation instructions
refactor: improve error handling in audio module
```

### Code Structure
```
music_engine/
├── app_standalone.py      # Main application
├── core/                  # Core music logic
├── gui/                   # GUI components
├── models/               # Data models
├── utils/                # Utilities
└── tests/                # Test files
```

## 🧪 Testing

### Running Tests
```bash
# Run all tests
python -m pytest

# Run specific test file
python -m pytest tests/test_scales.py

# Run with coverage
python -m pytest --cov=music_engine
```

### Writing Tests
- Use `pytest` framework
- Place tests in `tests/` directory
- Name test files as `test_*.py`
- Use descriptive test function names

```python
def test_major_scale_generation():
    """Test that major scales are generated correctly."""
    scale = ScaleBuilder.major("C")
    expected_notes = ["C4", "D4", "E4", "F4", "G4", "A4", "B4"]
    assert scale.notes == expected_notes
```

## 📤 Submitting Changes

### Pull Request Process

1. **Create a branch** for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following the coding standards

3. **Add tests** for new functionality

4. **Update documentation** if needed

5. **Commit your changes**:
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

6. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request**:
   - Go to the original repository
   - Click "New Pull Request"
   - Select your branch
   - Fill out the PR template
   - Wait for review

### PR Checklist
- [ ] Code follows style guidelines
- [ ] Tests pass locally
- [ ] Documentation updated
- [ ] Commit messages are clear
- [ ] PR description explains changes
- [ ] No merge conflicts

## 🎯 Areas for Contribution

### High Priority
- **Audio improvements** - Better sound synthesis
- **MIDI export** - Export musical content to MIDI
- **Keyboard input** - Play notes with computer keyboard
- **Chord diagrams** - Visual guitar chord diagrams

### Medium Priority
- **Additional scales** - More exotic scales
- **Rhythm exercises** - Interactive rhythm training
- **MusicXML import/export** - Standard music notation
- **Chord progressions database** - More progression examples

### Low Priority
- **Themes** - Additional UI themes
- **Internationalization** - Multiple language support
- **Plugin system** - Extensible architecture
- **Mobile version** - Cross-platform mobile app

## 📞 Getting Help

- 📧 **Email**: [your-email@example.com]
- 💬 **Discussions**: Use GitHub Discussions for questions
- 🐛 **Issues**: Report bugs via GitHub Issues
- 📖 **Documentation**: Check the docs folder

## 🙏 Acknowledgments

Thank you for contributing to Music Theory Engine! Your contributions help musicians worldwide learn and practice music theory.

🎸🎵 Happy coding! 🎵🎸