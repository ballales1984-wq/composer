# Piano di Sviluppo - Real-time Analysis

## Obiettivo
Implementare l'analisi in tempo reale che permette agli utenti di suonare tramite tastiera MIDI o tastiera virtuale nel browser e ottenere analisi instantanee di accordi, scale e compatibilità.

---

## Step 1: API per Input Real-time ✅

### 1.1 Endpoint `/api/analyzer/realtime/analyze` ✅
- Accetta note singole o multiple (fino a 6 note simultanee)
- Supporta both MIDI note numbers e nomi note
- Ritorna analisi immediata: nota, ottava, frequenza

### 1.2 Endpoint `/api/analyzer/realtime/chord-detect` ✅
- Dato un insieme di note, determina l'accordo
- Ritorna: nome accordo, root, qualità, note

### 1.3 Endpoint `/api/analyzer/realtime/scale-suggest` ✅
- Dato un insieme di note, suggerisce scale compatibili
- Ritorna: scale possibili con percentuali di match

---

## Step 2: Pagina Real-time Analyzer ✅

### 2.1 Nuovo template `realtime.html` ✅
- Tastiera virtuale cliccabile (2 ottave)
- Status connessione MIDI
- Display note attive
- Analisi in tempo reale

### 2.2 Visualizzazione ✅
- Note suonate (visualizzazione a tastiera)
- Accordo rilevato
- Scale compatibili

---

## Step 3: Integrazione Web MIDI API ✅

### 3.1 Hook per tastiera MIDI esterna ✅
- Rilevamento automatico dispositivi MIDI
- Listen per note on/off
- Mapping MIDI note numbers

### 3.2 Gestione eventi ✅
- Note on: aggiungi alla nota attiva
- Note off: rimuovi dalla nota attiva
- Timeout per accordi (500ms)

---

## Step 4: Algoritmo di Rilevamento Accordi ✅

### 4.1 Rilevamento pattern ✅
- Matching con pattern di intervalli noti
- Priorità: triadi > 7th > extended
- Gestione inversioni

### 4.2 Sugar chording ✅
- Normalizzazione delle note
- Rimozione duplicati
- Ordinamento per importanza

---

## Step 5: Miglioramenti Note Model ✅

### 5.1 Aggiunto metodo `from_midi()` ✅
- Crea una Nota da un numero MIDI

### 5.2 Aggiunte proprietà `midi` e `frequency` ✅
- `midi`: numero nota MIDI (0-127)
- `frequency`: frequenza in Hz

---

## Step 6: Bug Fix - Visualizzazione Accordi ✅

### 6.1 Corretto display del nome dell'accordo
- Il nome dell'accordo viene ora visualizzato correttamente con spazio tra root e qualità (es. "C Major" invece di "CMajor")

### 6.2 Corretto display delle note
- Corretto il bug che duplicava l'ottava nel nome della nota (es. "C4C4" invece di "C4")

### 6.3 Migliorata gestione dei casi non rilevati
- Aggiunta gestione migliore per i casi in cui l'accordo non viene rilevato

---

## File modificati/creati

1. `web_app/api/analyzer.py` - Aggiunti endpoints real-time
2. `web_app/templates/realtime.html` - Nuovo template + fix display
3. `web_app/app.py` - Aggiunta route per realtime
4. `music_engine/models/note.py` - Aggiunto from_midi, midi, frequency
5. `web_app/templates/index.html` - Aggiunto link alla pagina realtime

---

## Utilizzo

1. Avviare l'app: `python web_app/app.py`
2. Aprire il browser a `http://127.0.0.1:5000/realtime`
3. Suonare sulla tastiera virtuale o connettere un controller MIDI
4. Vedere l'analisi in tempo reale degli accordi e delle scale

---

*Implementato: 2026-02-14*
*Ultimo fix: 2026-02-15*

