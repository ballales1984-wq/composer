# Piano di Sviluppo - Music Theory Engine

## 📋 Analisi dello Stato Attuale

### ✅ Già Implementato:
- **Modelli core**: Note, Chord, Scale, Progression, Fretboard
- **Integrazioni**: music21 e mingus adapters
- **API Web**: scales, chords, progressions, analysis endpoints
- **UI Templates**: index, scales, chords, progressions, fretboard, about
- **Fretboard Visualization**: Visualizzazione interattiva con click per play note

### 🔄 Da Implementare:
1. **HarmonyEngine** - Motore di compatibilità accordo-scala
2. **Analisi unificata** - Accetta accordo O scala in input
3. **Compatibilità tonale** - Logica armonica tradizionale
4. **Compatibilità modale** - Logica modale
5. **Miglioramento UI** - Unified input per accordi e scale

---

## 📝 PIANO DI LAVORO

### Step 1: Creare HarmonyEngine (core/harmony.py)
- Classe per analisi accordo-scala
- Metodo `tonal_compatibility()` - compatibilità tonale
- Metodo `modal_compatibility()` - compatibilità modale
- Metodo `find_compatible_scales()` - trova scale compatibili
- Metodo `find_compatible_chords()` - trova accordi compatibili

### Step 2: Creare Interval class (core/intervals.py)
- Classe per gestire intervalli musicali
- Metodi per calcolare intervalli tra note
- Naming standard (unison, minor 2nd, major 2nd, etc.)

### Step 3: Creare analyzer endpoint unificato (web_app/api/analyzer.py)
- Accetta input: accordo (Cmaj7) O scala (C major)
- Restituisce:
  - Note costitutive
  - Intervalli
  - Qualità (per accordi)
  - Gradi (per scale)
  - Scale/Accordi compatibili
  - Posizioni sulla tastiera

### Step 4: Creare UI unificata (web_app/templates/analyzer.html)
- Input field che accetta accordo O scala
- Risultati:
  - Note/intervalli/qualità
  - Scale compatibili (tonale + modale)
  - Posizioni fretboard
  - Accordi armonizzati (per scale)

---

## 🎯 CLASSI DA CREARE

### Interval (core/intervals.py)
```python
class Interval:
    """Rappresenta un intervallo musicale."""
    
    # Intervalli standard (semitoni)
    INTERVALS = {
        0: 'unison', 1: 'minor 2nd', 2: 'major 2nd',
        3: 'minor 3rd', 4: 'major 3rd', 5: 'perfect 4th',
        6: 'tritone', 7: 'perfect 5th', 8: 'minor 6th',
        9: 'major 6th', 10: 'minor 7th', 11: 'major 7th',
        12: 'octave'
    }
    
    def __init__(self, semitones: int)
    def get_name() -> str
    def get_short_name() -> str
    @staticmethod
    def between(note1, note2) -> int
```

### HarmonyEngine (core/harmony.py)
```python
class HarmonyEngine:
    """Motore di analisi armonica per compatibilità accordo-scala."""
    
    def __init__(self)
    
    # Tonal compatibility
    def tonal_compatibility(chord, scale) -> dict
    def get_tonal_scales(chord) -> List[Scale]
    
    # Modal compatibility  
    def modal_compatibility(chord, scale) -> dict
    def get_modal_scales(chord) -> List[Scale]
    
    # General compatibility
    def find_compatible_scales(chord) -> dict
    def find_compatible_chords(scale) -> List[Chord]
    def analyze_input(input_str) -> dict
```

---

## 📂 Struttura File

```
music_engine/
├── core/
│   ├── __init__.py
│   ├── intervals.py      [NUOVO]
│   ├── harmony.py        [NUOVO]
│   ├── notes.py
│   ├── scales.py
│   ├── chords.py
│   ├── arpeggios.py
│   └── progressions.py
├── models/
│   ├── __init__.py
│   ├── note.py
│   ├── chord.py
│   ├── scale.py
│   ├── fretboard.py
│   ├── progression.py
│   └── arpeggio.py
├── integrations/
│   ├── __init__.py
│   ├── factory.py
│   ├── music21_adapter.py
│   └── mingus_adapter.py
└── web_app/
    ├── api/
    │   ├── analyzer.py    [NUOVO]
    │   ├── scales.py
    │   ├── chords.py
    │   ├── progressions.py
    │   └── analysis.py
    └── templates/
        └── analyzer.html  [NUOVO]
```

---

## ✅ Checklist Implementazione

- [ ] 1. Creare Interval class
- [ ] 2. Creare HarmonyEngine class
- [ ] 3. Implementare metodi compatibilità tonale
- [ ] 4. Implementare metodi compatibilità modale
- [ ] 5. Creare API endpoint /api/analyzer
- [ ] 6. Creare template analyzer.html
- [ ] 7. Integrare con fretboard esistente
- [ ] 8. Testare con vari input

---

*Ultimo aggiornamento: 2026-02-14*

