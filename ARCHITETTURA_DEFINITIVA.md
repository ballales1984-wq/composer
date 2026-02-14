# Architettura Definitiva - Music Theory Engine

## Visione

Applicazione **SPA (Single Page Application)** dove ogni pagina mostra tutti i componenti musicali (scale, accordi, arpeggi, triadi) con audio clickable su ogni elemento.

---

## Struttura SPA

```
┌─────────────────────────────────────────────────────────┐
│                      HEADER/NAV                         │
│  Home | Scales | Chords | Fretboard | Progressions     │
├─────────────────────────────────────────────────────────┤
│                                                         │
│                    MAIN CONTENT                         │
│                                                         │
│  ┌─────────────────┐  ┌─────────────────────────────┐  │
│  │   CONTROLS      │  │     VISUALIZATION AREA     │  │
│  │                 │  │                             │  │
│  │  - Note Root   │  │  - Fretboard (SVG)        │  │
│  │  - Type        │  │  - Chord Diagrams          │  │
│  │  - Tuning      │  │  - Scale Notes             │  │
│  │  - Display     │  │  - Arpeggio Patterns      │  │
│  │                 │  │  - Triads                 │  │
│  └─────────────────┘  └─────────────────────────────┘  │
│                                                         │
├─────────────────────────────────────────────────────────┤
│                      FOOTER                             │
└─────────────────────────────────────────────────────────┘
```

---

## Pagine Principali

### 1. Home (`/`)
- Dashboard con card per ogni sezione
- Link rapido alle funzionalità

### 2. Scales (`/scales`)
**Mostra:**
- Note della scala (lista)
- Intervalli della scala
- Fretboard con note evidenziate
- Diagramma tastiera (piano/chitarra)
- Audio clickable su ogni nota

**Controlli:**
- Root note selector
- Scale type (major, minor, modes, pentatonic, blues)
- Numero ottave

### 3. Chords (`/chords`)
**Mostra:**
- Note dell'accordo (lista)
- Fretboard con posizioni accordo
- Chord diagram (box)
- Triadi (1-3-5, inversioni)
- Arpeggio pattern
- Audio clickable su ogni nota

**Controlli:**
- Root note selector
- Quality (maj, min, dim, aug, 7th, maj7, etc.)
- Voicing/position selector

### 4. Fretboard (`/fretboard`)
**Mostra:**
- Tastiera chitarra completa
- Scale visualization
- Chord visualization
- Combined scale+chord
- Arpeggios patterns
- Triads on fretboard
- Audio clickable su ogni nota

**Controlli:**
- Tuning selector
- Num frets
- Display mode (scale/chord/both/all)
- Root note

### 5. Progressions (`/progressions`)
**Mostra:**
- Analisi progressione
- Numeri romani
- Scale suggerite
- Chord diagrams per ogni accordo
- Fretboard visualization
- Audio clickable

**Controlli:**
- Key selector
- Chords input
- Expand/continue buttons

### 6. Analyzer (`/analyzer`)
**Mostra:**
- Note inserite
- Tonalità rilevata
- Accordi identificati
- Analisi armonica
- Fretboard visualization
- Audio clickable

### 7. Realtime (`/realtime`)
**Mostra:**
- Virtual keyboard (piano)
- Analisi in tempo reale
- Note suonate
- Fretboard visualization
- Audio clickable

---

## Componenti Condivisi (JS)

### `fretboard.js` - GuitarFretboard
Usato in: Scales, Chords, Fretboard, Progressions, Analyzer, Realtime

```javascript
// Usage
const fretboard = new GuitarFretboard('container-id', {
    numFrets: 15,
    tuning: 'standard',
    showFretNumbers: true,
    showStringNames: true,
    onNoteClick: (note) => playAudio(note)
});
```

### `chord_diagram.js` - ChordBoxDiagram
Usato in: Chords, Fretboard, Progressions

### `audio_player.js` - AudioPlayer
Centralizzato per tutti i playback audio

```javascript
// Usage
const audio = new AudioPlayer();
audio.playNote('C', 4);  // Play C4
audio.playChord(['C', 'E', 'G']);  // Play C major
```

### `virtual_keyboard.js` - VirtualKeyboard
Usato in: Realtime, Analyzer

---

## API Unificate

### `/api/music/notes`
Restituisce: note, frequenze, ottave

### `/api/music/scales`
- `?root=C&type=major` → note, intervalli, gradi

### `/api/music/chords`  
- `?root=C&quality=maj` → note, tipi, posizioni chitarra

### `/api/music/arpeggios`
- `?root=C&quality=maj` → pattern, note

### `/api/music/triads`
- `?root=C` → triadi (maggiore, minore, diminuita, aumentata)

### `/api/analysis/*`
- Key detection
- Chord identification
- Progression analysis

---

## Audio System

### Ovunque clickable:
- ✅ Note sulla fretboard
- ✅ Note negli elenchi
- ✅ Accordi nei diagrammi
- ✅ Tasti della tastiera virtuale
- ✅ Note nelle progressioni

### Implementazione:
```javascript
// Audio context condiviso
class AudioManager {
    constructor() {
        this.context = new AudioContext();
    }
    
    playNote(note, octave = 4) {
        // Synthesizer playback
    }
    
    playChord(notes) {
        // Play multiple notes
    }
}
```

---

## Flusso Dati

```
User Input → API Call → Backend Processing → JSON Response 
    ↓
Frontend Update → Re-render Components → Audio Ready
```

---

## Ridondanze Risolte

| Funzionalità | Prima | Dopo |
|-------------|-------|------|
| Visualizzazione scala | Scales, Fretboard | Componente condiviso |
| Visualizzazione accordo | Chords, Fretboard, Progressions | Componente condiviso |
| Audio playback | Solo Fretboard | Ovunque (AudioManager) |
| Fretboard | Diverse pagine | Un componente riutilizzato |

---

## File da Modificare/Creare

### Nuovi file:
- `web_app/static/js/audio_manager.js` - Gestore audio centralizzato
- `web_app/static/js/components/` - Directory per componenti condivisi
- `web_app/templates/unified.html` - Template base per SPA

### Da refactoring:
- `fretboard.js` - Estendere per supportare tutti i modi
- `chord_diagram.js` - Integrare con AudioManager
- Template pages - Semplificare usando componenti condivisi

---

## Implementazione Progressiva

### Fase 1: Audio Manager
1. Creare `audio_manager.js`
2. Integrare in Fretboard (già funziona)
3. Estendere a Chords

### Fase 2: Componenti Condivisi
1. Creare directory `js/components/`
2. Muovere fretboard.js in components/
3. Muovere chord_diagram.js in components/

### Fase 3: Refactoring Pagine
1. Scales - mostra anche accordi
2. Chords - mostra anche fretboard
3. Unificare stile

### Fase 4: SPA
1. Convertire a routing client-side
2. Caricamento dinamico componenti

---

## Note

- Mantenere backward compatibility
- Testare ogni componente separatamente
- Documentare API nuove
- Performance: lazy loading per componenti pesanti (SVG complessi)

