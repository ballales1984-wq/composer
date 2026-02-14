# Piano di Integrazione: music21 e mingus

## Informazioni Raccoglite

### Struttura Attuale del Progetto
- **Modelli esistenti**: Note, Chord, Scale, Progression, Arpeggio
- **Sistema interno**: Basato su semitoni (0-11) con conversione note/nomi
- **Dipendenze attuali**: customtkinter, pillow, pyinstaller, numpy, pyaudio, simpleaudio, mido

### Librerie da Integrare
1. **music21**: Libreria completa per analisi musicale, MIDI, notazione
2. **mingus**: Teoria musicale avanzata, progressioni di accordi, analisi numeri romani

---

## Piano di Implementazione

### 1. Aggiornamento Dipendenze
- Aggiungere `music21` e `mingus` a `requirements.txt`

### 2. Creazione Modulo Integrazione (`music_engine/integrations/`)
Creare una nuova directory con:

#### 2.1 Adattatori music21 (`music_engine/integrations/music21_adapter.py`)
- `Music21Converter`: Classe per convertire tra i modelli interni e oggetti music21
  - `note_to_music21(note: Note) -> music21.note.Note`
  - `music21_to_note(m21_note) -> Note`
  - `chord_to_music21(chord: Chord) -> music21.chord.Chord`
  - `music21_to_chord(m21_chord) -> Chord`
  - `scale_to_music21(scale: Scale) -> music21.scale.Scale`
  - `stream_to_progression(stream) -> Progression`
- Funzionalità aggiuntive: analisi harmony, MIDI import/export

#### 2.2 Adattatori mingus (`music_engine/integrations/mingus_adapter.py`)
- `MingusConverter`: Classe per convertire tra i modelli interni e oggetti mingus
  - `note_to_mingus(note: Note) -> mingus.containers.Note`
  - `mingus_to_note(mingus_note) -> Note`
  - `chord_to_mingus(chord: Chord) -> mingus.containers.Chord`
  - `mingus_to_chord(mingus_chord) -> Chord`
  - `progression_to_mingus(prog: Progression) -> mingus.containers.Progressions`
- Funzionalità aggiuntive: roman numeral analysis, diatonic chord generation

#### 2.3 Factory unificata (`music_engine/integrations/factory.py`)
- `IntegrationFactory`: Punto di accesso centrale
  - `get_music21_converter() -> Music21Converter`
  - `get_mingus_converter() -> MingusConverter`
  - `convert_from_library(library_name, data)`

### 3. Aggiornamento Modelli
- Aggiungere metodi di conversione ai modelli esistenti:
  - `Note.to_music21()`, `Note.from_music21()`
  - `Note.to_mingus()`, `Note.from_mingus()`
  - `Chord.to_music21()`, `Chord.from_music21()`
  - `Chord.to_mingus()`, `Chord.from_mingus()`
  - `Scale.to_music21()`, `Scale.from_music21()`
  - `Progression.to_mingus()`, `Progression.from_mingus()`

### 4. Aggiornamento `__init__.py`
- Esportare i nuovi moduli di integrazione

---

## File da Modificare/Creare

| File | Azione |
|------|--------|
| `music_engine/requirements.txt` | Modificato - aggiungere dipendenze |
| `music_engine/models/note.py` | Modificato - aggiungere metodi conversione |
| `music_engine/models/chord.py` | Modificato - aggiungere metodi conversione |
| `music_engine/models/scale.py` | Modificato - aggiungere metodi conversione |
| `music_engine/models/progression.py` | Modificato - aggiungere metodi conversione |
| `music_engine/models/__init__.py` | Modificato - esportare nuove funzionalità |
| `music_engine/integrations/__init__.py` | Creato - modulo integrazione |
| `music_engine/integrations/music21_adapter.py` | Creato - adattatore music21 |
| `music_engine/integrations/mingus_adapter.py` | Creato - adattatore mingus |
| `music_engine/integrations/factory.py` | Creato - factory unificata |

---

## Passi Successivi

1. Installare le nuove dipendenze
2. Creare la struttura del modulo integrazione
3. Implementare gli adattatori
4. Aggiornare i modelli esistenti
5. Testare l'integrazione

