# Music Composer Project - Implementation Plan

## 📊 Current Status Summary

### Phase 0: Setup - [COMPLETED] ✅
- [x] Repository structure created
- [x] Python environment configured
- [x] Dependencies: music21, mingus, flask, etc.

### Phase 1: Engine Musicale - [COMPLETED] ✅
- [x] notes.py - Note and interval handling
- [x] chords.py - Chord construction and compatibility
- [x] scales.py - Scale generation
- [x] progressions.py - Progression handling
- [x] harmony.py - Chord-scale compatibility
- [x] intervals.py - Interval calculations

### Phase 2: Orchestratore - [IN PROGRESS] 🔄
**Current Focus**

### Phase 3: Generator Progressioni - [PENDING] ⏳

### Phase 4: Visualizzazione - [PENDING] ⏳

### Phase 5: Esercizi e Metronomo - [PENDING] ⏳

### Phase 6: Integrazione IA - [PENDING] ⏳

### Phase 7: Template e Generi - [PENDING] ⏳

---

## 🎯 Phase 2: Orchestrator Module

### File Structure to Create:
```
music_engine/orchestrator/
├── __init__.py
├── controller.py      # Coordinates input → engine → generator → visual
├── solver.py          # Scale and chord suggestions
├── expansion.py       # Expand 2-3 chord progressions
└── genre_rules.py     # Jazz/Pop/Rock adaptation
```

### Implementation Tasks:

#### 2.1 controller.py
- [ ] InputHandler class - handles various input types
- [ ] OutputFormatter class - formats suggestions for display
- [ ] Coordinator class - orchestrates modules

#### 2.2 solver.py  
- [ ] ScaleSolver - suggests scales for given context
- [ ] ChordSolver - suggests next chords
- [ ] ConflictResolver - resolves harmonic conflicts

#### 2.3 expansion.py
- [ ] ProgressionExpander - expands 2-3 chord progressions
- [ ] continuation_generator.py - generates continuations
- [ ] substitution_handler.py - chord substitutions

#### 2.4 genre_rules.py
- [ ] JazzRules - jazz-specific chord/scale suggestions
- [ ] PopRules - pop music patterns
- [ ] RockRules - rock music patterns
- [ ] GenreDetector - detects genre from input

---

## 🎯 Phase 3: Generator Progressioni

### File Structure:
```
music_engine/generator/
├── __init__.py
├── progression_db.py   # Pool of progressions by genre
├── rhythm_engine.py    # Rhythm templates / metronome
├── generator.py        # Create/modify sequences
└── carousel.py        # Chord carousel/circle of fifths
```

### Implementation Tasks:

#### 3.1 progression_db.py
- [ ] Jazz progressions database (ii-V-I, etc.)
- [ ] Pop progressions database (I-V-vi-IV, etc.)
- [ ] Rock progressions database
- [ ] Blues progressions

#### 3.2 rhythm_engine.py
- [ ] RhythmTemplate class
- [ ] Beat subdivision handling
- [ ] Tempo/BPM control
- [ ] Time signature support

#### 3.3 generator.py
- [ ] ProgressionGenerator - creates progressions
- [ ] VariationEngine - applies variations
- [ ] SequenceModifier - allows user modifications

#### 3.4 carousel.py
- [ ] CircleOfFifths implementation
- [ ] ChordCarousel - visual chord selector
- [ ] Related II-V-I generator

---

## 🎯 Phase 4: Visualizzazione

### File Structure:
```
music_engine/visualization/
├── __init__.py
├── keyboard.py        # Virtual piano keyboard
├── diagrams.py        # Chord/scale diagrams
├── tablature.py      # Guitar tablature
└── display.py        # Live display updates
```

### Implementation Tasks:

#### 4.1 keyboard.py
- [ ] VirtualKeyboardWidget - interactive piano
- [ ] Note highlighter
- [ ] Range selector

#### 4.2 diagrams.py
- [ ] ChordDiagramGenerator
- [ ] ScaleDiagramGenerator
- [ ] Mode visualizations

