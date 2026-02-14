# Piano di Sviluppo Unificato - Music Theory Engine

## 📊 Riepilogo Stato Attuale

### ✅ Completati
- Core: Note, Chord, Scale, Progression
- Web App: Flask con API complete
- CLI: Click-based
- Docker e CI/CD
- Integrations: music21, mingus
- Realtime analyzer con tastiera virtuale

### 🔄 In Corso
- Orchestrator Module (controller.py esistente)
- Custom Exceptions (modulo creato, da integrare)

### ⏳ Da Completare

---

## 🎯 PIANO DI LAVORO PRIORITARIO

### FASE 1: Custom Exceptions (Immediata)
**Obiettivo**: Integrare le eccezioni personalizzate nei moduli core

- [ ] 1.1 Integrare eccezioni in `chord.py`
- [ ] 1.2 Integrare eccezioni in `scale.py`
- [ ] 1.3 Testare il funzionamento

### FASE 2: Combined Display (Breve termine)
**Obiettivo**: Integrare la visualizzazione fretboard con le altre pagine

- [ ] 2.1 Aggiungere pulsante "View on Fretboard" in scales.html
- [ ] 2.2 Aggiungere pulsante "View on Fretboard" in chords.html

### FASE 3: Orchestrator Completo (Medio termine)
**Obiettivo**: Completare il modulo orchestrator

- [ ] 3.1 Creare progression_db.py (database progressioni per genere)
- [ ] 3.2 Creare rhythm_engine.py (template ritmici)
- [ ] 3.3 Creare generator.py (generatore progressioni)
- [ ] 3.4 Creare carousel.py (circle of fifths)

### FASE 4: Visualizzazioni (Medio termine)
**Obiettivo**: Nuove visualizzazioni

- [ ] 4.1 Creare keyboard.py (tastiera virtuale avanzata)
- [ ] 4.2 Creare diagrams.py (diagrammi accordi/scale)
- [ ] 4.3 Creare tablature.py (tablature chitarra)

### FASE 5: Analisi API (Medio termine)
**Obiettivo**: Endpoint API avanzati

- [ ] 5.1 `/api/analysis/key` - Analisi tonalità
- [ ] 5.2 `/api/analysis/compatibility` - Compatibilità accordo-scala
- [ ] 5.3 `/api/analysis/progressions` - Generazione progressioni

### FASE 6: Audio Module (Lungo termine)
**Obiettivo**: Sintesi audio e MIDI

- [ ] 6.1 Completare synthesizer.py
- [ ] 6.2 Completare midi_renderer.py
- [ ] 6.3 Completare player.py
- [ ] 6.4 Creare adapter per modelli

---

## 📁 File da Modificare/Creare

### FASE 1: Custom Exceptions
- `music_engine/models/chord.py`
- `music_engine/models/scale.py`

### FASE 2: Combined Display
- `web_app/templates/scales.html`
- `web_app/templates/chords.html`

### FASE 3: Orchestrator
- `music_engine/generator/progression_db.py` (NUOVO)
- `music_engine/generator/rhythm_engine.py` (NUOVO)
- `music_engine/generator/generator.py` (NUOVO)
- `music_engine/generator/carousel.py` (NUOVO)

### FASE 4: Visualizzazioni
- `music_engine/visualization/keyboard.py` (NUOVO)
- `music_engine/visualization/diagrams.py` (NUOVO)
- `music_engine/visualization/tablature.py` (NUOVO)

---

## 🚀 Prossimi Passi

1. **Partire dalla FASE 1**: Integrare custom exceptions in chord.py e scale.py
2. **Poi FASE 2**: Aggiungere link a fretboard nelle pagine
3. **Continuare con FASE 3-6** secondo priorità

---

*Data creazione: 2026-02-14*

