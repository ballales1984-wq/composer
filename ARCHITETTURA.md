# Music Theory Engine - Architettura del Progetto

## Panoramica

L'applicazione è un'applicazione web Flask per esplorare la teoria musicale in modo interattivo.

## Struttura delle Pagine

### 1. **Home** (`/`) 
Dashboard principale con link a tutte le funzionalità.

### 2. **Scales** (`/scales`)
- **Scopo**: Esplorare scale musicali
- **Funzionalità**: 
  - Seleziona nota root e tipo di scala
  - Visualizza note della scala
  - Visualizza intervalli
  - Opzionale: mostra sulla tastiera/fretboard

### 3. **Chords** (`/chords`)
- **Scopo**: Costruire e visualizzare accordi
- **Funzionalità**:
  - Seleziona nota root e qualità accordo
  - Visualizza note dell'accordo
  - Visualizza diagramma accordi chitarra
  - Audio playback

### 4. **Fretboard** (`/fretboard`)
- **Scopo**: Visualizzazione tastiera chitarra
- **Funzionalità**:
  - Note, scale, accordi sulla tastiera
  - Diversi tuning (standard, drop D, open G, etc.)
  - Modalità combinata scala + accordo
  - Click su nota per audio

### 5. **Progressions** (`/progressions`)
- **Scopo**: Analizzare e generare progressioni di accordi
- **Funzionalità**:
  - Analizza progressione data
  - Converti in numeri romani
  - Suggerisci scale compatibili
  - Genera/espandi progressioni
  - **Mostra diagrammi accordi**

### 6. **Analyzer** (`/analyzer`)
- **Scopo**: Analisi armonica in tempo reale
- **Funzionalità**:
  - Analizza note inserite
  - Trova tonalità
  - Analizza intervalli

### 7. **Realtime** (`/realtime`)
- **Scopo**: Analisi in tempo reale con tastiera virtuale
- **Funzionalità**:
  - Tastiera virtuale su schermo
  - Analisi live delle note suonate

## Struttura API

### `/api/scales/*`
- `GET /api/scales/list` - Lista tutte le scale
- `GET /api/scales/notes?root=C&type=major` - Note di una scala
- `GET /api/scales/intervals?type=major` - Intervalli di una scala

### `/api/chords/*`
- `GET /api/chords/list` - Lista tutti gli accordi
- `GET /api/chords/notes?root=C&quality=maj` - Note di un accordo
- `GET /api/chords/voicings?root=C&quality=maj` - Posizioni chitarra

### `/api/progressions/*`
- `GET /api/progressions/analyze?chords=C,F,G&key=C` - Analizza progressione
- `GET /api/progressions/roman?key=C&chords=C,G` - Converti in numeri romani
- `GET /api/progressions/scales?chords=C,G` - Scale compatibili

### `/api/analysis/*`
- `GET /api/analysis/key?notes=C,E,G` - Trova tonalità
- `GET /api/analysis/chord?notes=C,E,G` - Identifica accordo

### `/api/orchestrator/*`
- `POST /api/orchestrator/suggest` - Suggerisci progressioni
- `POST /api/orchestrator/expand` - Espandi progressione
- `POST /api/orchestrator/continuation` - Continua progressione

### `/api/circle/*`
- `GET /api/circle/of-fifths` - Dati cerchio delle quinte
- `GET /api/circle/keys` - Lista tonalità

## Modelli (music_engine/models)

- **Note**: Nota singola
- **Chord**: Accordo con root, qualità, note
- **Scale**: Scala con root, tipo, note
- **Progression**: Progressione di accordi
- **Arpeggio**: Note dell'arpeggio

## Diagrammi e Visualizzazioni

### Fretboard (fretboard.js)
Visualizzazione SVG della tastiera chitarra con:
- Note evidenziate
- Colorazione per tipo (root, scala, accordo)
- Click per audio

### Chord Diagrams (chord_diagram.js)
Diagrammi standard per chitarra con:
- Dita indicate
- Barre
- Note muti e aperte

## Routing e Flusso

```
Home
├── Scales → API scales → Visualizza scale
├── Chords  → API chords → Diagrammi + Audio
├── Fretboard → API scales/chords → Visualizzazione tastiera
├── Progressions → API progressions → Analisi + Diagrammi
├── Analyzer  → API analysis → Analisi armonica
└── Realtime → API analysis → Tastiera virtuale
```

## Ridondanze Identificate

1. **Visualizzazione scale**: presente in Scales, Fretboard, e potenzialmente Analyzer
2. **Visualizzazione accordi**: presente in Chords, Fretboard, Progressions
3. **Audio playback**: implementato in Fretboard, potrebbe mancare in Chords
4. **Diagrammi accordi**: in Chords e Progressions

## Raccomandazioni

1. **Unificare visualizzazioni**: Creare componenti condivisi
2. **Migliorare coerenza**: Stesso stile e comportamento tra pagine
3. **Aggiungere documentazione**: Commenti nel codice
4. **Test**: Verificare che tutte le API rispondano correttamente