#### 4.3 tablature.py
- [ ] TabRenderer - renders guitar tabs
- [ ] Interactive tablature
- [ ] Multiple tuning support

#### 4.4 display.py
- [ ] LiveUpdateDisplay
- [ ] Fretboard sync
- [ ] Animation system

---

## 🎯 Phase 5: Esercizi e Metronomo

### File Structure:
```
music_engine/exercises/
├── __init__.py
├── scale_exercises.py     # Scale practice
├── progression_exercises.py # Improvisation practice
├── metronome.py           # Rhythm synchronization
└── practice_session.py    # Practice session manager
```

### Implementation Tasks:

#### 5.1 scale_exercises.py
- [ ] ScalePracticeGenerator
- [ ] Mode exercises
- [ ] Speed exercises

#### 5.2 progression_exercises.py
- [ ] Improvisation prompts
- [ ] Chord soloing exercises
- [ ] Target notes practice

#### 5.3 metronome.py
- [ ] MetronomeEngine
- [ ] Accent patterns
- [ ] Tempo automation

#### 5.4 practice_session.py
- [ ] Session scheduler
- [ ] Progress tracking
- [ ] Difficulty progression

---

## 🎯 Phase 6: IA Integration (Ollama)

### File Structure:
```
music_engine/ai/
├── __init__.py
├── assistant.py       # AI musical consultant
├── prompt_manager.py # Prompt handling
└── context.py        # Context management
```

### Implementation Tasks:

#### 6.1 assistant.py
- [ ] OllamaAssistant class
- [ ] MusicalQueryHandler
- [ ] Suggestion engine

#### 6.2 prompt_manager.py
- [ ] PromptTemplateManager
- [ ] ContextBuilder
- [ ] ResponseParser

#### 6.3 context.py
- [ ] MusicalContext class
- [ ] History manager
- [ ] Preference learning

---

##: Template e Generi

### File 🎯 Phase 7 Structure:
```
templates/
├── jazz_template.json
├── pop_template.json
├── rock_template.json
└── blues_template.json
```

### Implementation Tasks:

#### 7.1 Genre Templates
- [ ] Jazz template with typical progressions
- [ ] Pop template with common patterns
- [ ] Rock template with power chords
- [ ] Blues template with 12-bar patterns

#### 7.2 Template Engine
- [ ] TemplateLoader
- [ ] TemplateApplier
- [ ] Custom template creator

---

## 📋 Web API Extensions Needed

### New Endpoints to Add:
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/orchestrator/suggest` | POST | Get chord/scale suggestions |
| `/api/orchestrator/expand` | POST | Expand progression |
| `/api/generator/progression` | GET | Generate progression |
| `/api/generator/carousel` | GET | Get circle of fifths data |
| `/api/exercises/generate` | POST | Generate practice exercise |
| `/api/metronome/start` | POST | Start metronome |
| `/api/ai/query` | POST | Query AI assistant |

---

## ✅ Test Scenarios

### Phase 2 Tests:
- [ ] Input: 2-3 chord progression → Output: scale suggestions
- [ ] Input: Jazz context → Output: jazz-appropriate suggestions
- [ ] Input: Conflict resolution → Output: resolved progression

### Phase 3 Tests:
- [ ] Generate progression → Output: listenable sequence
- [ ] Genre selection → Output: genre-appropriate progression
- [ ] Chord substitution → Output: substituted progression

### Phase 4 Tests:
- [ ] Chord selection → Visual: keyboard highlight
- [ ] Scale selection → Visual: fretboard + tablature
- [ ] Real-time update → Visual: smooth animation

### Phase 5 Tests:
- [ ] Exercise generation → Practice session starts
- [ ] Metronome → Audio + visual beat
- [ ] Progression exercise → Improv prompts

### Phase 6 Tests:
- [ ] "Cmaj7 → G7, which scale?" → AI: correct suggestion
- [ ] Context-aware suggestions
- [ ] Genre-specific help

---

*Last Updated: 2026-02-14*
*Priority: Phase 2 (Orchestrator) is current focus*

