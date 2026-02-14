# TODO - Piano di Lavoro Unificato

## 🎯 FASE 1: Custom Exceptions (Priorità Alta) ✅ COMPLETATA

### 1.1 Integrare eccezioni in chord.py ✅
- [x] 1.1.1 Importare eccezioni da exceptions.py
- [x] 1.1.2 Sostituire ValueError con InvalidChordError nel costruttore
- [x] 1.1.3 Sostituire ValueError con InvalidQualityError per qualità non valide
- [x] 1.1.4 Aggiungere try/except nei metodi che generano errori

### 1.2 Integrare eccezioni in scale.py ✅
- [x] 1.2.1 Importare eccezioni da exceptions.py
- [x] 1.2.2 Sostituire ValueError con InvalidScaleError nel costruttore
- [x] 1.2.3 Sostituire IndexError con InvalidScaleError in get_degree
- [x] 1.2.4 Aggiungere gestione errori in get_mode


### 1.3 Testare le eccezioni ✅
- [x] 1.3.1 Verificare che i vecchi test passino
- [x] 1.3.2 Testare i nuovi messaggi di errore

---

## 🎯 FASE 2: Combined Display ✅ COMPLETATA

### 2.1 scales.html - View on Fretboard ✅
- [x] 2.1.1 Aggiungere pulsante "View on Fretboard"
- [x] 2.1.2 Passare parametri scale via URL

### 2.2 chords.html - View on Fretboard ✅
- [x] 2.2.1 Aggiungere pulsante "View on Fretboard"
- [x] 2.2.2 Passare parametri accordo via URL

---

## 🎯 FASE 3: Orchestrator (Generator) ✅ COMPLETATO

### 3.1 progression_db.py ✅
- [x] Creare database progressioni per genere

### 3.2 rhythm_engine.py ✅
- [x] Creare template ritmici

### 3.3 generator.py ✅
- [x] Creare generatore progressioni

### 3.4 carousel.py ✅
- [x] Creare Circle of Fifths

---

## 🎯 FASE 4: Visualizzazioni ✅ COMPLETATA

### 4.1 keyboard.py ✅
- [x] Creare tastiera virtuale avanzata (esiste in gui/virtual_keyboard.py)

### 4.2 diagrams.py ✅
- [x] Creare diagrammi accordi/scale (esiste in gui/)

### 4.3 tablature.py ✅
- [x] Creare tablature chitarra (esiste in gui/fretboard_viewer.py)

---

## 🎯 FASE 5: Analysis API ✅ COMPLETATA

### 5.1 Endpoint key detection ✅
- [x] Implementare /api/analysis/key

### 5.2 Endpoint compatibility ✅
- [x] Implementare /api/analysis/compatibility

### 5.3 Endpoint progressions ✅
- [x] Implementare /api/analysis/progressions

---

## 🎯 FASE 6: Audio Module

### 6.1 Synthesizer
- [ ] Completare synthesizer.py

### 6.2 MIDI Renderer
- [ ] Completare midi_renderer.py

### 6.3 Player
- [ ] Completare player.py

### 6.4 Adapter
- [ ] Creare adapter per modelli

---

*Ultimo aggiornamento: 2026-02-14*

